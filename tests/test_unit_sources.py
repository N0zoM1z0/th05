"""Canonical readable Japanese must reach TC86 as explicitly verified CP932."""
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import replay_units
from lib.replay_toolchain import digest, include_closure
from lib.unit_sources import (encoded_input, producer_snapshot, source_encoding,
                              stage_inputs, validate_producer_inputs)


class UnitSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.cpp = '#include "src/shared.hpp"\nconst char *caption = "開始";\n'
        for name, text in {"src/a.cpp": self.cpp, "src/shared.hpp": "// 共通\n",
                           "probes/bindings.asm": ".386\nend\n"}.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode("utf-8"))
        self.entry = {"id": "jp", "source": "src/a.cpp", "module": "th05/a.cpp",
                      "source_encoding": "cp932", "bindings_source": "probes/bindings.asm"}
        self.paths = {"src/a.cpp", "src/shared.hpp", "probes/bindings.asm"}
        self.snapshots = [{"path": name, "sha256": digest(self.root / name)} for name in sorted(self.paths)]

    def test_fake_compiler_receives_positive_and_mutated_japanese_as_cp932(self):
        observed = []

        class FakeBuilder:
            def __init__(self, root, prefix, msdos):
                self.root, self.msdos, self.records = root, msdos, []

            def execute(self, label, command):
                if "tcc" in command:
                    observed.append(((self.root / "src/a.cpp").read_bytes(),
                                     (self.root / "src/shared.hpp").read_bytes()))
                    (self.root / label).write_bytes(b"object")
                if label == "link":
                    (self.root / "units.exe").write_bytes(b"candidate")

        omf = {key: "identity" for key in replay_units.OMF_FIELDS}
        omf.update(valid=True, translator_comments=["TC86 Borland C++ 4.02"])
        mutation = {"source": "src/a.cpp", "find": "開始", "replace": "終了"}
        with patch.object(replay_units, "Builder", FakeBuilder), patch.object(replay_units, "describe_omf", return_value=omf), \
             patch.object(replay_units, "parse_mz", return_value=SimpleNamespace(valid=True)):
            positive = replay_units.cold_round(self.root / "positive", self.root, [self.entry], paths=self.paths)
            negative = replay_units.cold_round(self.root / "negative", self.root, [self.entry], paths=self.paths, mutation=mutation)
        self.assertEqual(observed[0], (self.cpp.encode("cp932"), "// 共通\n".encode("cp932")))
        self.assertEqual(observed[1][0], self.cpp.replace("開始", "終了").encode("cp932"))
        validate_producer_inputs(self.root, positive["source"], self.entry, self.snapshots)
        validate_producer_inputs(self.root, negative["source"], self.entry, self.snapshots, mutation=mutation)
        actual = {row["path"]: row["sha256"] for row in producer_snapshot(positive["source"], self.entry, self.snapshots)}
        self.assertNotEqual(actual["src/a.cpp"], digest(self.root / "src/a.cpp"))
        self.assertEqual((self.root / "src/a.cpp").read_bytes(), self.cpp.encode("utf-8"))

    def test_raw_staging_preserves_original_bytes_including_utf8_and_crlf(self):
        raw = '// 日本語\r\nconst char *s = "開始";\r\n'.encode("utf-8")
        (self.root / "src/a.cpp").write_bytes(raw)
        entry = {key: value for key, value in self.entry.items() if key != "source_encoding"}
        stage_inputs(self.root, self.root / "raw", [entry], self.paths)
        self.assertEqual((self.root / "raw/src/a.cpp").read_bytes(), raw)
        self.assertEqual(source_encoding(entry), "raw")

    def test_incorrect_encoding_and_tampered_positive_or_negative_producer_are_rejected(self):
        stage_inputs(self.root, self.root / "positive", [self.entry], self.paths)
        source = self.root / "positive/src/a.cpp"
        source.write_bytes(self.cpp.encode("utf-8"))
        with self.assertRaisesRegex(ValueError, "staging"):
            validate_producer_inputs(self.root, self.root / "positive", self.entry, self.snapshots)
        mutation = {"source": "src/a.cpp", "find": "開始", "replace": "終了"}
        stage_inputs(self.root, self.root / "negative", [self.entry], self.paths, mutation=mutation)
        source = self.root / "negative/src/a.cpp"
        source.write_bytes(self.cpp.encode("cp932"))
        with self.assertRaisesRegex(ValueError, "staging"):
            validate_producer_inputs(self.root, self.root / "negative", self.entry, self.snapshots, mutation=mutation)
        with self.assertRaises(ValueError):
            source_encoding({"source_encoding": "utf-8"})

    def test_shared_japanese_header_rejects_mixed_encodings_but_ascii_is_identical(self):
        (self.root / "src/b.cpp").write_text('#include "src/shared.hpp"\nint b;\n')
        other = {**self.entry, "id": "raw", "source": "src/b.cpp", "module": "th05/b.cpp", "source_encoding": "raw"}
        paths = self.paths | {"src/b.cpp"}
        with self.assertRaisesRegex(ValueError, "shared compiler input"):
            stage_inputs(self.root, self.root / "conflict", [self.entry, other], paths)
        ascii_header = b"// ASCII shared header\r\n"
        (self.root / "src/shared.hpp").write_bytes(ascii_header)
        stage_inputs(self.root, self.root / "ascii", [self.entry, other], paths)
        self.assertEqual((self.root / "ascii/src/shared.hpp").read_bytes(), ascii_header)
        with self.assertRaisesRegex(ValueError, "conflicting"):
            replay_units.translation_units([self.entry, {**self.entry, "source_encoding": "raw"}])

    def test_unencodable_text_and_nonunique_mutation_fail_without_silent_replacement(self):
        with self.assertRaises(UnicodeEncodeError):
            encoded_input("😀".encode(), "cp932", path="src/a.cpp")
        with self.assertRaisesRegex(ValueError, "anchor drifted"):
            encoded_input("開始 開始".encode(), "cp932", path="src/a.cpp",
                          mutation={"source": "src/a.cpp", "find": "開始", "replace": "終了"})

    def test_actual_assembled_binding_alias_is_checked_even_with_canonical_copy(self):
        producer = self.root / "producer"
        stage_inputs(self.root, producer, [self.entry], self.paths)
        canonical_binding = producer / self.entry["bindings_source"]
        alias = producer / "bindings.asm"
        alias.write_bytes(canonical_binding.read_bytes() + b"; tampered active input\n")
        with self.assertRaisesRegex(ValueError, "assembled bindings.asm alias"):
            validate_producer_inputs(self.root, producer, self.entry, self.snapshots)
        alias.write_bytes(canonical_binding.read_bytes())
        canonical_binding.unlink()
        validate_producer_inputs(self.root, producer, self.entry, self.snapshots)


if __name__ == "__main__":
    unittest.main()
