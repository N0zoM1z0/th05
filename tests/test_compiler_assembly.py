"""Compiler-to-assembler provenance and context guards; no game behavior model."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib import compiler_assembly as recipe
from lib.replay_toolchain import snapshot_paths


class CompilerAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.entry = {"id": "sample", "source": "src/a.cpp", "module": "th05/a.cpp",
                      "segment": "A_TEXT", "group": "main_03", "cs_base": 16,
                      "ds_base": 32, "target_start": 16, "size": 4,
                      "functions": 1, "origin": "compiler-generated-cxx",
                      "compiler_pipeline": recipe.PIPELINE,
                      "bindings_source": "probes/units/bindings.asm"}

    def debug(self, name):
        body = b"\xe9" + bytes(4) + bytes([len(name)]) + name.encode("ascii")
        return body.hex().upper()

    def test_actual_cpp_dependencies_decode_continuations_and_ignore_system_headers(self):
        record = self.debug("src/a.cpp")
        text = ("?debug C " + self.debug("th05/a.cpp") + "\n?debug C " + record[:12]
                + "+\n?debug C " + record[12:] + "\n?debug C "
                + self.debug(r"C:\TC4\INCLUDE\stddef.h") + "\n?debug C E9\n")
        self.assertEqual(recipe.compiler_dependencies(text.encode(), self.entry), ["src/a.cpp"])
        with self.assertRaisesRegex(ValueError, "wrapper"):
            recipe.compiler_dependencies(("?debug C " + record).encode(), self.entry)
        with self.assertRaisesRegex(ValueError, "truncated"):
            recipe.compiler_dependencies(b"?debug C E900+\n", self.entry)

    def test_wrapper_adds_only_missing_bound_foreign_code_segments(self):
        generated = b".386p\nA_TEXT segment byte public use16 'CODE'\nA_TEXT ends\nmain_03 group A_TEXT,FOREIGN\nDGROUP group _DATA\n_DATA segment word public use16 'DATA'\n_DATA ends\nend\n"
        binder = b"FOREIGN segment byte public 'CODE' use16\norg 32\nFOREIGN ends\nmain_03 group FOREIGN,A_TEXT\n"
        wrapper = recipe.assembly_wrapper(generated, binder, "a.asm")
        self.assertEqual(wrapper, b".386p\nFOREIGN segment byte public use16 'CODE'\nFOREIGN ends\ninclude a.asm\n")
        self.assertNotIn(b"org", wrapper)
        with self.assertRaisesRegex(ValueError, "foreign CODE"):
            recipe.assembly_wrapper(generated, binder.replace(b"'CODE'", b"'DATA'"), "a.asm")
        with self.assertRaisesRegex(ValueError, "foreign CODE"):
            recipe.assembly_wrapper(generated, binder.replace(b"main_03 group", b"main_01 group"), "a.asm")

    def stage(self):
        return {"compiler_dependencies": ["src/a.cpp"],
                **{key: "0" * 64 for key in ("compiler_generated_assembly_sha256",
                   "assembly_after_tasm_sha256", "map_sha256", "mz_sha256", "wrapper_sha256", "commands_sha256")},
                "owned_CODE": {"size": 4, "segment": "A_TEXT"},
                "comparison": {"exact": True}, "omf": {"translator_comments": recipe.TRANSLATOR}}

    def result(self):
        stages = [self.stage(), self.stage()]
        return {"compiler_assembly": stages, "compiler_arguments": [recipe.arguments(self.entry)] * 2,
                "rounds": [stage["comparison"] for stage in stages],
                "omfs": [stage["omf"] for stage in stages]}

    def test_two_stage_identity_rejects_edited_or_missing_compiler_output(self):
        result = self.result()
        recipe.validate_result_metadata(self.entry, result)
        changed = copy.deepcopy(result)
        changed["compiler_assembly"][1]["assembly_after_tasm_sha256"] = "1" * 64
        with self.assertRaisesRegex(ValueError, "lineage|witnesses"):
            recipe.validate_result_metadata(self.entry, changed)
        del changed["compiler_assembly"][1]["compiler_generated_assembly_sha256"]
        with self.assertRaisesRegex(ValueError, "lineage|witnesses"):
            recipe.validate_result_metadata(self.entry, changed)

    def test_pipeline_scope_freezes_real_cpp_inputs_binder_and_recipe_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = {"src/a.cpp": "int a() { return 1; }\n",
                     "probes/units/bindings.asm": ".386\nend\n", "unrelated.txt": "untouched\n"}
            files.update({name: "# recipe fixture\n" for name in recipe.PRODUCER_FILES})
            for name, text in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
            required = recipe.required_paths(root, self.entry, ["src/a.cpp"])
            snapshots = snapshot_paths(root, required)
            self.assertEqual(recipe.scoped_snapshot(root, self.entry, self.result(), snapshots), snapshots)
            self.assertNotIn("unrelated.txt", required)
            with self.assertRaisesRegex(ValueError, "incomplete"):
                recipe.scoped_snapshot(root, self.entry, self.result(), snapshots[:-1])

    def test_new_recipe_is_explicit_and_does_not_change_direct_default(self):
        self.assertTrue(recipe.enabled(self.entry))
        self.assertFalse(recipe.enabled({}))
        self.assertEqual(recipe.arguments(self.entry)[0], "-S")
        with self.assertRaisesRegex(ValueError, "unsupported"):
            recipe.enabled({"compiler_pipeline": "other"})
        changed = {**self.entry, "source": "src/a.asm"}
        with self.assertRaisesRegex(ValueError, r"C/C\+\+"):
            recipe.validate_entry(changed)

    def test_positive_builds_cannot_alias_the_same_saved_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("a", "b", "negative"):
                (root / name / "source").mkdir(parents=True)
            self.assertEqual(len(recipe.producer_directories(root)), 3)
            (root / "b/source").rmdir()
            (root / "b/source").symlink_to(root / "a/source", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "independent"):
                recipe.producer_directories(root)


if __name__ == "__main__":
    unittest.main()
