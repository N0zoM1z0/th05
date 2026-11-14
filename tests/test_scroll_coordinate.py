"""Behavior model for the exact 16-bit near-Pascal scroll-coordinate leaf."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "src/main/scroll/coordinates.cpp").read_text()
HEADER = (ROOT / "src/main/scroll/coordinates.hpp").read_text()
SMALL = (ROOT / "src/main/runtime/small.hpp").read_text()


def signed16(value):
    value &= 0xFFFF
    return value - 0x10000 if value & 0x8000 else value


def scroll_subpixel_y_to_vram_seg1(y, scroll_active, scroll_line):
    """Model the AX/SAR/one-correction sequence, not a modulo operation."""
    ax = signed16(y)
    ax = signed16(ax >> 4)  # Original signed SAR AX, 4.
    if scroll_active:
        ax = signed16(ax + signed16(scroll_line))
    if ax < 0:
        ax = signed16(ax + 400)
    elif ax >= 400:
        ax = signed16(ax - 400)
    return signed16(ax)


class ScrollCoordinateTests(unittest.TestCase):
    def test_signed_subpixel_shift_and_negative_boundary(self):
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(15, False, 123), 0)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(16, False, 123), 1)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(-1, False, 123), 399)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(-16, False, 123), 399)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(-6400, False, 123), 0)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(-6416, False, 123), -1)

    def test_scroll_origin_is_added_before_the_single_wrap(self):
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(16, True, -2), 399)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(16, True, 400), 1)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(16, False, 400), 1)

    def test_correction_is_exactly_one_step_not_full_modulo(self):
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(6400, False, 0), 0)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(12800, False, 0), 400)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(-12800, False, 0), -400)
        self.assertEqual(scroll_subpixel_y_to_vram_seg1(16, True, 800), 401)

    def test_source_preserves_the_real_pascal_stack_word_and_signed_ax(self):
        self.assertIn("_BX = _SP;", SOURCE)
        self.assertIn("_AX = static_cast<int>(peek(_SS, (_BX + 2)));", SOURCE)
        self.assertIn("_AX = static_cast<short>(_AX) >> 4;", SOURCE)
        self.assertIn("if(scroll_active)", SOURCE)
        self.assertIn("if(static_cast<short>(_AX) < 0)", SOURCE)
        self.assertIn("else if(static_cast<short>(_AX) >= SCROLL_RING_HEIGHT)", SOURCE)
        self.assertIn("return _AX;", SOURCE)
        self.assertNotIn("__asm", SOURCE)
        self.assertIn('extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg1', HEADER)
        self.assertIn("small_scroll_line_is_2", SMALL)
        self.assertIn("small_scroll_flag_is_1", SMALL)


if __name__ == "__main__":
    unittest.main()
