"""Bounded codegen evidence tests; never invoke Wine or a compiler."""
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import probe_zero_compare as probe


def assembly(instruction="cmp\tax,0", branch="jle\t@reject"):
    return ("ZERO_TEXT segment byte public 'CODE'\n_zero_compare\tproc\tnear\n"
            "\tmov\tax,word ptr [bp+4]\n\tcmp\tcx,416\n\tjge\t@reject\n"
            f"\t{instruction}\n\t{branch}\n\tcmp\tax,384\n\tjl\t@accept\n"
            "@reject:\n\txor\tax,ax\n\tret\n_zero_compare\tendp\nZERO_TEXT ends\n")


class ZeroCompareTests(unittest.TestCase):
    def test_matrix_contains_only_requested_options_and_signed_sources(self):
        self.assertEqual(len(probe.PROFILES) * len(probe.ZEROS), 16)
        self.assertEqual({flags for _, flags in probe.PROFILES},
                         {("-O", "-Z"), ("-O", "-Z-"), ("-Z",), ("-Z-",)})
        for variant in probe.ZEROS:
            source = probe.source_text(variant)
            self.assertIn("typedef signed short pixel_t;", source)
            self.assertIn("#define top static_cast<pixel_t>(_AX)", source)
            self.assertIn("#define left static_cast<pixel_t>(_CX)", source)
            self.assertEqual(source.count("&&"), 3)
            for forbidden in ("keep_0", "address_0", "__emit", "asm", "0u", "volatile"):
                self.assertNotIn(forbidden, source)

    def test_cmp_and_or_are_distinguished_and_require_signed_reject_branch(self):
        result = probe.inspect_asm(assembly())
        self.assertTrue(result["emits_cmp_ax_zero_jle"])
        self.assertEqual(result["lower_bound_forms"], ["cmp-ax-zero"])
        result = probe.inspect_asm(assembly("or\tax,ax"))
        self.assertFalse(result["emits_cmp_ax_zero_jle"])
        self.assertEqual(result["lower_bound_forms"], ["or-ax-ax"])
        self.assertFalse(probe.inspect_asm(assembly(branch="jbe\t@reject"))["emits_cmp_ax_zero_jle"])

    def test_relocation_symbol_and_nonzero_are_not_zero_immediates(self):
        for operand in ("offset address_0", "1", "0001h", "_zero"):
            self.assertFalse(probe.inspect_asm(assembly("cmp\tax," + operand))["emits_cmp_ax_zero_jle"])
        self.assertTrue(probe.inspect_asm(assembly("cmp\tax,0000h"))["emits_cmp_ax_zero_jle"])

    def test_ambiguous_or_unbounded_body_fails(self):
        with self.assertRaises(ValueError):
            probe.inspect_asm(assembly() + assembly())
        with self.assertRaises(ValueError):
            probe.inspect_asm(assembly().replace("\tret\n", "\tnop\n" * 170))

    def test_compile_case_uses_builder_and_freezes_full_outputs(self):
        class FakeBuilder:
            def __init__(self, root, prefix, msdos):
                self.root, self.msdos, self.records = root, msdos, []

            def execute(self, label, command):
                self.records.append({"output": label, "command": command, "returncode": 0})
                (self.root / "ZERO.ASM").write_text(assembly())

        with tempfile.TemporaryDirectory() as tmp:
            row = probe.compile_case(Path(tmp) / "case", "literal", "O-Z", ("-O", "-Z"),
                                     builder_factory=FakeBuilder)
            self.assertTrue(row["pass"])
            command = row["steps"][0]["command"]
            self.assertIn("-S", command)
            self.assertNotIn("-c", command)
            self.assertEqual(command[-1], "zero.cpp")
            self.assertEqual({item["path"] for item in row["artifacts"]},
                             {"source/zero.cpp", "source/ZERO.ASM", "source/build_dumb.bat"})

    def test_stale_cache_fails_before_build_and_records_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".analysis").mkdir()
            output = root / ".analysis/out"
            with patch.object(probe, "freeze_toolchain", side_effect=ValueError("stale")) as frozen:
                with patch.object(probe, "compile_case") as compile_case:
                    receipt = probe.run(output, root=root)
            self.assertFalse(receipt["pass"])
            self.assertEqual(receipt["results"], [])
            self.assertFalse(frozen.call_args.kwargs["allow_probes"])
            compile_case.assert_not_called()
            self.assertTrue((output / "receipt.json").is_file())

    def test_full_matrix_orchestration_is_serial_and_never_claims_exact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("config/toolchain.toml", "config/targets.toml",
                         "scripts/lib/reference_build.py", "scripts/lib/replay_toolchain.py",
                         "scripts/lib/toolchain.py",
                         ".analysis/toolchain/wineprefix/drive_c/TC4/BIN/TURBOC.CFG"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("// frozen test input\n")
            target = SimpleNamespace(valid=True, program_image=b"\0" * probe.TARGET_START + probe.TARGET_BYTES)
            seen = []

            def fake_compile(work, variant, profile, options, *, root):
                seen.append((variant, profile))
                return {"variant": variant, "profile": profile, "pass": True,
                        "inspection": {"lower_bound_forms": ["or-ax-ax"],
                                       "emits_cmp_ax_zero_jle": False}}

            with patch.object(probe, "freeze_toolchain", return_value={"reused": True}):
                with patch.object(probe, "load_target_manifest", return_value={}):
                    with patch.object(probe, "find_artifact", return_value={}):
                        with patch.object(probe, "read_verified_artifact", return_value=b"pinned"):
                            with patch.object(probe, "parse_mz", return_value=target):
                                with patch.object(probe, "compile_case", side_effect=fake_compile):
                                    receipt = probe.run(root / ".analysis/out", root=root)
            self.assertEqual(seen, [(variant, profile) for variant in probe.ZEROS
                                    for profile, _ in probe.PROFILES])
            self.assertTrue(receipt["pass"])
            self.assertFalse(receipt["boss_bg_exact"])
            self.assertTrue(receipt["raw_replay_required"])
            self.assertEqual(receipt["cmp_candidates"], [])


if __name__ == "__main__":
    unittest.main()
