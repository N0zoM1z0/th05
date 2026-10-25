"""Whole-function scopes cannot skip bad neighbours or recompile one TU per unit."""
import copy
from pathlib import Path
import struct
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.unit_oracle import (compare_mapped_unit, function_scoped, map_publics,
                             map_unit, map_unit_scope)
import progress
import replay_units

MAP = """ 0000:0000 0010 C=CODE S=BG_TEXT G=MAIN_01 M=th05/bg.cpp ACBP=28
  Address         Publics by Name
 0000:0000       first()
 0000:0004 idle  blocked()
  Address         Publics by Value
 0000:0000 Abs   _address_0
 0000:0000       first()
 0000:0004 idle  blocked()
 0000:0008       third()
 0000:000C       last()
 0000:0020       foreign()

Program entry point at 0000:0000
"""


def image(*, changed=None, fixups=()):
    body = bytearray(b"\x90" * 16)
    if changed is not None:
        body[changed] = 0xCC
    header = struct.pack("<14H", 0x5A4D, 64, 1, len(fixups), 3,
                         1, 0xFFFF, 0, 16, 0, 0, 0, 28, 0)
    header += b"".join(struct.pack("<HH", offset, 0) for offset in fixups)
    return parse_mz(header.ljust(48, b"\0") + body)


def entry(symbol="first()", end="blocked()", *, size=4):
    result = {"id": symbol, "source": "src/bg.cpp", "module": "th05/bg.cpp",
              "segment": "BG_TEXT", "target_start": 0, "size": size,
              "functions": 1, "alignment_offsets": [], "function_symbol": symbol,
              "bindings_source": "probes/units/bg.asm", "wrapper_options": "-zPmain_01"}
    if end is not None:
        result["function_end_symbol"] = end
    return result


class FunctionScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.map = self.root / "units.map"
        self.map.write_text(MAP)

    def test_idle_next_function_is_a_boundary_even_when_not_registered(self):
        scope = map_unit_scope(self.map, entry())
        self.assertEqual((scope["start"], scope["size"]), (0, 4))
        self.assertEqual(scope["next_function_symbol"], "blocked()")
        self.assertEqual(map_unit(self.map, entry(end=None)), (0, 4))
        with self.assertRaisesRegex(ValueError, "actual next"):
            map_unit(self.map, entry(end="third()", size=8))

    def test_last_function_ends_at_real_contribution_not_foreign_public(self):
        scope = map_unit_scope(self.map, entry("last()", end=None))
        self.assertEqual((scope["start"], scope["size"]), (12, 4))
        self.assertEqual(scope["boundary_kind"], "contribution-end")
        with self.assertRaises(ValueError):
            map_unit(self.map, entry("last()", end="foreign()"))

    def test_wrong_module_outside_symbol_and_nonfunction_labels_rejected(self):
        for replacement in ({"module": "th05/other.cpp"}, {"function_symbol": "foreign()"},
                            {"function_symbol": "_address_0"}, {"functions": 2}):
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                map_unit(self.map, {**entry(), **replacement})
        self.map.write_text(MAP.replace("0000:0004 idle  blocked()", "0000:0004       _table"))
        with self.assertRaisesRegex(ValueError, "next MAP public"):
            map_unit(self.map, entry(end=None))

    def test_duplicate_and_aliased_publics_fail_closed(self):
        self.assertEqual(len(map_publics(self.map)), 5)
        self.map.write_text(MAP.replace(" 0000:0008       third()", " 0000:0000       alias()"))
        with self.assertRaisesRegex(ValueError, "aliased"):
            map_unit(self.map, entry())
        self.map.write_text(MAP.replace(" 0000:0008       third()", " 0000:0000       first()"))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            map_unit(self.map, entry())

    def test_whole_contribution_default_has_identical_comparison_shape(self):
        whole = {key: value for key, value in entry(size=16).items()
                 if key not in ("function_symbol", "function_end_symbol")}
        self.assertEqual(map_unit(self.map, whole), (0, 16))
        comparison = compare_mapped_unit(image(), image(), self.map, whole)
        self.assertNotIn("map_scope", comparison)
        self.assertTrue(comparison["exact"])
        with self.assertRaises(ValueError):
            function_scoped({**whole, "function_end_symbol": "blocked()"})

    def test_bad_unselected_function_does_not_grant_or_block_neighbour_credit(self):
        result = compare_mapped_unit(image(), image(changed=5), self.map, entry())
        self.assertTrue(result["exact"])
        self.assertEqual(result["size"], 4)
        self.assertEqual(result["map_scope"]["kind"], "complete-function")
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            compare_mapped_unit(image(), image(), self.map, entry(size=3))
        self.assertFalse(compare_mapped_unit(image(), image(changed=1), self.map, entry())["exact"])

    def test_ordered_fixups_and_relocation_word_boundaries_remain_strict(self):
        result = compare_mapped_unit(image(fixups=(0, 2)), image(fixups=(2, 0)), self.map, entry())
        self.assertTrue(result["raw_exact"])
        self.assertFalse(result["fixups_exact"])
        with self.assertRaisesRegex(ValueError, "splits"):
            compare_mapped_unit(image(fixups=(3,)), image(fixups=(3,)), self.map, entry())

    def test_accept_result_requires_scope_and_rejects_containment_or_boundary_drift(self):
        comparison = compare_mapped_unit(image(), image(), self.map, entry())
        omf = {"dependency_timestamp_normalized_sha256": "same",
               "translator_comments": ["TC86 Borland C++ 4.02"]}
        result = {"id": entry()["id"], "exact": True, "object_normalized_equal": True,
                  "rounds": [comparison, copy.deepcopy(comparison)], "omfs": [omf, omf]}
        progress.validate_result(entry(), result)
        for mutation in ({"start": 1}, {"contribution_size": 3}, {"boundary_kind": "contribution-end"},
                         {"next_function_symbol": "third()"}):
            invalid = copy.deepcopy(result)
            invalid["rounds"][0]["map_scope"].update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                progress.validate_result(entry(), invalid)
        invalid = copy.deepcopy(result)
        del invalid["rounds"][0]["map_scope"]
        with self.assertRaises(ValueError):
            progress.validate_result(entry(), invalid)

    def test_function_negative_control_uses_its_own_complete_scope(self):
        result = replay_units.mapped_control_comparison(image(), image(changed=1), entry(), self.map)
        self.assertFalse(result["raw_exact"])
        self.assertEqual(result["size"], 4)
        self.assertEqual(result["map_scope"]["next_function_symbol"], "blocked()")

    def test_render_does_not_call_a_function_unit_a_complete_contribution(self):
        markdown, _ = progress.render({"unit_count": 1, "functions": 1, "instruction_bytes": 4,
                                       "complete_extent_bytes": 4})
        self.assertIn("1 bounded C/C++ units pass", markdown)
        self.assertIn("Unaccepted functions in the same translation unit receive no credit", markdown)
        self.assertNotIn("1 complete C++ contributions", markdown)


