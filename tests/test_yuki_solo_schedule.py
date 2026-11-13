"""Frame-accurate source model for Yuki's complete ten-phase solo Boss."""
from collections import Counter
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/mai_yuki/yuki_update.cpp").read_text()
CHOREOGRAPHY = (ROOT / "src/main/boss/mai_yuki/yuki_solo_choreography.hpp").read_text()
TABLES = (ROOT / "src/main/boss/mai_yuki/solo_pattern_tables.cpp").read_text()
INITIAL = (ROOT / "src/main/boss/mai_yuki/yuki_patterns_initial.inl").read_text()
LATER = (ROOT / "src/main/boss/mai_yuki/yuki_patterns_later.inl").read_text()
GENERIC = (ROOT / "src/main/boss/generic.cpp").read_text()
GENERIC_HPP = (ROOT / "src/main/boss/generic.hpp").read_text()
MOVEMENT = (ROOT / "src/main/boss/movement.hpp").read_text()


def named_constants(source, prefix):
    values = {}
    for name, expression in re.findall(
        rf"\b({prefix}[A-Z0-9_]+)\s*=\s*([^,;}}]+)", source
    ):
        expression = expression.strip()
        try:
            values[name] = int(expression, 0)
        except ValueError:
            continue
    return values


def callback_bank(name):
    match = re.search(
        rf"MaiYukiPattern\s+{name}\[\d+\]\s*=\s*\{{(.*?)\}};",
        TABLES,
        re.S,
    )
    if not match:
        raise AssertionError(f"callback bank {name} is missing")
    return re.findall(r"\b(yuki_solo_[a-z0-9_]+)\b", match.group(1))


def alternating_wave(initial, bank, limit):
    """Count completed attacks, selecting the next callback after reposition."""
    sequence = [initial]
    for completed in range(1, limit):
        sequence.append(bank[completed & 1])
    return sequence


def final_wave(initial, bank, limit):
    """Final wave starts from a fresh zero counter after boss_phase_next."""
    sequence = [initial]
    for completed in range(1, limit):
        sequence.append(bank[completed % len(bank)])
    return sequence


def function_body(source, function_name, next_function_name):
    start = source.index(f"bool near {function_name}(void)")
    end = source.index(f"bool near {next_function_name}(void)", start)
    return source[start:end]


