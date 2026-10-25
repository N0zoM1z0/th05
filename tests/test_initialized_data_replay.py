"""Synthetic compiler fixtures exercise DATA orchestration; never invoke Wine."""

import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import replay_units
import progress
from lib.unit_oracle import compare_mapped_unit
from lib.pc98 import parse_mz
from lib.unit_sources import validate_producer_inputs, producer_snapshot
from lib.replay_toolchain import snapshot_paths, digest, entry_digest
from ownership import partition


def record(kind, data):
    framed = bytes([kind]) + struct.pack("<H", len(data) + 1) + data
    return framed + bytes([-sum(framed) & 255])


def object_bytes(data):
    names = b"".join(
        bytes([len(s)]) + s for s in [b"OWNER_TEXT", b"CODE", b"_DATA", b"DATA", b""]
    )
    out = record(0x80, b"\x0eth05/owner.cpp")
    translator = b"TC86 Borland C++ 4.02"
    out += record(0x88, b"\0\0" + bytes([len(translator)]) + translator)
    for name in (b"th05/owner.cpp", b"src/owner.cpp"):
        out += record(0x88, b"\0\xe9" + bytes(4) + bytes([len(name)]) + name)
    out += record(0x96, names) + record(0x98, b"\x28\1\0\1\2\5")
    out += record(0x98, b"\x48" + struct.pack("<H", len(data)) + b"\3\4\5")
    out += record(0xA0, b"\1\0\0\xcb")
    out += record(0xA0, b"\2\0\0" + data[:4]) + record(0x9C, b"\xc8\2\x54\1")
    out += record(0xA0, b"\2\4\0" + data[4:]) + record(0x8A, b"\0")
    return out


def executable(data):
    body = bytearray(32)
    body[0] = 0xCB
    body[16 : 16 + len(data)] = data
    header = struct.pack("<14H", 0x5A4D, 80, 1, 1, 3, 1, 0xFFFF, 0, 16, 0, 0, 0, 28, 0)
    return (header + struct.pack("<HH", 18, 0)).ljust(48, b"\0") + body


