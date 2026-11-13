"""Yumeko's sword-sweep loop, scratch-byte carry and aimed-burst protocol."""
from pathlib import Path
import math
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SWEEP = (ROOT / "src/main/boss/yumeko/sweep.cpp").read_text()
RULES = (ROOT / "src/main/boss/yumeko/sweep_combat_rules.hpp").read_text()
SCRATCH = (ROOT / "src/main/boss/yumeko/final_ring_scratch.hpp").read_text()
UPDATE = (ROOT / "src/main/boss/yumeko/update.cpp").read_text()


def macro(name):
    expression = re.search(rf"#define {name}\s+([^\n]+)", RULES).group(1).strip()
    expression = expression.strip("() ")
    if "*" in expression:
        left, right = expression.split("*", 1)
        return int(left.strip()) * int(right.strip())
    return int(expression)


def burst_cycle(initial_round, initial_speed):
    """Return one uninterrupted second-half cycle through its terminal reset."""
    round_value = initial_round
    speed = initial_speed
    shots = []
    sounds = 0
    retargets = 0
    terminal_return = False
    for _ in range(100):
        if speed > macro("YSW_BURST_RECYCLE_THRESHOLD_SUBPX"):
            speed = macro("YSW_BURST_RESTART_SPEED_SUBPX")
            sounds += 1
            round_value += 1
            if round_value > macro("YSW_BURST_ROUND_LIMIT"):
                round_value = macro("YSW_FIRST_ROUND")
                terminal_return = True
                break
            retargets += 1
        speed += macro("YSW_BURST_ACCEL_PER_VOLLEY_SUBPX")
        shots.append(speed)
    return shots, speed, round_value, sounds, retargets, terminal_return


class YumekoSweepCycleTests(unittest.TestCase):
    def test_ranked_sword_count_and_alternating_side_parity(self):
        spacing = {
            "EASY": macro("YSW_EASY_SWORD_SPACING_PX"),
            "NORMAL": macro("YSW_NORMAL_SWORD_SPACING_PX"),
            "HARD": macro("YSW_HARD_SWORD_SPACING_PX"),
            "LUNATIC": macro("YSW_LUNATIC_SWORD_SPACING_PX"),
        }
        expected = {
            "EASY": {9, 10}, "NORMAL": {12, 13},
            "HARD": {15, 16}, "LUNATIC": {22, 23, 24},
        }
        for rank, gap in spacing.items():
            counts = {math.ceil((376 - y) / gap) for y in range(32)}
            self.assertEqual(counts, expected[rank])
            final_sides = {(count * 0x80) & 0xFF for count in counts}
            self.assertEqual(final_sides, {0, 0x80})

        first = SWEEP[SWEEP.index("if(yumeko_sweep_round == YSW_FIRST_ROUND)"):]
        self.assertIn("sword_template.angle = yumeko_sweep_side;", first)
        self.assertIn("yumeko_sweep_side += YSW_OTHER_SIDE_ANGLE;", first)
        self.assertIn("boss2.pos.cur.y.v += (yumeko_sweep_spacing << YSW_SUBPIXEL_SHIFT);", first)
        self.assertIn("if(boss2.pos.cur.y.v >= to_sp(YSW_SWEEP_Y_LIMIT_PX))", first)
        self.assertIn("boss2.pos.cur.y.v = randring2_next16_mod(to_sp(YSW_FIRST_Y_JITTER_PX));", first)
        self.assertIn("yumeko_sweep_round++;", first)

    def test_first_cycle_has_four_twelve_bullet_bursts_and_a_terminal_no_shot(self):
        shots, speed, round_value, sounds, retargets, returned = burst_cycle(
            initial_round=1, initial_speed=128
        )
        self.assertEqual(shots, list(range(16, 105, 8)) * 4)
        self.assertEqual(len(shots), 48)
        self.assertEqual((speed, round_value, sounds, retargets, returned), (8, 0, 5, 4, True))

    def test_later_cycles_carry_speed_eight_and_last_aim_for_a_sixty_shot_cycle(self):
        shots, speed, round_value, sounds, retargets, returned = burst_cycle(
            initial_round=1, initial_speed=8
        )
        self.assertEqual(shots, list(range(16, 105, 8)) * 5)
        self.assertEqual(len(shots), 60)
        self.assertEqual((speed, round_value, sounds, retargets, returned), (8, 0, 5, 4, True))

        # A round reset occurs before the early return; the angle assignment is
        # after it, so the terminal boundary leaves the last aim unchanged.
        reset = SWEEP[SWEEP.index("if(yumeko_sweep_round > YSW_BURST_ROUND_LIMIT)"):]
        self.assertLess(reset.index("yumeko_sweep_round = YSW_FIRST_ROUND;"), reset.index("return;"))
        self.assertLess(reset.index("return;"), reset.index("bullet_template.angle = player_angle_from("))

    def test_only_charge_initializes_side_speed_and_round(self):
        self.assertIn("yumeko_sweep_side = YSW_FIRST_SIDE;", SWEEP)
        self.assertIn("yumeko_sweep_round = YSW_FIRST_ROUND;", SWEEP)
        self.assertIn("bullet_template.speed.v = YSW_BLUE_SPEED_SUBPX;", SWEEP)
        self.assertIn("YSW_BLUE_SPEED_SUBPX (8 * 16)", RULES)
        self.assertEqual(SWEEP.count("yumeko_sweep_side = YSW_FIRST_SIDE;"), 1)
        self.assertEqual(SWEEP.count("yumeko_sweep_round = YSW_FIRST_ROUND;"), 2)
        self.assertIn("yumeko_sweep_spacing", SCRATCH)
        self.assertIn("yumeko_pattern_sword_sweep();", UPDATE)

    def test_cycle_boundary_does_not_reset_live_side_speed_or_angle(self):
        terminal = SWEEP[SWEEP.index("if(yumeko_sweep_round > YSW_BURST_ROUND_LIMIT)"):]
        terminal = terminal[:terminal.index("bullet_template.angle = player_angle_from(")]
        self.assertIn("yumeko_sweep_round = YSW_FIRST_ROUND;", terminal)
        self.assertNotIn("yumeko_sweep_side", terminal)
        self.assertNotIn("bullet_template.speed.v", terminal)
        self.assertNotIn("bullet_template.angle", terminal)
        self.assertIn("bullet_template.speed.v += YSW_BURST_ACCEL_PER_VOLLEY_SUBPX;", SWEEP)
        self.assertIn("bullets_add_regular();", SWEEP)


if __name__ == "__main__":
    unittest.main()
