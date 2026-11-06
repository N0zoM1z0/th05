"""The progress card compares accepted bytes without inventing a denominator."""
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from progress import render_svg


class ProgressSvgTests(unittest.TestCase):
    def test_columns_use_separate_shared_scales_and_keep_padding_out(self):
        summary = {
            'functions': 5, 'instruction_bytes': 280, 'authored_code_bytes': 300,
            'code_data_bytes': 20, 'authored_data_bytes': 50,
            'authored_bytes': 350, 'complete_extent_bytes': 357, 'padding_bytes': 7,
            'artifacts': {
                'op': {'functions': 2, 'authored_code_bytes': 100, 'authored_data_bytes': 40},
                'main': {'functions': 3, 'authored_code_bytes': 200, 'authored_data_bytes': 10},
            },
        }
        svg = render_svg(summary)
        root = ET.fromstring(svg)
        self.assertEqual((root.get('width'), root.get('height')), ('788', '440'))
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        bars = [r for r in root.findall('.//svg:rect', ns)
                if r.get('fill') in ('#9b6de3', '#55c7a6')]
        self.assertEqual([r.get('width') for r in bars],
                         ['141.00', '282.00', '282.00', '70.50',
                          '0.00', '0.00', '0.00', '0.00'])
        self.assertIn('Accepted authored C/C++ bytes only', svg)
        self.assertIn('350 B · 5 functions', svg)
        self.assertIn('7 padding bytes earn no credit', svg)
        self.assertIn('not completion percentages', svg)
        self.assertIn('global authored-byte denominator: n/a', svg)

    def test_empty_columns_and_single_artifact_fallback_are_valid(self):
        summary = {'functions': 0, 'instruction_bytes': 0, 'complete_extent_bytes': 0}
        svg = render_svg(summary)
        ET.fromstring(svg)
        self.assertNotIn('nan', svg)
        self.assertIn('scale 0–0 B', svg)
        for name in ('OP.EXE', 'MAIN.EXE', 'MAINE.EXE', 'ZUN.COM'):
            self.assertIn(name, svg)


if __name__ == '__main__':
    unittest.main()
