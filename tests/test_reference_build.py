"""The bounded build planner must preserve flags and link input order."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.reference_build import rules_from_batch


class BuildPlanTests(unittest.TestCase):
    def test_cxx_flags_and_continued_response(self):
        rules = rules_from_batch("\n".join([
            "echo -c -ml -DGAME=5 -nobj/th05/ th05/foo.cpp>obj\\batch.@c",
            "echo th05/bar.cpp>>obj\\batch.@c", "tcc @obj/batch.@c",
            "echo -c -s c0l.obj obj\\th05\\foo.obj+>obj\\th05\\main.@l",
            "echo obj\\th05\\bar.obj, bin\\th05\\main.exe, obj\\th05\\main.map, cl.lib>>obj\\th05\\main.@l",
            "tlink @obj\\th05\\main.@l"]))
        self.assertEqual(rules["obj/th05/foo.obj"].arguments[-1], "th05/foo.cpp")
        self.assertIn("-DGAME=5", rules["obj/th05/bar.obj"].arguments)
        self.assertEqual(rules["bin/th05/main.exe"].dependencies,
                         ("obj/th05/foo.obj", "obj/th05/bar.obj"))


if __name__ == "__main__":
    unittest.main()