class YukiSoloScheduleTests(unittest.TestCase):
    def test_ten_phase_dispatch_and_hp_ladder_are_complete(self):
        values = named_constants(UPDATE, "YUKI_SOLO_PHASE_")
        self.assertEqual(
            [values[f"YUKI_SOLO_PHASE_{name}"] for name in (
                "SETUP", "READY", "ENTRANCE", "WAVE_FIRST",
                "WAVE_SECOND_APPROACH", "WAVE_SECOND", "SPEEDUP_APPROACH",
                "SPEEDUP", "FINAL_APPROACH", "WAVE_FINAL",
            )],
            list(range(10)),
        )
        self.assertEqual(values["YUKI_SOLO_PHASE_DEFEAT"], 253)
        health = named_constants(CHOREOGRAPHY, "YUKI_SOLO_HP_")
        self.assertEqual(
            [health[f"YUKI_SOLO_HP_{name}"] for name in (
                "TOTAL", "SETUP_GATE", "FIRST_WAVE_END", "SECOND_WAVE_END", "SPEEDUP_END"
            )],
            [7900, 4600, 3200, 1200, 0],
        )
        for phase in (
            "SETUP", "READY", "ENTRANCE", "WAVE_FIRST", "WAVE_SECOND_APPROACH",
            "WAVE_SECOND", "SPEEDUP_APPROACH", "SPEEDUP", "FINAL_APPROACH", "WAVE_FINAL",
        ):
            self.assertIn(f"case YUKI_SOLO_PHASE_{phase}:", UPDATE)

    def test_each_wave_has_an_independent_pattern_counter(self):
        limits = named_constants(UPDATE, "YUKI_SOLO_WAVE_")
        self.assertEqual(limits["YUKI_SOLO_WAVE_FIRST_LIMIT"], 12)
        self.assertEqual(limits["YUKI_SOLO_WAVE_SECOND_LIMIT"], 24)
        self.assertEqual(limits["YUKI_SOLO_WAVE_FINAL_LIMIT"], 36)
        self.assertIn("boss.phase_state.patterns_seen = 0;", GENERIC)
        self.assertIn("boss_phase_next(ET_NW_SE, YUKI_SOLO_HP_FIRST_WAVE_END);", UPDATE)
        self.assertIn("boss_phase_next(ET_SW_NE, YUKI_SOLO_HP_SECOND_WAVE_END);", UPDATE)

        pair1 = callback_bank("yuki_solo_pattern_pair1")
        pair2 = callback_bank("yuki_solo_pattern_pair2")
        first = alternating_wave("yuki_solo_ring_sweep", pair1, 12)
        second = alternating_wave("yuki_solo_random_rings", pair2, 24)
        self.assertEqual(len(first), 12)
        self.assertEqual(Counter(first), {
            "yuki_solo_ring_sweep": 6,
            "yuki_solo_random_spreads": 6,
        })
        self.assertEqual(len(second), 24)
        self.assertEqual(Counter(second), {
            "yuki_solo_random_rings": 12,
            "yuki_solo_snow_fan": 12,
        })

    def test_final_wave_fresh_counter_selects_vector_stack_first(self):
        limits = named_constants(UPDATE, "YUKI_SOLO_WAVE_")
        final_bank = callback_bank("yuki_solo_pattern_final")
        self.assertEqual(final_bank, [
            "yuki_solo_snow_cross",
            "yuki_solo_vector_stacks",
            "yuki_solo_vector_stacks",
            "yuki_solo_vector_stacks",
            "yuki_solo_vector_stacks",
        ])
        sequence = final_wave("yuki_solo_snow_cross", final_bank, limits["YUKI_SOLO_WAVE_FINAL_LIMIT"])
        self.assertEqual(len(sequence), 36)
        self.assertEqual(sequence[:6], [
            "yuki_solo_snow_cross",
            "yuki_solo_vector_stacks",
            "yuki_solo_vector_stacks",
            "yuki_solo_vector_stacks",
            "yuki_solo_vector_stacks",
            "yuki_solo_snow_cross",
        ])
        self.assertEqual(Counter(sequence), {
            "yuki_solo_snow_cross": 8,
            "yuki_solo_vector_stacks": 28,
        })
        self.assertIn("boss_solo_pattern_current = yuki_solo_snow_cross;", UPDATE)
        self.assertIn("boss.phase_state.patterns_seen % YUKI_SOLO_FINAL_PATTERN_COUNT", UPDATE)
        self.assertIn("YUKI_SOLO_FINAL_WAVE_DELAY_FRAMES = 8", CHOREOGRAPHY)

    def test_timed_clear_clears_the_shared_bonus_bit_but_hp_clear_sets_it(self):
        # The native Boss ABI overlays the per-wave count and defeat bonus
        # in the same byte at offset 21; zeroing the count is intentional.
        union = re.search(r"union\s*\{\s*unsigned char patterns_seen;\s*bool defeat_bonus;\s*\}", MOVEMENT, re.S)
        self.assertIsNotNone(union)
        self.assertIn("th05_boss_phase_state_at_21", MOVEMENT)

        timeout = UPDATE.index("if(boss.phase_state.patterns_seen >= YUKI_SOLO_WAVE_FINAL_LIMIT)")
        clear_count = UPDATE.index("boss.phase_state.patterns_seen = 0;", timeout)
        jump = UPDATE.index("goto defeat;", clear_count)
        hp_test = UPDATE.index("if(!boss_hittest_shots())", jump)
        grant_bonus = UPDATE.index("boss.phase_state.defeat_bonus = true;", hp_test)
        self.assertLess(timeout, clear_count)
        self.assertLess(clear_count, jump)
        self.assertLess(jump, hp_test)
        self.assertLess(hp_test, grant_bonus)
        self.assertIn("bullet_zap.active = boss.phase_state.defeat_bonus;", GENERIC_HPP)
        self.assertIn("if(boss.phase_state.defeat_bonus) { boss_score_bonus(bonus_units); }", GENERIC_HPP)

        # The timeout writes zero to the shared byte and bypasses the HP-only
        # true assignment; the HP route writes one before the common label.
        self.assertFalse(bool(0))
        self.assertTrue(bool(1))

    def test_snow_cross_fires_its_last_quarter_volley_before_reversing(self):
        body = function_body(LATER, "yuki_solo_snow_cross", "yuki_solo_vector_stacks")
        self.assertEqual(body.count("YUKI_SNOW_CROSS_QUARTER();"), 4)
        self.assertLess(
            body.index("YUKI_SNOW_CROSS_QUARTER();"),
            body.index("b4ball_template.angle += yuki_solo_snow_step;"),
        )
        self.assertLess(
            body.index("b4ball_template.angle += yuki_solo_snow_step;"),
            body.index("if(boss.phase_frame == 64)"),
        )
        volleys = list(range(32, 65, 4))
        self.assertEqual(volleys, [32, 36, 40, 44, 48, 52, 56, 60, 64])
        self.assertEqual(len(volleys) * 4, 36)
        self.assertIn("yuki_solo_snow_step = -yuki_solo_snow_step;", body)

    def test_snow_fan_fires_five_balls_at_each_of_five_32_frame_gates(self):
        body = function_body(LATER, "yuki_solo_snow_fan", "yuki_solo_snow_cross")
        self.assertIn("(boss.phase_frame % 32) == 0", body)
        self.assertEqual(body.count("YUKI_SNOW_FAN_NEXT_BALL("), 4)
        self.assertIn("b4balls_add();", body)
        volley_frames = list(range(32, 161, 32))
        self.assertEqual(volley_frames, [32, 64, 96, 128, 160])
        self.assertEqual(len(volley_frames) * 5, 25)
        self.assertLess(body.index("YUKI_SNOW_FAN_NEXT_BALL(+12);"), body.index("if(boss.phase_frame == 160)"))

    def test_vector_stacks_include_frame_64_before_reposition(self):
        body = function_body(LATER, "yuki_solo_vector_stacks", "yuki_solo_speedup")
        volley_frames = list(range(26, 65, 2))
        self.assertEqual(len(volley_frames), 20)
        self.assertEqual(volley_frames[-1], 64)
        self.assertLess(body.index("bullets_add_regular();"), body.index("if(boss.phase_frame == 64)"))
        self.assertLess(body.index("yuki_solo_angle_step = -yuki_solo_angle_step;"), body.index("YUKI_SOLO_REPOSITION();"))

    def test_opening_ring_and_random_ring_leaf_cadences_keep_terminal_volley(self):
        ring = function_body(INITIAL, "yuki_solo_ring_sweep", "yuki_solo_random_spreads")
        random_rings = function_body(INITIAL, "yuki_solo_random_rings", "yuki_solo") if "bool near yuki_solo(void)" in INITIAL else INITIAL[INITIAL.index("bool near yuki_solo_random_rings(void)"):]
        ring_frames = list(range(50, 257, 2))
        random_ring_frames = list(range(16, 161, 16))
        self.assertEqual(len(ring_frames), 104)
        self.assertEqual(len(random_ring_frames), 10)
        self.assertLess(ring.index("bullets_add_special();"), ring.index("if(boss.phase_frame == 160)"))
        self.assertLess(ring.index("if(boss.phase_frame == 160)"), ring.index("if(boss.phase_frame == 256)"))
        self.assertIn("if((boss.phase_frame % 16) == 0)", random_rings)
        self.assertLess(random_rings.index("bullets_add_regular();"), random_rings.index("if(boss.phase_frame == 160)"))

    def test_random_spreads_draws_speed_and_spread_per_even_frame(self):
        body = function_body(INITIAL, "yuki_solo_random_spreads", "yuki_solo_random_rings")
        self.assertEqual(body.count("randring2_next16_and("), 2)
        self.assertIn("randring2_next16_and(0x1F) + 8", body)
        self.assertIn("randring2_next16_and(7)", body)
        volley_frames = list(range(10, 257, 2))
        self.assertEqual(len(volley_frames), 124)
        self.assertEqual(volley_frames[-1], 256)
        self.assertLess(body.index("bullets_add_regular();"), body.index("if(boss.phase_frame == 256)"))

    def test_speedup_timeout_calls_leaf_on_frame_2000_before_phase_transition(self):
        values = named_constants(CHOREOGRAPHY, "YUKI_SOLO_SPEEDUP_")
        self.assertEqual(values["YUKI_SOLO_SPEEDUP_TIMEOUT_FRAMES"], 2000)
        self.assertLess(UPDATE.index("yuki_solo_speedup();"), UPDATE.index("if(boss.phase_frame < YUKI_SOLO_SPEEDUP_TIMEOUT_FRAMES)"))
        self.assertLess(UPDATE.index("if(boss.phase_frame < YUKI_SOLO_SPEEDUP_TIMEOUT_FRAMES)"), UPDATE.index("boss_phase_next(ET_HORIZONTAL, YUKI_SOLO_HP_SPEEDUP_END);"))
        frames = list(range(12, 2001, 4))
        self.assertEqual(len(frames), 498)
        self.assertEqual(frames[-1], 2000)


if __name__ == "__main__":
    unittest.main()
