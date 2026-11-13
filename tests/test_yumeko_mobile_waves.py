"""Yumeko's two large mobile-wave state machines and callback-bank protocol."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/yumeko/update.cpp").read_text()
PATTERNS = (ROOT / "src/main/boss/yumeko/patterns.cpp").read_text()
SCHEDULES = (ROOT / "src/main/boss/yumeko/schedule_data.cpp").read_text()
SCRATCH = (ROOT / "src/main/boss/yumeko/final_ring_scratch.hpp").read_text()
TIMING = (ROOT / "src/main/boss/yumeko/phase_timing.hpp").read_text()


def phase_block(name, next_marker):
    start = UPDATE.index(f"case {name}:")
    end = UPDATE.index(next_marker, start)
    return UPDATE[start:end]


def bank(name):
    match = re.search(rf"yumeko_patterns_{name}\[4\]\s*=\s*\{{([^}}]+)\}}", SCHEDULES, re.S)
    if not match:
        raise AssertionError(f"Yumeko {name} bank missing")
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


class YumekoMobileWaveTests(unittest.TestCase):
    def test_each_wave_has_one_preinstalled_callback_then_nineteen_bank_callbacks(self):
        first = bank("phase2")
        second = bank("phase5")
        self.assertEqual(first, ["yumeko_pattern_sword_fan", "yumeko_pattern_red_ring", "0", "0"])
        self.assertEqual(second, ["yumeko_pattern_counterrotating_spreads", "yumeko_pattern_mirrored_spreads", "0", "0"])

        entrance = phase_block("YUMEKO_PHASE_ENTRANCE_WAIT", "case YUMEKO_PHASE_MOBILE_FIRST:")
        stationary_first = phase_block("YUMEKO_PHASE_STATIONARY_FIRST", "case YUMEKO_PHASE_SWORD_SWEEP:")
        self.assertIn("yumeko_pattern = yumeko_pattern_sword_fan;", entrance)
        self.assertIn("yumeko_pattern = yumeko_pattern_counterrotating_spreads;", stationary_first)

        first_wave = ["yumeko_pattern_sword_fan"] + [first[count & 1] for count in range(1, 20)]
        second_wave = ["yumeko_pattern_counterrotating_spreads"] + [second[count & 1] for count in range(1, 20)]
        self.assertEqual(len(first_wave), 20)
        self.assertEqual(len(second_wave), 20)
        self.assertEqual(first_wave.count("yumeko_pattern_sword_fan"), 10)
        self.assertEqual(first_wave.count("yumeko_pattern_red_ring"), 10)
        self.assertEqual(second_wave.count("yumeko_pattern_counterrotating_spreads"), 10)
        self.assertEqual(second_wave.count("yumeko_pattern_mirrored_spreads"), 10)

    def test_twentieth_reposition_completion_exits_before_bank_lookup_and_hit_test(self):
        values = re.search(r"YUMEKO_WAVE_PATTERN_LIMIT\s*=\s*(\d+)", SCRATCH)
        self.assertIsNotNone(values)
        limit = int(values.group(1))
        self.assertEqual(limit, 20)
        mobile = phase_block("YUMEKO_PHASE_MOBILE_FIRST", "case YUMEKO_PHASE_APPROACH_FIRST:")
        increment = mobile.index("boss.phase_state.patterns_seen++;")
        limit_test = mobile.index("boss.phase_state.patterns_seen >= YUMEKO_WAVE_PATTERN_LIMIT")
        early_exit = mobile.index("goto moving_phase_end;")
        bank_lookup = mobile.index("YUMEKO_SELECT_MOBILE_BANK(")
        hit_test = mobile.index("if(!boss_hittest_shots())")
        self.assertLess(increment, limit_test)
        self.assertLess(limit_test, early_exit)
        self.assertLess(early_exit, bank_lookup)
        self.assertLess(bank_lookup, hit_test)

        # Counts 1..19 select the next callback. Count 20 takes the goto and
        # cannot index either four-entry table or execute the hit/bonus path.
        selected_counts = list(range(1, limit))
        self.assertEqual(len(selected_counts), 19)
        self.assertNotIn(limit, selected_counts)
        self.assertIn("YUMEKO_FINISH_MOBILE_WAVE(ET_CIRCLE, YUMEKO_HP_AFTER_MOBILE_FIRST);", mobile)
        self.assertIn("YUMEKO_FINISH_MOBILE_WAVE(ET_HORIZONTAL, YUMEKO_HP_AFTER_MOBILE_SECOND);", mobile)
        timing = re.search(r"YUMEKO_HP_AFTER_MOBILE_FIRST\s*=\s*(\d+)", TIMING)
        self.assertEqual(int(timing.group(1)), 5700)
        timing = re.search(r"YUMEKO_HP_AFTER_MOBILE_SECOND\s*=\s*(\d+)", TIMING)
        self.assertEqual(int(timing.group(1)), 2700)

    def test_reposition_callback_resets_phase_clock_and_runs_for_64_updates(self):
        macro_start = PATTERNS.index("#define YUMEKO_PATTERNS_ENTER_REPOSITION()")
        macro_end = PATTERNS.index("// In the sword fan", macro_start)
        reposition_macro = PATTERNS[macro_start:macro_end]
        self.assertIn("boss.phase_frame = 0;", reposition_macro)
        self.assertIn("boss.mode = YUMEKO_MODE_REPOSITION;", reposition_macro)
        self.assertIn("YUMEKO_MOBILE_REPOSITION_FRAMES = 64", TIMING)

        start = PATTERNS.index("bool pascal near yumeko_flystep_bounce(")
        end = PATTERNS.index("void near yumeko_pattern_sword_fan(void)", start)
        flystep = PATTERNS[start:end]
        self.assertIn("if(boss.phase_frame == YM_BOUNCE_START_FRAME)", flystep)
        self.assertIn("boss.pos.cur.x.v += boss.pos.velocity.x.v;", flystep)
        self.assertIn("boss.pos.cur.y.v += boss.pos.velocity.y.v;", flystep)
        self.assertIn("if(boss.phase_frame >= end_frame)", flystep)
        self.assertIn("return true;", flystep)

        # The controller increments once before dispatch. A reset to zero is
        # followed by exactly frames 1..64 before the reposition completes.
        self.assertIn("boss.phase_frame++;", UPDATE)
        self.assertEqual(list(range(1, 65))[-1], 64)
        self.assertEqual(20 * 64, 1280)

    def test_mode_values_and_bank_selection_share_the_original_one_bit_index(self):
        self.assertIn("YUMEKO_MODE_REPOSITION = 0", SCRATCH)
        self.assertIn("YUMEKO_MODE_ATTACK = 1", SCRATCH)
        self.assertIn("boss.phase_state.patterns_seen & YM_MOBILE_ATTACK_VARIANT_MASK", UPDATE)
        self.assertIn("#define YM_MOBILE_ATTACK_VARIANT_MASK 1", (ROOT / "src/main/boss/yumeko/mobile_attack_rules.hpp").read_text())
        mobile = phase_block("YUMEKO_PHASE_MOBILE_FIRST", "case YUMEKO_PHASE_APPROACH_FIRST:")
        self.assertIn("if(boss.mode == YUMEKO_MODE_REPOSITION) {\n            break;\n        }", mobile)
        self.assertIn("case YUMEKO_MODE_REPOSITION:", mobile)
        self.assertIn("case YUMEKO_MODE_ATTACK:", mobile)


if __name__ == "__main__":
    unittest.main()
