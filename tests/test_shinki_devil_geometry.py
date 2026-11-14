"""Shinki Devil's four columns, mirrored laser angles and turn clock."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEVIL = (ROOT / "src/main/boss/shinki/devil.inl").read_text()
BALLISTICS = (ROOT / "src/main/boss/shinki/devil_ballistics.hpp").read_text()
SHINKI_HPP = (ROOT / "src/main/boss/shinki/shinki.hpp").read_text()


def define_int(name, source):
    match = re.search(rf"#define {name}\s+(0[xX][0-9A-Fa-f]+|[0-9]+)", source)
    if not match:
        raise AssertionError(f"missing macro {name}")
    return int(match.group(1), 0)


def const_int(name, source):
    match = re.search(rf"{name}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)", source)
    if not match:
        raise AssertionError(f"missing constant {name}")
    return int(match.group(1), 0)


def devil_const(name):
    return const_int(name, DEVIL)


def laser_turns(count):
    outer = define_int("SHINKI_DEVIL_LASER_INITIAL_ANGLE", BALLISTICS)
    inner = outer
    direction = "clockwise"
    result = []
    for _ in range(count):
        # The source writes A/B first, then derives C/D from those fresh angles.
        result.append((outer, inner, (0x80 - inner) & 0xFF, (0x80 - outer) & 0xFF))
        if direction == "clockwise":
            outer = (outer + 1) & 0xFF
            inner = (inner - 1) & 0xFF
            if inner == devil_const("DEVIL_LASER_INNER_LOW"):
                direction = "counterclockwise"
        else:
            outer = (outer - 1) & 0xFF
            inner = (inner + 1) & 0xFF
            if inner == devil_const("DEVIL_LASER_INNER_HIGH"):
                direction = "clockwise"
    return result, (outer, inner, direction)


class ShinkiDevilGeometryTests(unittest.TestCase):
    def test_four_laser_origins_and_bullet_origins_are_the_same_symmetric_columns(self):
        wing_width = const_int("SHINKI_WING_W", SHINKI_HPP)
        column_count = devil_const("COLUMN_COUNT")
        column_width = wing_width // 4
        first_offset = wing_width // 2 - wing_width // 8
        self.assertIn("(SHINKI_WING_W / 2) - (SHINKI_WING_W / 8)", DEVIL)
        self.assertEqual((wing_width, column_count, column_width, first_offset), (256, 4, 64, 96))
        offsets = [first_offset - i * column_width for i in range(column_count)]
        self.assertEqual(offsets, [96, 32, -32, -96])
        self.assertEqual(offsets, [-x for x in reversed(offsets)])

        setup_start = DEVIL.index("// Laser activation")
        setup_end = DEVIL.index("// Spread bullets", setup_start)
        setup = DEVIL[setup_start:setup_end]
        self.assertIn("laser_template.coords.origin.x.v += to_sp(SHINKI_TO_LAST_COLUMN_DISTANCE);", setup)
        self.assertEqual(setup.count("laser_manual_fixed_spawn("), 1)
        self.assertIn("DEVIL_NEXT_FIXED_LASER(SHINKI_DEVIL_LASER_SLOT_B);", setup)
        self.assertIn("DEVIL_NEXT_FIXED_LASER(SHINKI_DEVIL_LASER_SLOT_C);", setup)
        self.assertIn("DEVIL_NEXT_FIXED_LASER(SHINKI_DEVIL_LASER_SLOT_D);", setup)
        self.assertIn("laser_template.coords.width.nonshrink = SHINKI_DEVIL_LASER_WIDTH_PX;", setup)
        self.assertIn("laser_template.coords.angle = SHINKI_DEVIL_LASER_INITIAL_ANGLE;", setup)
        self.assertIn("laser_template.col = SHINKI_DEVIL_LASER_COLOR;", setup)
        self.assertEqual(define_int("SHINKI_DEVIL_LASER_WIDTH_PX", BALLISTICS), 6)
        self.assertEqual(define_int("SHINKI_DEVIL_LASER_COLOR", BALLISTICS), 14)

        next_laser = re.search(r"#define DEVIL_NEXT_FIXED_LASER\(slot\)(.*?)\n\t}", DEVIL, re.S)
        self.assertIsNotNone(next_laser)
        self.assertIn("laser_template.coords.origin.x.v -= to_sp(COLUMN_W);", next_laser.group(1))
        self.assertIn("laser_manual_fixed_spawn(slot);", next_laser.group(1))

    def test_red_and_decorative_spreads_walk_right_to_left_with_mirrored_angles(self):
        spread_start = DEVIL.index("// Spread bullets")
        laser_start = DEVIL.index("// Lasers", spread_start)
        spread = DEVIL[spread_start:laser_start]
        red_start = spread.index("bullet_template.origin.x.v += to_sp(SHINKI_TO_LAST_COLUMN_DISTANCE);")
        red_end = spread.index("if(!bullet_intro_done)", red_start)
        red = spread[red_start:red_end]
        self.assertIn("DEVIL_FIRE_COL(bullet_angle_outer);", red)
        self.assertIn("DEVIL_NEXT_FIRE_COL(bullet_angle_inner);", red)
        self.assertIn("DEVIL_NEXT_FIRE_COL(SHINKI_DEVIL_MIRROR_ANGLE - bullet_angle_inner);", red)
        self.assertIn("DEVIL_NEXT_FIRE_COL(SHINKI_DEVIL_MIRROR_ANGLE - bullet_angle_outer);", red)
        self.assertEqual(red.count("DEVIL_NEXT_FIRE_COL("), 3)

        decorative_start = spread.index('// "Decorative" pellets aimed to the top of the playfield')
        decorative = spread[decorative_start:]
        self.assertIn("bullet_template.angle = (SHINKI_DEVIL_MIRROR_ANGLE + bullet_angle_outer);", decorative)
        self.assertIn("bullet_template.origin.x.v += to_sp((COLUMN_W * (COLUMN_COUNT - 1)));", decorative)
        self.assertIn("DEVIL_NEXT_FIRE_COL(SHINKI_DEVIL_MIRROR_ANGLE + bullet_angle_inner);", decorative)
        self.assertIn("DEVIL_NEXT_FIRE_COL(DEVIL_ANGLE_ZERO - bullet_angle_inner);", decorative)
        self.assertIn("DEVIL_NEXT_FIRE_COL(DEVIL_ANGLE_ZERO - bullet_angle_outer);", decorative)
        self.assertEqual(define_int("SHINKI_DEVIL_PRELUDE_BULLET_COUNT", BALLISTICS), 1)
        self.assertEqual(define_int("SHINKI_DEVIL_FULL_BULLET_COUNT", BALLISTICS), 3)
        self.assertEqual(devil_const("DEVIL_DECORATIVE_SPREAD_COUNT"), 3)
        self.assertEqual(define_int("SHINKI_DEVIL_SPREAD_ARC_ANGLE", BALLISTICS), 0x30)

    def test_laser_mirrors_are_written_before_the_sweep_angles_advance(self):
        angle_start = DEVIL.index("lasers[0].coords.angle = laser_angle_outer;")
        angle_end = DEVIL.index("if(laser_direction == CLOCKWISE)", angle_start)
        angle_block = DEVIL[angle_start:angle_end]
        writes = [
            "lasers[0].coords.angle = laser_angle_outer;",
            "lasers[1].coords.angle = laser_angle_inner;",
            "lasers[2].coords.angle = (SHINKI_DEVIL_MIRROR_ANGLE - lasers[1].coords.angle);",
            "lasers[3].coords.angle = (SHINKI_DEVIL_MIRROR_ANGLE - lasers[0].coords.angle);",
        ]
        positions = [angle_block.index(write) for write in writes]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("laser_angle_outer++;", DEVIL[angle_end:])
        self.assertIn("laser_angle_inner--;", DEVIL[angle_end:])
        self.assertIn("laser_angle_outer--;", DEVIL[angle_end:])
        self.assertIn("laser_angle_inner++;", DEVIL[angle_end:])
        self.assertEqual(define_int("SHINKI_DEVIL_MIRROR_ANGLE", BALLISTICS), 0x80)

    def test_eight_frame_clock_reverses_at_inner_38_and_41(self):
        self.assertEqual(devil_const("DEVIL_LASER_TURN_INTERVAL_FRAMES"), 8)
        self.assertEqual(devil_const("DEVIL_LASER_INNER_LOW"), 0x38)
        self.assertEqual(devil_const("DEVIL_LASER_INNER_HIGH"), 0x41)
        turns, state_after_18 = laser_turns(18)
        self.assertEqual(turns[0], (0x40, 0x40, 0x40, 0x40))
        self.assertEqual(turns[1], (0x41, 0x3F, 0x41, 0x3F))
        self.assertEqual(turns[7], (0x47, 0x39, 0x47, 0x39))
        self.assertEqual(turns[8], (0x48, 0x38, 0x48, 0x38))
        self.assertEqual(turns[16], (0x40, 0x40, 0x40, 0x40))
        self.assertEqual(turns[17], (0x3F, 0x41, 0x3F, 0x41))
        self.assertEqual(state_after_18, (0x40, 0x40, "clockwise"))
        self.assertEqual(18 * 8, 144)

    def test_laser_turns_wait_until_the_shared_phase_latch_is_released(self):
        grow_start = DEVIL.index("// Lasers")
        grow = DEVIL[grow_start:]
        latch_start = grow.index("} else if(!lasers_active)")
        turn_start = grow.index("} else if((boss.phase_frame % DEVIL_LASER_TURN_INTERVAL_FRAMES) == 0)")
        self.assertLess(latch_start, turn_start)
        self.assertIn("if(bullet_angle_outer == DEVIL_SPREAD_OUTER_LOW)", grow[latch_start:turn_start])
        self.assertIn("lasers_active++;", grow[latch_start:turn_start])
        self.assertIn("boss.phase_frame % DEVIL_LASER_TURN_INTERVAL_FRAMES", grow[turn_start:])


    def test_laser_turn_frames_follow_the_first_post_latch_eight_frame_boundary(self):
        # Every outer-low boundary is 284 + 64*n, hence frame % 8 == 4.
        # The latch branch wins on that frame; the angle branch runs four
        # frames later at the next phase_frame multiple of eight.
        first_low_frames = [284 + 64 * n for n in range(8)]
        self.assertTrue(all(frame % 8 == 4 for frame in first_low_frames))
        first_turns = [frame + 4 for frame in first_low_frames]
        self.assertEqual(first_turns, [288, 352, 416, 480, 544, 608, 672, 736])
        self.assertTrue(all(frame % 8 == 0 for frame in first_turns))
        self.assertEqual([first_turns[0] + 8 * n for n in range(18)][-1], 424)


if __name__ == "__main__":
    unittest.main()