class InitializedDataReplayTests(unittest.TestCase):
    def test_shared_tu_cold_rounds_consume_cp932_and_data_negative_without_old_code_relabel(
        self,
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "probes").mkdir()
            canonical = 'const char caption[] = "開始";\nvoid far owner(void) {}\n'
            (root / "src/owner.cpp").write_bytes(canonical.encode())
            (root / "probes/bindings.asm").write_text(".386\nend\n")
            common = {
                "source": "src/owner.cpp",
                "module": "th05/owner.cpp",
                "source_encoding": "cp932",
                "bindings_source": "probes/bindings.asm",
                "origin": "compiler-generated-cxx",
            }
            code = {
                **common,
                "id": "code",
                "segment": "OWNER_TEXT",
                "size": 1,
                "target_start": 0,
                "functions": 1,
            }
            data = {
                **common,
                "id": "data",
                "segment": "_DATA",
                "size": 10,
                "target_start": 16,
                "functions": 0,
                "extent_kind": "initialized-data",
                "data_semantics": ["ui-text", "function-pointers", "state"],
            }
            paths = {"src/owner.cpp", "probes/bindings.asm"}
            calls = []
            consumed = []

            class FakeBuilder:
                def __init__(self, source, prefix, msdos):
                    self.source, self.msdos, self.records = source, msdos, []

                def execute(self, label, command):
                    if "tcc" in command:
                        calls.append(command)
                        raw = (self.source / "src/owner.cpp").read_bytes()
                        consumed.append(raw)
                        # Deterministic fixture compiler: a real CP932 initializer
                        # and far-pointer segment word, independent from its CODE.
                        text = raw.split(b'"')[1]
                        self.data = bytes(4) + text + b"\0\1"
                        (self.source / label).write_bytes(object_bytes(self.data))
                    if label == "link":
                        (self.source / "units.exe").write_bytes(executable(self.data))
                        (self.source / "units.map").write_text(
                            " 0000:0000 0001 C=CODE S=OWNER_TEXT G=OWN M=th05/owner.cpp ACBP=28\n 0000:0010 000A C=DATA S=_DATA G=DGROUP M=th05/owner.cpp ACBP=48\n"
                        )

            mutation = {
                "unit": "data",
                "source": "src/owner.cpp",
                "find": "開始",
                "replace": "終了",
            }
            with (
                patch.object(replay_units, "ROOT", root),
                patch.object(replay_units, "Builder", FakeBuilder),
            ):
                rounds = [
                    replay_units.cold_round(
                        root / name, root, [code, data], paths=paths
                    )
                    for name in ("a", "b")
                ]
                negative = replay_units.cold_round(
                    root / "negative", root, [data], paths=paths, mutation=mutation
                )
            self.assertEqual(
                len(calls), 3
            )  # One true TU per round, not one per extent.
            self.assertEqual(consumed[:2], [canonical.encode("cp932")] * 2)
            self.assertEqual(
                consumed[2], canonical.replace("開始", "終了").encode("cp932")
            )
            self.assertEqual((root / "src/owner.cpp").read_bytes(), canonical.encode())
            target = rounds[0]["candidate"]
            comparisons = [
                compare_mapped_unit(
                    target, r["candidate"], r["source"] / "units.map", data
                )
                for r in rounds
            ]
            result = {
                "id": "data",
                "exact": True,
                "object_normalized_equal": True,
                "rounds": comparisons,
                "omfs": [r["omfs"]["data"] for r in rounds],
            }
            progress.validate_result(data, result)
            observed = replay_units.mapped_control_comparison(
                target, negative["candidate"], data, negative["source"] / "units.map"
            )
            progress.validate_control(observed)
            self.assertEqual(observed["target_fixups"], [2])
            self.assertFalse(observed["raw_exact"])
            self.assertTrue(
                compare_mapped_unit(
                    target,
                    negative["candidate"],
                    negative["source"] / "units.map",
                    code,
                )["exact"]
            )
            self.assertNotIn("initialized_data_scope", rounds[0]["omfs"]["code"])
            self.assertNotIn(
                "map_scope",
                compare_mapped_unit(
                    target,
                    rounds[1]["candidate"],
                    rounds[1]["source"] / "units.map",
                    code,
                ),
            )
            snapshots = snapshot_paths(root, paths)
            validate_producer_inputs(root, rounds[0]["source"], data, snapshots)
            validate_producer_inputs(
                root, negative["source"], data, snapshots, mutation=mutation
            )
            bad = copy.deepcopy(result)
            bad["omfs"][0]["initialized_data_scope"]["ledata"].pop()
            with self.assertRaisesRegex(ValueError, "incomplete"):
                progress.validate_result(data, bad)
            # A changed linked DATA byte cannot be accepted by relabeling fields.
            tampered = copy.deepcopy(result)
            tampered["rounds"][0] = observed
            with self.assertRaises(ValueError):
                progress.validate_result(data, tampered)

            # Exercise the real importer against complete synthetic saved
            # artifacts. Only target/probe provenance is a fixture; MAP/MZ,
            # OMF, sources, wrapper, encoding and the negative are re-read.
            (root / "config").mkdir()
            lines = ['artifact = "th05-main"', "[[units]]"]
            lines += [key + " = " + json.dumps(value) for key, value in data.items()]
            lines += ["[[controls]]"] + [
                key + " = " + json.dumps(value) for key, value in mutation.items()
            ]
            manifest = "\n".join(lines) + "\n"
            (root / "config/exact_units.toml").write_text(manifest)
            (root / "exact-units.toml").write_text(manifest)
            (root / "config/toolchain.toml").write_text("# synthetic tool context\n")
            tool_sha = digest(root / "config/toolchain.toml")
            tool = {
                "ready": True,
                "identity_pass": True,
                "execution_pass": True,
                "manifest_sha256": tool_sha,
            }
            (root / "toolchain-attestation.json").write_text(json.dumps(tool))
            tool_receipt = digest(root / "toolchain-attestation.json")
            proof = {
                "manifest_sha256": tool_sha,
                "original_full_receipt_sha256": tool_receipt,
                "reused": True,
            }
            (root / "toolchain-reuse-proof.json").write_text(json.dumps(proof))
            target_sha = digest(rounds[0]["source"] / "units.exe")
            (root / "config/targets.toml").write_text(
                '[[artifacts]]\nid="th05-main"\nsha256="' + target_sha + '"\n'
            )
            for path in paths:
                destination = root / "inputs" / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((root / path).read_bytes())
            result.update(
                entry_sha256=entry_digest(data),
                source_inputs=snapshots,
                producer_paths=["a/source", "b/source"],
                compiler_arguments=[r["compiler_arguments"]["data"] for r in rounds],
                producer_source_inputs=[
                    producer_snapshot(r["source"], data, snapshots) for r in rounds
                ],
            )
            negative_record = {
                "unit_id": "data",
                "entry_sha256": entry_digest(data),
                "mutation": mutation,
                "control_sha256": entry_digest(mutation),
                "producer_path": "negative/source",
                "comparison": observed,
                "omf": negative["omfs"]["data"],
                "compiler_arguments": negative["compiler_arguments"]["data"],
                "producer_source_inputs": producer_snapshot(
                    negative["source"], data, snapshots
                ),
            }
            receipt = {
                "schema_version": 2,
                "kind": "bounded-cxx-unit-exact-replay",
                "pass": True,
                "manifest_sha256": digest(root / "exact-units.toml"),
                "target_sha256": target_sha,
                "toolchain_manifest_sha256": tool_sha,
                "toolchain_receipt_sha256": tool_receipt,
                "toolchain_reused": True,
                "toolchain_reuse_proof_sha256": digest(
                    root / "toolchain-reuse-proof.json"
                ),
                "source_inputs": snapshots,
                "results": [result],
                "compiled_negative_control": observed,
                "negative_control": negative_record,
                "complete_executable_exact": False,
            }
            receipt_path = root / "receipt.json"
            receipt_path.write_text(json.dumps(receipt))
            with patch.object(
                progress,
                "load_unit_target",
                return_value=({"sha256": target_sha}, target, None),
            ):
                progress.accept(receipt_path, root=root)
                summary = progress.summarize(root)
                self.assertEqual(
                    (
                        summary["functions"],
                        summary["authored_code_bytes"],
                        summary["authored_data_bytes"],
                        summary["authored_bytes"],
                    ),
                    (0, 0, 10, 10),
                )
                ledger_path = root / "config/accepted_units.json"
                ledger_before = ledger_path.read_bytes()
                positive_object = rounds[0]["source"] / "owner.obj"
                original_object = positive_object.read_bytes()
                positive_object.write_bytes(
                    object_bytes(bytes(4) + "終了".encode("cp932") + b"\0\1")
                )
                with self.assertRaisesRegex(ValueError, "compiler object disagrees"):
                    progress.accept(receipt_path, root=root)
                positive_object.write_bytes(original_object)
                # Restoring only the negative's source bytes cannot conceal a
                # positive linked DATA image substituted for that negative.
                negative_exe = negative["source"] / "units.exe"
                negative_exe.write_bytes(
                    (rounds[0]["source"] / "units.exe").read_bytes()
                )
                with self.assertRaisesRegex(ValueError, "negative artifact disagrees"):
                    progress.accept(receipt_path, root=root)
                self.assertEqual(ledger_path.read_bytes(), ledger_before)
            self.assertEqual(len(calls), 3)  # Import never starts another producer.

    def test_mixed_summary_and_gapless_inventory_keep_code_data_disjoint(self):
        code = {
            "id": "c",
            "size": 5,
            "functions": 1,
            "target_start": 0,
            "extent_kind": "code",
        }
        data = {
            "id": "d",
            "size": 10,
            "functions": 0,
            "target_start": 16,
            "extent_kind": "initialized-data",
            "origin": "compiler-generated-cxx",
            "data_semantics": ["ui-text"],
            "padding_bytes": [{"offset": 9, "value": 0}],
        }
        pieces = partition(40, [code, data])
        counts = {
            kind: sum(p["end"] - p["start"] for p in pieces if p["kind"] == kind)
            for kind in (
                "accepted-cxx-instructions",
                "accepted-cxx-initialized-data",
                "checked-uncredited-padding",
                "unknown",
            )
        }
        self.assertEqual(
            counts,
            {
                "accepted-cxx-instructions": 5,
                "accepted-cxx-initialized-data": 9,
                "checked-uncredited-padding": 1,
                "unknown": 25,
            },
        )

        def summary(unit):
            cl = progress.classify_extent(unit)
            cl.setdefault("authored_data_bytes", 0)
            cl.setdefault("authored_bytes", cl["authored_code_bytes"])
            return {
                **cl,
                "unit_count": 1,
                "functions": unit["functions"],
                "complete_extent_bytes": unit["size"],
                "units": [{**unit, **cl}],
                "percentage": None,
                "authored_denominator": None,
            }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config/exact_units.op.toml").touch()

            def mocked(root, *, artifact_name="main"):
                return summary(data if artifact_name == "op" else code)

            with patch.object(progress, "summarize", side_effect=mocked):
                combined = progress.summarize_all(root)
        self.assertEqual(
            (
                combined["functions"],
                combined["authored_code_bytes"],
                combined["authored_data_bytes"],
                combined["authored_bytes"],
            ),
            (1, 5, 9, 14),
        )
        self.assertIsNone(combined["percentage"])
        self.assertIsNone(combined["authored_denominator"])
        markdown, svg = progress.render(combined)
        self.assertIn("9 initialized DATA bytes", svg)
        self.assertIn("5 authored code bytes", svg)
        self.assertIn("| OP decoded C/C++ units | 1 | 9 | 9 | 10 |", markdown)


if __name__ == "__main__":
    unittest.main()
