"""Stage-four midboss disappearance/reappearance transition protocol."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
TRANSITION = (ROOT / "src/main/midboss/transition4.cpp").read_text()
TRANSITION_HPP = (ROOT / "src/main/midboss/transition4.hpp").read_text()
STAGE4 = (ROOT / "src/main/midboss/stage4.cpp").read_text()
STAGE4_HPP = (ROOT / "src/main/midboss/stage4.hpp").read_text()
SCRATCH = (ROOT / "src/main/midboss/stage4_scratch.hpp").read_text()


def constant(name):
    match = re.search(rf"\b{name}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)", TRANSITION)
    if not match:
        raise AssertionError(f"missing transition constant {name}")
    return int(match.group(1), 0)


def transition_step(phase_frame, x, y, center_x, vulnerable, stage_parity,
                    random_x=0, random_y=0):
    """Mirror the natural signed-int frame arithmetic in the 208-byte leaf."""
    start = constant("MIDBOSS4_TRANSITION_START_FRAME")
    half = constant("MIDBOSS4_TRANSITION_HALF_FRAMES")
    slowdown = constant("MIDBOSS4_TRANSITION_SLOWDOWN_FRAME")
    end = constant("MIDBOSS4_TRANSITION_END_FRAME")
    divisor = constant("MIDBOSS4_TRANSITION_SLOWDOWN_DIVISOR")
    x_step = constant("MIDBOSS4_TRANSITION_X_STEP_SP")
    x_range = constant("MIDBOSS4_TRANSITION_CENTER_X_RANGE_PX") * 16
    x_min = constant("MIDBOSS4_TRANSITION_CENTER_X_MIN_PX") * 16
    y_range = constant("MIDBOSS4_TRANSITION_CENTER_Y_RANGE_PX") * 16
    y_min = constant("MIDBOSS4_TRANSITION_CENTER_Y_MIN_PX") * 16

    sound = False
    complete = False
    if phase_frame >= start:
        frame = phase_frame - start
        if frame < half:
            if frame == 0:
                vulnerable = 0
                sound = True
                center_x = x
            if frame > slowdown:
                frame = slowdown + ((frame - slowdown) // divisor)
            x = center_x + frame * x_step if stage_parity else center_x - frame * x_step
        elif frame == half:
            center_x = (random_x % x_range) + x_min
            y = (random_y % y_range) + y_min
        else:
            frame = end - frame
            if frame > slowdown:
                frame = slowdown + ((frame - slowdown) // divisor)
            x = center_x + frame * x_step if stage_parity else center_x - frame * x_step
            if frame == 0:
                vulnerable = 1
                complete = True
    return x, y, center_x, vulnerable, sound, complete


class Midboss4TransitionTests(unittest.TestCase):
    def test_transition_constants_name_the_original_clock_and_coordinate_units(self):
        expected = {
            "MIDBOSS4_TRANSITION_START_FRAME": 16,
            "MIDBOSS4_TRANSITION_HALF_FRAMES": 32,
            "MIDBOSS4_TRANSITION_SLOWDOWN_FRAME": 20,
            "MIDBOSS4_TRANSITION_END_FRAME": 64,
            "MIDBOSS4_TRANSITION_SLOWDOWN_DIVISOR": 2,
            "MIDBOSS4_TRANSITION_X_STEP_SP": 32,
            "MIDBOSS4_TRANSITION_CENTER_X_RANGE_PX": 256,
            "MIDBOSS4_TRANSITION_CENTER_X_MIN_PX": 64,
            "MIDBOSS4_TRANSITION_CENTER_Y_RANGE_PX": 32,
            "MIDBOSS4_TRANSITION_CENTER_Y_MIN_PX": 64,
        }
        self.assertEqual({name: constant(name) for name in expected}, expected)
        self.assertIn("Natural movement algorithm from MAIN 1527:0D04", TRANSITION)

    def test_first_fifteen_phase_updates_do_not_move_or_change_vulnerability(self):
        initial = (2048, 1400, 0, 1)
        for phase_frame in range(1, 16):
            result = transition_step(phase_frame, *initial, stage_parity=1)
            self.assertEqual(result[:4], initial)
            self.assertEqual(result[4:], (False, False))

    def test_frame_sixteen_hides_the_midboss_and_captures_its_center_once(self):
        result = transition_step(16, 2100, 1400, 0, 1, stage_parity=1)
        self.assertEqual(result, (2100, 1400, 2100, 0, True, False))
        source = TRANSITION[TRANSITION.index("if(frame == 0)"):TRANSITION.index("if(frame > MIDBOSS4_TRANSITION_SLOWDOWN_FRAME)")]
        self.assertLess(source.index("midboss4_scratch.shot_vulnerable = 0;"),
                        source.index("snd_se_play(13);"))
        self.assertLess(source.index("snd_se_play(13);"),
                        source.index("midboss4_transition_center_x = midboss.pos.cur.x.v;"))

    def test_horizontal_motion_uses_stage_parity_and_signed_two_pixel_steps(self):
        center = 3000
        plus = transition_step(17, 0, 1200, center, 0, stage_parity=1)
        minus = transition_step(17, 0, 1200, center, 0, stage_parity=0)
        self.assertEqual((plus[0], minus[0]), (center + 32, center - 32))
        self.assertEqual(constant("MIDBOSS4_TRANSITION_X_STEP_SP"), 32)
        self.assertEqual(32 / 16, 2)

    def test_slowdown_is_integer_halving_after_twenty_frames_on_both_halves(self):
        center = 4096
        # phase_frame 36 maps to motion frame 20; frame 37 maps 21 -> 20.
        at_20 = transition_step(36, 0, 0, center, 0, stage_parity=1)
        at_21 = transition_step(37, 0, 0, center, 0, stage_parity=1)
        self.assertEqual((at_20[0], at_21[0]), (center + 640, center + 640))
        # The outbound peak at frame 31 compresses to 25.
        peak = transition_step(47, 0, 0, center, 0, stage_parity=1)
        self.assertEqual(peak[0], center + 800)
        # The inbound frame 43 maps to 21 -> 20; frame 44 is exactly 20.
        inbound_21 = transition_step(59, 0, 0, center, 0, stage_parity=1)
        inbound_20 = transition_step(60, 0, 0, center, 0, stage_parity=1)
        self.assertEqual((inbound_21[0], inbound_20[0]), (center + 640, center + 640))

    def test_midpoint_randomizes_center_and_y_without_moving_x_on_that_update(self):
        old_x = 4096 + 800
        old_y = 1700
        random_x = 1234
        random_y = 321
        result = transition_step(48, old_x, old_y, 4096, 0, stage_parity=1,
                                 random_x=random_x, random_y=random_y)
        self.assertEqual(result[0], old_x)
        self.assertEqual(result[1], random_y + 64 * 16)
        self.assertEqual(result[2], random_x + 64 * 16)
        self.assertEqual(result[3:], (0, False, False))
        self.assertEqual(constant("MIDBOSS4_TRANSITION_CENTER_X_MIN_PX"), 64)
        self.assertEqual(constant("MIDBOSS4_TRANSITION_CENTER_X_RANGE_PX"), 256)
        self.assertEqual(constant("MIDBOSS4_TRANSITION_CENTER_Y_MIN_PX"), 64)
        self.assertEqual(constant("MIDBOSS4_TRANSITION_CENTER_Y_RANGE_PX"), 32)

    def test_randomized_center_is_used_on_the_return_half_and_returns_to_zero(self):
        center = 64 * 16 + 1000
        first_return = transition_step(49, 0, 0, center, 0, stage_parity=1)
        self.assertEqual(first_return[0], center + 25 * 32)
        near_center = transition_step(79, 0, 0, center, 0, stage_parity=1)
        self.assertEqual(near_center[0], center + 32)
        complete = transition_step(80, 0, 0, center, 0, stage_parity=1)
        self.assertEqual(complete, (center, 0, center, 1, False, True))

    def test_transition_and_controller_share_the_typed_vulnerability_byte(self):
        self.assertIn("#define midboss4_scratch (*reinterpret_cast<Midboss4Scratch near *>(boss_statebyte))", SCRATCH)
        self.assertIn("midboss4_scratch.shot_vulnerable = 0;", TRANSITION)
        self.assertIn("midboss4_scratch.shot_vulnerable = 1;", TRANSITION)
        self.assertIn("#define vulnerable midboss4_scratch.shot_vulnerable", STAGE4)
        self.assertIn("shot_vulnerable", SCRATCH)
        self.assertIn("midboss4_vulnerable_at_15", SCRATCH)
        self.assertNotIn("boss_statebyte[15]", TRANSITION)

    def test_controller_resets_phase_clock_on_completion_before_next_pattern(self):
        start = STAGE4.index("if(midboss4_pattern_transition())")
        end = STAGE4.index("if(vulnerable)", start)
        completion = STAGE4[start:end]
        positions = [
            completion.index("midboss.phase_frame = 0;"),
            completion.index("patterns_done++;"),
            completion.index("pattern = ((patterns_done % MIDBOSS4_PATTERN_VARIANT_MODULUS) + MIDBOSS4_PATTERN_RANDOM_CLOUDS);"),
            completion.index("if(patterns_done >= MIDBOSS4_PATTERN_BUDGET)"),
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("goto defeat;", completion)
        self.assertLess(STAGE4.index("if(vulnerable)"), STAGE4.index("stage4_midboss_hittest_shots("))

    def test_leaf_only_returns_true_at_the_exact_end_and_does_not_clamp_later_calls(self):
        self.assertIn("if(frame == 0) {\n                midboss4_scratch.shot_vulnerable = 1;\n                return true;", TRANSITION)
        after = transition_step(81, 0, 0, 1000, 1, stage_parity=1)
        self.assertEqual(after[0], 1000 - 32)
        self.assertFalse(after[5])
        self.assertIn("if(midboss4_pattern_transition()) {", STAGE4)
        self.assertIn("midboss.phase_frame = 0;", STAGE4)


if __name__ == "__main__":
    unittest.main()
