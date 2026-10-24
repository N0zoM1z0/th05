"""Retained decoded views preserve packed identity, frames and observed order."""
import copy
import json
from pathlib import Path
import struct
import shutil
import sys
import tempfile
import tomllib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib import unit_context as uc
from lib.unit_oracle import compare_unit
from lib.replay_toolchain import entry_digest
import replay_units
import progress


class UnitContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def fixture(self, name="op", *, reverse=False, bad_frame=False):
        context = uc.UnitContext(self.root, name)
        context.cache.mkdir(parents=True, exist_ok=True)
        payload = bytes(range(32))
        rows = [{"segment": 0, "offset": 4, "linear": 4}, {"segment": 1, "offset": 0, "linear": 16}]
        if reverse:
            rows.reverse()
        if bad_frame:
            rows[0]["segment"] += 1
        raw = b"opaque synthetic carrier; verification mocked separately"
        artifact = {"id": context.artifact, "sha256": uc.sha(raw)}
        relocations = (json.dumps(rows) + "\n").encode()
        policy = {"target_sha256": uc.sha(raw), "payload_size": 32, "relocation_count": 2,
                  "initial_ss": 10, "initial_sp": 128, "entry_cs": 0, "entry_ip": 0}
        runs = []
        for load in (0x1000, 0x3333):
            data = bytearray(payload)
            for row in rows:
                value = struct.unpack_from("<H", data, row["linear"])[0]
                struct.pack_into("<H", data, row["linear"], (value + load) & 65535)
            runs.append({"load_segment": load, "decoded_end": 32, "final_cs": load,
                         "final_ip": 0, "final_ss": load + 10, "final_sp": 128,
                         "transfer_site": 100, "instruction_count": 123,
                         "relocated_payload_sha256": uc.sha(data)})
        receipt = {**policy, "artifact": context.artifact, "target_size": len(raw),
                   "method": "target-owned-diet-decoder", "payload_sha256": uc.sha(payload),
                   "relocations_sha256": uc.sha(relocations), "policy": policy, "runs": runs,
                   "checks": {key: True for key in ("distinct_load_segments", "relocation_stream_load_invariant",
                       "complete_decoded_bytes_load_invariant", "decoder_output_extent", "restored_entry_and_stack")}}
        (context.cache / "payload.bin").write_bytes(payload)
        (context.cache / "relocations.json").write_bytes(relocations)
        receipt_bytes = json.dumps(receipt).encode()
        (context.cache / "receipt.json").write_bytes(receipt_bytes)
        proof = {"artifact": context.artifact, "kind": "decoded-load-module-only", "packed_target_sha256": artifact["sha256"],
                 "receipt_sha256": uc.sha(receipt_bytes), "payload_sha256": uc.sha(payload),
                 "relocations_sha256": uc.sha(relocations), "payload_size": len(payload), "relocation_count": len(rows), "runs": runs}
        config = {"artifact": context.artifact, "units": [], "target_view": {
            "receipt_sha256": uc.sha(receipt_bytes), "proof_sha256": uc.proof_sha256(proof)}}
        return context, config, artifact, raw

    def load(self, fixture):
        context, config, artifact, raw = fixture
        with patch.object(uc, "load_target_manifest", return_value={"artifacts": [artifact]}), \
             patch.object(uc, "read_verified_artifact", return_value=raw):
            return uc.load_unit_target(context, config)

    def test_decoded_view_has_no_invented_mz_header_and_preserves_nonmonotonic_order(self):
        first = self.load(self.fixture())[1]
        second = self.load(self.fixture(reverse=True))[1]
        self.assertFalse(hasattr(first, "header"))
        self.assertEqual(first.program_image, second.program_image)
        self.assertEqual([row.linear for row in second.relocations], [16, 4])
        comparison = compare_unit(first, second, 0, 0, 32)
        self.assertTrue(comparison["raw_exact"])
        self.assertFalse(comparison["fixups_exact"])

    def test_payload_relocations_and_receipt_tampering_fail_without_running_decoder(self):
        for name in ("payload.bin", "relocations.json", "receipt.json"):
            fixture = self.fixture()
            path = fixture[0].cache / name
            path.write_bytes(path.read_bytes() + b" ")
            with self.subTest(file=name), self.assertRaises(ValueError):
                self.load(fixture)

    def test_relocation_frame_identity_cannot_be_replaced_by_same_linear_operand(self):
        with self.assertRaisesRegex(ValueError, "frame"):
            self.load(self.fixture(bad_frame=True))

    def test_historical_two_load_hash_is_recomputed(self):
        fixture = self.fixture()
        path = fixture[0].cache / "receipt.json"
        receipt = json.loads(path.read_bytes())
        receipt["runs"][1]["relocated_payload_sha256"] = "0" * 64
        path.write_text(json.dumps(receipt))
        fixture[1]["target_view"]["receipt_sha256"] = uc.sha(path.read_bytes())
        with self.assertRaisesRegex(ValueError, "two-load byte hashes"):
            self.load(fixture)

    def test_wrong_artifact_manifest_or_original_identity_is_rejected(self):
        fixture = self.fixture()
        fixture[1]["artifact"] = "th05-maine"
        with self.assertRaisesRegex(ValueError, "different artifact"):
            self.load(fixture)
        fixture = self.fixture()
        fixture[2]["sha256"] = "b" * 64
        with self.assertRaises(ValueError):
            self.load(fixture)

    def test_main_defaults_keep_old_paths_flags_and_entry_identity(self):
        main = uc.UnitContext(self.root)
        self.assertEqual(main.manifest, self.root / "config/exact_units.toml")
        self.assertEqual(main.ledger, self.root / "config/accepted_units.json")
        entry = {"id": "old", "module": "th05/a.cpp"}
        before = entry_digest(entry)
        self.assertEqual(uc.compiler_arguments(entry), ["-c", "-I.", "-O", "-b-", "-3", "-Z", "-d",
                         "-DGAME=5", "-ml", "-DBINARY='M'", "th05/a.cpp"])
        self.assertEqual(entry_digest(entry), before)
        self.assertNotEqual(main.ledger, uc.UnitContext(self.root, "op").ledger)
        self.assertEqual(uc.unit_binary({}, uc.UnitContext(self.root, "maine").binary), "E")
        self.assertEqual(uc.unit_binary({"binary": "O"}, "E"), "O")
        with self.assertRaises(ValueError):
            uc.UnitContext(self.root, "zun")

    def test_empty_op_ledger_does_not_reuse_main_units_with_same_id(self):
        context = uc.UnitContext(self.root, "op")
        context.ledger.parent.mkdir()
        (self.root / "config/accepted_units.json").write_text(json.dumps({"units": [{"id": "same"}]}))
        entries, reasons = replay_units.select_units(self.root, {"units": [{"id": "same"}]}, None,
                                                    ledger=context.ledger)
        self.assertEqual(reasons, {"same": "missing"})

    def test_maine_binary_override_reaches_actual_builder_command_and_archive(self):
        commands = []

        class FakeBuilder:
            def __init__(self, root, prefix, msdos):
                self.root, self.msdos, self.records = root, msdos, []

            def execute(self, label, command):
                commands.append(command)
                if label.endswith(".obj"):
                    (self.root / label).write_bytes(b"object")
                if label == "link":
                    (self.root / "units.exe").write_bytes(b"candidate")

        for name in ("src/a.cpp", "probes/a.asm"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("// synthetic input\n")
        unit = {"id": "a", "source": "src/a.cpp", "module": "th05/a.cpp", "binary": "O", "bindings_source": "probes/a.asm"}
        omf = {key: "identity" for key in replay_units.OMF_FIELDS}
        omf.update(valid=True, translator_comments=["TC86 Borland C++ 4.02"])
        with patch.object(replay_units, "Builder", FakeBuilder), patch.object(replay_units, "describe_omf", return_value=omf), \
             patch.object(replay_units, "parse_mz", return_value=SimpleNamespace(valid=True)):
            replay_units.cold_round(self.root / "work", self.root, [unit], paths={"src/a.cpp", "probes/a.asm"}, binary="E")
        compile_command = next(command for command in commands if "tcc" in command)
        self.assertIn("-DBINARY='O'", compile_command)
        self.assertNotIn("-DBINARY='E'", compile_command)
        archive = json.loads((self.root / "work/source/compiler-arguments.json").read_text())
        self.assertEqual(archive[unit["module"]], uc.compiler_arguments(unit, "E"))
        with self.assertRaisesRegex(ValueError, "conflicting"):
            replay_units.translation_units([unit, {**unit, "id": "b", "binary": "E"}], binary="E")

    def test_nonempty_decoded_summary_requires_no_private_game_or_cache_files(self):
        fixture = self.fixture()
        context, config, artifact, _ = fixture
        proof = self.load(fixture)[2]
        context.manifest.parent.mkdir()
        context.manifest.write_text('artifact = "th05-op"\n[[units]]\nid = "u"\nsource = "src/u.cpp"\n'
            'module = "th05/u.cpp"\nsize = 4\ntarget_start = 0\nfunctions = 1\n[target_view]\n' +
            '\n'.join(f'{key} = "{value}"' for key, value in config["target_view"].items()))
        (self.root / "config/targets.toml").write_text(f'[[artifacts]]\nid = "th05-op"\nsha256 = "{artifact["sha256"]}"\n')
        (self.root / "config/toolchain.toml").write_text("schema_version = 1\n")
        tool_sha = uc.sha((self.root / "config/toolchain.toml").read_bytes())
        entry = tomllib.loads(context.manifest.read_text())["units"][0]
        comparison = {"size": 4, "target_start": 0, "candidate_start": 0, "target_sha256": "a" * 64,
                      "candidate_sha256": "a" * 64, "target_fixups": [], "candidate_fixups": [],
                      "raw_exact": True, "fixups_exact": True, "exact": True}
        omf = {"translator_comments": ["TC86 Borland C++ 4.02"], "dependency_timestamp_normalized_sha256": "obj"}
        result = {"id": "u", "exact": True, "object_normalized_equal": True,
                  "rounds": [comparison, copy.deepcopy(comparison)], "omfs": [omf, copy.deepcopy(omf)],
                  "compiler_arguments": [uc.compiler_arguments(entry, "O")] * 2}
        control = {"raw_exact": False, "exact": False, "target_sha256": "a", "candidate_sha256": "b"}
        accepted = {"artifact": "th05-op", "target_sha256": artifact["sha256"], "target_view": proof,
                    "toolchain_manifest_sha256": tool_sha, "compiled_negative_rejected": True,
                    "compiled_negative_control": control, "units": [{"id": "u", "entry_sha256": entry_digest(entry),
                        "result": result, "source_inputs": [], "target_view": proof}]}
        shutil.rmtree(self.root / ".analysis")
        with patch.object(progress, "load_unit_target", side_effect=AssertionError("private target read")), \
             patch.object(progress, "scoped_snapshot", return_value=[]):
            summary = progress.summarize(self.root, accepted, artifact_name="op")
            self.assertEqual(summary["authored_code_bytes"], 4)
            tampered = copy.deepcopy(accepted)
            tampered["target_view"]["payload_sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "configuration pins"):
                progress.summarize(self.root, tampered, artifact_name="op")

    def test_combined_unit_rows_and_totals_cover_each_artifact(self):
        for name in ("op", "maine"):
            path = uc.UnitContext(self.root, name).manifest
            path.parent.mkdir(exist_ok=True)
            path.touch()

        def summary(size):
            return {"units": [{"id": "same", "size": size}] if size else [], "unit_count": int(bool(size)),
                    "functions": int(bool(size)), "complete_extent_bytes": size, "authored_code_bytes": size,
                    "code_data_bytes": 0, "padding_bytes": 0, "instruction_bytes": size}

        with patch.object(progress, "summarize", side_effect=lambda root, **kwargs:
                          summary({"main": 4, "op": 8, "maine": 0}[kwargs.get("artifact_name", "main")])):
            combined = progress.summarize_all(self.root)
        self.assertEqual(combined["unit_count"], len(combined["units"]))
        self.assertEqual(combined["complete_extent_bytes"], sum(unit["size"] for unit in combined["units"]))
        self.assertEqual(combined["complete_extent_bytes"], 12)
        self.assertEqual([unit["id"] for unit in combined["units"]], ["main:same", "op:same"])


if __name__ == "__main__":
    unittest.main()
