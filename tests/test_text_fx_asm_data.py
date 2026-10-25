"""ASM ownership gates must reject assets, partial extents and false negatives."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import tomllib
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from replay_text_fx_data import CONFIG, PUBLIC, asm_scopes, check_public, map_scope, mutate


def record(kind, data):
    body = bytes([kind]) + struct.pack("<H", len(data) + 1) + data
    return body + bytes([-sum(body) & 255])


def fixture(*, partial=False, overlap=False, asset=False, extra=b"", producer="Turbo Assembler  Version 5.0"):
    names = ["_DATA", "DATA", "TEXT_FX_STATE_DATA", "", "MASK_RESOURCE"]
    encoded = b"".join(bytes([len(n)]) + n.encode() for n in names)
    out = record(0x80, b"\x07fixture")
    out += record(0x88, b"\0\0" + bytes([len(producer)]) + producer.encode())
    out += record(0x96, encoded)
    out += record(0x98, b"\x48\x1c\0\1\2\4")
    out += record(0x98, b"\x48\x04\0\3\2\4")
    if asset:
        out += record(0x98, b"\x48\x20\0\5\2\4")
    out += record(0xA0, b"\1\0\0" + b"AB" * (13 if partial else 14))
    out += record(0xA0, b"\2\0\0CDCD")
    if overlap:
        out += record(0xA0, b"\1\0\0AA")
    return out + extra + record(0x8A, b"\0")


class TextFxAsmDataTests(unittest.TestCase):
    def test_only_complete_assembler_data_contributions(self):
        scopes = asm_scopes(fixture())
        self.assertEqual({k: v["size"] for k, v in scopes.items()}, {"dispatch": 28, "state": 4})
        for kwargs in ({"partial": True}, {"overlap": True}, {"asset": True},
                       {"producer": "TC86 Borland C++ 4.02"},
                       {"extra": record(0x9C, b"\0")}, {"extra": record(0xA2, b"\0")}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                asm_scopes(fixture(**kwargs))

    def test_omf_checksum_cannot_be_ignored(self):
        data = bytearray(fixture())
        data[10] ^= 1
        with self.assertRaises(ValueError):
            asm_scopes(bytes(data))

    def test_map_requires_actual_module_class_group_and_frame(self):
        line = " 0EFE:09A2 001C C=DATA S=_DATA G=DGROUP M=tfxdata.asm ACBP=48\n"
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "units.map"
            path.write_text(line)
            self.assertEqual(map_scope(path, "_DATA", 0xEFE), (0xF982, 28))
            for value in (line * 2, line.replace("tfxdata.asm", "bindings.asm"),
                          line.replace("C=DATA", "C=BSS"), line.replace("DGROUP", "OTHER"),
                          line.replace("0EFE:", "0EFF:")):
                path.write_text(value)
                with self.subTest(value=value), self.assertRaises(ValueError):
                    map_scope(path, "_DATA", 0xEFE)

    def test_negative_mutation_has_one_semantic_anchor(self):
        data = b"_graph_putsa_fx_spacing dw 16\n"
        self.assertEqual(mutate(data, "state"), b"_graph_putsa_fx_spacing dw 17\n")
        for bad in (b"", data * 2):
            with self.assertRaises(ValueError):
                mutate(bad, "state")

    def test_accepted_report_cannot_claim_cxx_or_global_credit(self):
        config = tomllib.loads(CONFIG.read_text())
        report = json.loads(PUBLIC.read_text())
        check_public(report, config)
        for patch in ({"cxx_authored_credit": 64}, {"global_authored_credit": 64},
                      {"origin": "compiler-generated-cxx-semantic-data"},
                      {"asm_data_bytes_exact": 128}, {"complete_executable_exact": True}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                check_public({**report, **patch}, config)

    def test_accepted_report_rejects_wrong_extent_or_non_data_negative(self):
        config = tomllib.loads(CONFIG.read_text())
        report = json.loads(PUBLIC.read_text())
        for category, field, value in (("rounds", "size", 27), ("rounds", "raw_exact", False),
                                       ("rounds", "candidate_fixups", [2]),
                                       ("negative_controls", "raw_exact", True),
                                       ("negative_controls", "fixups_exact", False)):
            bad = copy.deepcopy(report)
            profile = bad["profiles"]["op"]
            observation = profile[category][0] if category == "rounds" else profile[category]["dispatch"]
            observation["comparisons"]["dispatch"][field] = value
            with self.subTest(category=category, field=field), self.assertRaises(ValueError):
                check_public(bad, config)


if __name__ == "__main__":
    unittest.main()
