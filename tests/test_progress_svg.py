"""The progress card renders valid SVG for full and empty summaries."""
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from progress import render_svg


class ProgressSvgTests(unittest.TestCase):
    def test_full_and_empty_summaries_render_valid_svg(self):
        full = {
            'functions': 5, 'instruction_bytes': 280, 'authored_code_bytes': 300,
            'code_data_bytes': 20, 'authored_data_bytes': 50,
            'authored_bytes': 350, 'complete_extent_bytes': 357, 'padding_bytes': 7,
            'artifacts': {
                'op': {'functions': 2, 'authored_code_bytes': 100, 'authored_data_bytes': 40},
                'main': {'functions': 3, 'authored_code_bytes': 200, 'authored_data_bytes': 10},
            },
        }
        empty = {'functions': 0, 'instruction_bytes': 0, 'complete_extent_bytes': 0}
        for summary in (full, empty):
            with self.subTest(functions=summary['functions']):
                svg = render_svg(summary)
                ET.fromstring(svg)
                self.assertNotIn('nan', svg)
                for name in ('OP.EXE', 'MAIN.EXE', 'MAINE.EXE', 'ZUN.COM'):
                    self.assertIn(name, svg)


if __name__ == '__main__':
    unittest.main()
