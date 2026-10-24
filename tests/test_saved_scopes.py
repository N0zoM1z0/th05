"""Retained-producer review cannot change code, boundaries, context or control."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import review_saved_scopes as review
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext


def executable(*, negative=False, reverse=True):
    header = struct.pack("<14H", 0x5A4D, 64, 1, 2, 3, 1, 0xFFFF, 0, 16, 0, 0, 0, 28, 0)
    header += b"".join(struct.pack("<HH", offset, 0) for offset in ((10, 2) if reverse else (2, 10)))
    body = bytearray(16)
    body[9] = int(negative)
    return header.ljust(48, b"\0") + body


def manifest(config):
    lines = [f'artifact = "{config["artifact"]}"']
    for table in ("units", "controls"):
        for row in config.get(table, []):
            lines.append("[[" + table + "]]")
            lines.extend(key + " = " + json.dumps(value) for key, value in row.items())
    return "\n".join(lines) + "\n"


class SavedScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.work = self.root / ".analysis/review"
        self.parent = self.work / "parent"
        self.parent.mkdir(parents=True)
        self.entry = {"id": "whole", "source": "src/a.cpp", "module": "th05/a.cpp",
                      "segment": "A_TEXT", "target_start": 0, "size": 16, "functions": 4,
                      "bindings_source": "probes/bindings.asm"}
        self.first = {**self.entry, "id": "first", "size": 4, "functions": 1,
                      "function_symbol": "first()", "function_end_symbol": "middle()"}
        self.third = {**self.entry, "id": "third", "target_start": 8, "size": 4, "functions": 1,
                      "function_symbol": "third()", "function_end_symbol": "last()"}
        self.mutation = {"unit": "whole", "source": "src/a.cpp", "find": "value = 8", "replace": "value = 7"}
        self.config = {"artifact": "th05-main", "units": [self.first, self.third],
                       "controls": [{**self.mutation, "unit": "third"}]}
        self.parent_result = {"id": "whole", "object_normalized_equal": True,
            "rounds": [{"raw_exact": True, "candidate_start": 0}, {"raw_exact": True, "candidate_start": 0}],
            "omfs": [{"sha256": "original-a"}, {"sha256": "original-b"}],
            "source_inputs": [], "producer_paths": ["a/source", "b/source"]}
        parent = {"schema_version": 2, "kind": review.PARENT_KIND, "pass": False,
                  "results": [self.parent_result], "negative_control": {"unit_id": "whole", "mutation": self.mutation,
                  "producer_path": "negative/source", "omf": {"sha256": "original-negative"}},
                  "target_sha256": "target", "toolchain_receipt_sha256": "full-report",
                  "toolchain_manifest_sha256": "toolchain", "toolchain_reused": True,
                  "toolchain_reuse_proof_sha256": "static-proof", "source_inputs": []}
        (self.parent / "receipt.json").write_text(json.dumps(parent))
        (self.parent / "exact-units.toml").write_text(manifest({"artifact": "th05-main", "units": [self.entry]}))
        self.write_config()
        for label in ("a", "b", "negative"):
            source = self.parent / label / "source"
            source.mkdir(parents=True)
            (source / "units.exe").write_bytes(executable(negative=label == "negative"))
            (source / "a.obj").write_bytes(b"retained opaque object identity")
            (source / "units.map").write_text(" 0000:0000 0010 C=CODE S=A_TEXT G=GROUP M=th05/a.cpp\n"
                " Address Publics by Value\n 0000:0000 first()\n 0000:0004 middle()\n"
                " 0000:0008 third()\n 0000:000C last()\nProgram entry point at 0000:0000\n")
        self.loader = patch.object(review, "load_unit_target", return_value=(
            {"sha256": "target"}, parse_mz(executable(reverse=False)), None))
        self.loader.start()
        self.addCleanup(self.loader.stop)

    def write_config(self):
        (self.work / "exact-units.toml").write_text(manifest(self.config))

    def derive(self):
        self.write_config()
        return review.derive_review(self.root, self.work, self.config, [row["id"] for row in self.config["units"]])

    def test_review_uses_old_two_producers_and_unique_natural_control_without_recompile(self):
        original = (self.parent / "receipt.json").read_bytes()
        receipt = self.derive()
        self.assertEqual(receipt["kind"], review.KIND)
        self.assertEqual(receipt["compiler_invocations"], 0)
        self.assertTrue(receipt["pass"])
        self.assertFalse(receipt["parent_aggregate_pass"])
        self.assertEqual(receipt["results"][0]["producer_paths"], ["parent/a/source", "parent/b/source"])
        self.assertEqual(receipt["results"][0]["omfs"], self.parent_result["omfs"])
        self.assertEqual(receipt["negative_control"]["unit_id"], "third")
        self.assertEqual(receipt["negative_control"]["comparison"]["size"], 4)
        self.assertEqual((self.parent / "receipt.json").read_bytes(), original)

    def test_multiple_contributions_can_retain_the_unchanged_real_control_owner(self):
        first_parent = {**self.entry, "size": 8, "functions": 2}
        control_parent = {**self.entry, "id": "control-whole", "segment": "B_TEXT",
                          "target_start": 8, "size": 8, "functions": 2}
        parent = json.loads((self.parent / "receipt.json").read_text())
        second_result = copy.deepcopy(self.parent_result)
        second_result["id"] = "control-whole"
        for row in second_result["rounds"]:
            row["candidate_start"] = 8
        parent["results"].append(second_result)
        parent["negative_control"]["unit_id"] = "control-whole"
        parent["negative_control"]["mutation"]["unit"] = "control-whole"
        (self.parent / "receipt.json").write_text(json.dumps(parent))
        (self.parent / "exact-units.toml").write_text(manifest({
            "artifact": "th05-main", "units": [first_parent, control_parent]}))
        self.config["units"] = [self.first, control_parent]
        self.config["controls"] = [{**self.mutation, "unit": "control-whole"}]
        for label in ("a", "b", "negative"):
            path = self.parent / label / "source/units.map"
            path.write_text(path.read_text().replace("0010 C=CODE", "0008 C=CODE").replace(
                " Address Publics by Value", " 0000:0008 0008 C=CODE S=B_TEXT G=GROUP M=th05/a.cpp\n Address Publics by Value"))
        receipt = self.derive()
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["compiler_invocations"], 0)
        self.assertEqual([row["id"] for row in receipt["results"]], ["first", "control-whole"])
        self.assertEqual(receipt["negative_control"]["unit_id"], "control-whole")
        self.assertEqual(receipt["negative_control"]["entry_sha256"], review.entry_digest(control_parent))

    def test_a_retained_whole_control_cannot_be_changed_or_overlap_a_new_scope(self):
        context = UnitContext(self.root)
        review.check_scope_entries(self.entry, [self.entry], context, retained_control="whole")
        with self.assertRaises(ValueError):
            review.check_scope_entries(self.entry, [{**self.entry, "functions": 3}], context,
                                       retained_control="whole")
        with self.assertRaisesRegex(ValueError, "overlap"):
            review.check_scope_entries(self.entry, [self.entry, self.first], context,
                                       retained_control="whole")

    def test_context_changes_bounds_overlap_and_classification_are_rejected(self):
        context = UnitContext(self.root)
        for replacement in ({"source": "src/other.cpp"}, {"module": "th05/other.cpp"}, {"binary": "O"},
                            {"source_encoding": "cp932"}, {"wrapper_options": "-zPother"},
                            {"target_start": 15}, {"padding_bytes": [{"offset": 0, "value": 0}]}):
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                review.check_scope_entries(self.entry, [{**self.first, **replacement}], context)
        with self.assertRaisesRegex(ValueError, "overlap"):
            review.check_scope_entries(self.entry, [self.first, {**self.third, "target_start": 0}], context)

    def test_mechanically_wrong_target_offset_cannot_relabel_a_real_map_function(self):
        self.config["units"][0] = {**self.first, "target_start": 1}
        with self.assertRaisesRegex(ValueError, "relative scope"):
            self.derive()

    def test_missing_or_changed_negative_owner_cannot_be_inherited(self):
        self.config["units"] = [self.first]
        with self.assertRaisesRegex(ValueError, "mutation owner"):
            self.derive()
        self.config["units"] = [self.first, self.third]
        self.config["controls"][0]["replace"] = "value = 6"
        with self.assertRaisesRegex(ValueError, "identical parent mutation"):
            self.derive()

    def test_archive_tampering_and_synthetic_producer_relabel_are_rejected(self):
        receipt = self.derive()
        path = self.work / "receipt.json"
        path.write_text(json.dumps(receipt))
        validate_parent = Mock()
        review.validate_review(path, root=self.root, artifact_name="main", validate_parent=validate_parent)
        validate_parent.assert_called_once_with(self.parent / "receipt.json")
        forged = copy.deepcopy(receipt)
        forged["results"][0]["producer_paths"] = ["new/a/source", "new/b/source"]
        path.write_text(json.dumps(forged))
        with self.assertRaisesRegex(ValueError, "mechanical projection"):
            review.validate_review(path, root=self.root, artifact_name="main", validate_parent=Mock())
        path.write_text(json.dumps(receipt))
        (self.parent / "a/source/a.obj").write_bytes(b"changed object")
        with self.assertRaisesRegex(ValueError, "archive was changed"):
            review.validate_review(path, root=self.root, artifact_name="main", validate_parent=Mock())

    def test_review_of_review_parent_and_inexact_selected_function_are_rejected(self):
        parent_path = self.parent / "receipt.json"
        parent = json.loads(parent_path.read_text())
        parent["kind"] = review.KIND
        parent_path.write_text(json.dumps(parent))
        with self.assertRaisesRegex(ValueError, "original bounded"):
            self.derive()
        parent["kind"] = review.PARENT_KIND
        parent_path.write_text(json.dumps(parent))
        (self.parent / "a/source/units.exe").write_bytes(executable(negative=True))
        with self.assertRaisesRegex(ValueError, "not raw/ordered-fixup exact"):
            self.derive()


if __name__ == "__main__":
    unittest.main()