class TranslationUnitTests(unittest.TestCase):
    def test_context_conflicts_fail_before_wrapper_overwrite(self):
        for replacement in ({"source": "src/other.cpp"}, {"wrapper_options": "-zPother"},
                            {"bindings_source": "probes/other.asm"}):
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ValueError, "conflicting"):
                replay_units.translation_units([entry(), {**entry("third()", "last()"), **replacement}])

    def test_many_function_units_compile_and_link_one_real_object_per_round(self):
        commands = []

        class FakeBuilder:
            def __init__(self, root, prefix, msdos):
                self.root, self.msdos, self.records = root, msdos, []

            def execute(self, label, command):
                commands.append(command)
                self.records.append({"output": label, "command": command})
                if label.endswith(".obj"):
                    (self.root / label).write_bytes(b"object")
                if label == "link":
                    (self.root / "units.exe").write_bytes(b"MZ")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "src/bg.cpp").write_text("int a() { return 1; }\n")
            (root / "probes/units").mkdir(parents=True)
            (root / "probes/units/bg.asm").write_text(".386\nend\n")
            units = [entry(), entry("third()", "last()"), entry("last()", None)]
            omf = {"valid": True, "sha256": "same", "dependency_timestamp_normalized_sha256": "same",
                   "module_name": "th05/bg.cpp", "translator_comments": ["TC86 Borland C++ 4.02"],
                   "dependency_paths": ["th05/bg.cpp", "src/bg.cpp"]}
            with patch.object(replay_units, "Builder", FakeBuilder), \
                 patch.object(replay_units, "describe_omf", return_value=omf), \
                 patch.object(replay_units, "parse_mz", return_value=SimpleNamespace(valid=True)):
                for label in ("a", "b"):
                    result = replay_units.cold_round(root / label, root, units,
                                                    paths={"src/bg.cpp", "probes/units/bg.asm"})
                    self.assertEqual(set(result["omfs"]), {unit["id"] for unit in units})
                    response = (root / label / "source/link.rsp").read_text()
                    self.assertEqual(response.count("bg.obj"), 1)
            compiles = [command for command in commands if "tcc" in command]
            self.assertEqual(len(compiles), 2)
            self.assertEqual(len([command for command in commands if "tlink" in command]), 2)


if __name__ == "__main__":
    unittest.main()
