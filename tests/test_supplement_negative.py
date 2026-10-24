"""A failed/stale retained replay cannot authorize even a negative compilation."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import supplement_negative


class SupplementalNegativeTests(unittest.TestCase):
    def test_failed_or_stale_parent_stops_before_tools_and_output_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / ".analysis/parent/receipt.json"
            parent.parent.mkdir(parents=True)
            parent.write_text("{}")
            output = root / ".analysis/new-control"
            for rejected in (False, "stale"):
                with self.subTest(parent=rejected), \
                     patch.object(supplement_negative.progress, "accept") as validate, \
                     patch.object(supplement_negative, "freeze_toolchain") as tools, \
                     patch.object(supplement_negative, "cold_round") as compiler:
                    if rejected == "stale":
                        validate.side_effect = ValueError("saved source identity changed")
                    else:
                        validate.return_value = {"kind": "bounded-cxx-unit-exact-replay", "pass": False}
                    with self.assertRaises(ValueError):
                        supplement_negative.build(parent, "owner", output, root=root)
                    tools.assert_not_called()
                    compiler.assert_not_called()
                    self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
