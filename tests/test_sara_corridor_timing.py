"""The Sara corridor's two clocks and staged laser rotation are independent."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RULES = (ROOT / "src/main/boss/sara/projectile_rules.hpp").read_text()
SOURCE = (ROOT / "src/main/boss/sara/sara.cpp").read_text()


def sara_laser_constants():
    match = re.search(r"enum SaraLaserCorridorRules\s*\{(.*?)\};", RULES, re.S)
    if not match:
        raise AssertionError("SaraLaserCorridorRules enum is missing")
    values = {}
    for name, expression in re.findall(r"\b(SARA_[A-Z0-9_]+)\s*=\s*([^,]+)", match.group(1)):
        expression = expression.strip()
        try:
            values[name] = int(expression, 0)
        except ValueError:
            # The terminal angle is deliberately expressed from the two
            # canonical geometry constants instead of duplicated as 0x4A.
            continue
    return values, match.group(1)


def corridor_schedule(values):
    center = values["SARA_LASER_CORRIDOR_CENTER_ANGLE"]
    width = values["SARA_LASER_CORRIDOR_ANGLE_WIDTH"]
    offset = values["SARA_LASER_OFFSET_ANGLE"]
    terminal = center + width // 2
    left = (-center - offset) & 0xFF
    right = (-center + offset) & 0xFF
    interval = values["SARA_LASER_INITIAL_TURN_INTERVAL"]
    ball_count = values["SARA_LASER_INITIAL_BALL_COUNT"]
    threshold_angles = {
        values["SARA_LASER_SLOWDOWN_ANGLE_A"],
        values["SARA_LASER_SLOWDOWN_ANGLE_B"],
        values["SARA_LASER_SLOWDOWN_ANGLE_C"],
        values["SARA_LASER_SLOWDOWN_ANGLE_D"],
    }
    threshold_frames = []
    count_frames = []
    rotations = 0
    terminal_frame = None
    for frame in range(values["SARA_LASER_CREATE_FRAME"] + 1, 1301):
        if frame % interval == 0 and left > terminal:
            right = (right + 1) & 0xFF
            left = (left - 1) & 0xFF
            rotations += 1
            if left in threshold_angles:
                interval += 1
                threshold_frames.append((left, frame, interval))
            if left == terminal:
                terminal_frame = frame
        if frame % values["SARA_LASER_RANDOM_COUNT_STEP_FRAMES"] == 0:
            if ball_count < values["SARA_LASER_RANDOM_COUNT_LIMIT"]:
                ball_count += 1
                count_frames.append(frame)
    return {
        "left_initial": (-center - offset) & 0xFF,
        "right_initial": (-center + offset) & 0xFF,
        "left_final": left,
        "right_final": right,
        "terminal": terminal,
        "terminal_frame": terminal_frame,
        "rotations": rotations,
        "interval": interval,
        "threshold_frames": threshold_frames,
        "ball_count": ball_count,
        "count_frames": count_frames,
    }


class SaraCorridorTimingTests(unittest.TestCase):
    def test_terminal_angle_is_derived_from_center_and_width(self):
        values, enum = sara_laser_constants()
        self.assertEqual(values["SARA_LASER_CORRIDOR_CENTER_ANGLE"], 0x40)
        self.assertEqual(values["SARA_LASER_CORRIDOR_ANGLE_WIDTH"], 0x14)
        self.assertIn(
            "SARA_LASER_ROTATION_TERMINAL_ANGLE = (\n        SARA_LASER_CORRIDOR_CENTER_ANGLE + (SARA_LASER_CORRIDOR_ANGLE_WIDTH / 2)",
            enum,
        )
        self.assertIn(
            "lasers[X_LEFT].coords.angle > SARA_LASER_ROTATION_TERMINAL_ANGLE",
            SOURCE,
        )

    def test_four_slowdown_steps_reach_the_strict_terminal_on_frame_210(self):
        values, _ = sara_laser_constants()
        schedule = corridor_schedule(values)
        self.assertEqual(schedule["left_initial"], 0xA0)
        self.assertEqual(schedule["right_initial"], 0xE0)
        self.assertEqual(schedule["terminal"], 0x4A)
        self.assertEqual(
            schedule["threshold_frames"],
            [(0x80, 64, 2), (0x60, 128, 3), (0x58, 150, 4), (0x50, 180, 5)],
        )
        self.assertEqual(schedule["terminal_frame"], 210)
        self.assertEqual(schedule["rotations"], 86)
        self.assertEqual(schedule["left_final"], 0x4A)
        self.assertEqual(schedule["right_final"], 0x36)
        self.assertEqual(schedule["interval"], 5)

    def test_random_ball_count_uses_its_own_64_frame_clock(self):
        values, _ = sara_laser_constants()
        schedule = corridor_schedule(values)
        self.assertEqual(schedule["count_frames"], [64, 128, 192, 256, 320, 384, 448])
        self.assertEqual(schedule["ball_count"], 8)
        self.assertLess(
            SOURCE.index("if(stage_frame_mod16 == SAR_CORRIDOR_FIRE_TICK)"),
            SOURCE.index("if(\n\t\t((boss.phase_frame % SARA_LASER_RANDOM_COUNT_STEP_FRAMES) == 0)"),
        )

    def test_corridor_creation_growth_and_global_timeout_remain_distinct(self):
        values, _ = sara_laser_constants()
        self.assertEqual(values["SARA_LASER_CREATE_FRAME"], 32)
        self.assertEqual(values["SARA_LASER_GROW_FRAME"], 64)
        self.assertRegex(SOURCE, r"SARA_LASER_CORRIDOR_TIMEOUT\s*=\s*1300")
        self.assertIn("if(boss.phase_frame >= SARA_LASER_CORRIDOR_TIMEOUT)", SOURCE)


if __name__ == "__main__":
    unittest.main()
