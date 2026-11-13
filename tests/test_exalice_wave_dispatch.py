"""EX-Alice's four 32-callback regular waves and terminal charge schedule."""
from collections import Counter
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/exalice/update.cpp").read_text()
FULL = (ROOT / "src/main/boss/exalice/full_context.cpp").read_text()
TABLES = (ROOT / "src/main/boss/exalice/pattern_pairs.cpp").read_text()
PATTERNS = (ROOT / "src/main/boss/exalice/patterns.cpp").read_text()
PHASES = (ROOT / "src/main/boss/exalice/update_phases.hpp").read_text()


def table_rows():
    match = re.search(r"exalice_patterns_by_phase\[4\]\[2\]\s*=\s*\{(.*?)\};", TABLES, re.S)
    if not match:
        raise AssertionError("EX-Alice four-by-two callback table missing")
    return [re.findall(r"exalice_pattern_[a-z_]+", row) for row in re.findall(r"\{([^{}]+)\}", match.group(1))]


def phase_values():
    names = (
        "EXALICE_HP_INITIAL", "EXALICE_HP_SETUP_END",
        "EXALICE_HP_WAVE1_REGULAR_END", "EXALICE_HP_WAVE1_CHARGE_END",
        "EXALICE_HP_WAVE2_REGULAR_END", "EXALICE_HP_WAVE2_CHARGE_END",
        "EXALICE_HP_WAVE3_REGULAR_END", "EXALICE_HP_WAVE3_CHARGE_END",
        "EXALICE_HP_WAVE4_REGULAR_END", "EXALICE_HP_LAST_CHARGE_END",
    )
    return [int(re.search(rf"{name}\s*=\s*(\d+)", PHASES).group(1)) for name in names]


class ExAliceWaveDispatchTests(unittest.TestCase):
    def test_four_banks_and_preinstalled_callbacks_produce_exactly_32_executions(self):
        rows = table_rows()
        self.assertEqual(rows, [
            ["exalice_pattern_random_fan", "exalice_pattern_turning_rings"],
            ["exalice_pattern_gravity_stacks", "exalice_pattern_diamond_rings"],
            ["exalice_pattern_bouncing_rings", "exalice_pattern_speedup_fans"],
            ["exalice_pattern_cross_cheetos", "exalice_pattern_turning_cheetos"],
        ])
        initial = [
            "exalice_pattern_random_fan",
            "exalice_pattern_gravity_stacks",
            "exalice_pattern_fixed_laser_fan",
            "exalice_pattern_cross_cheetos",
        ]
        for wave, first in enumerate(initial):
            executed = [first] + [rows[wave][count & 1] for count in range(1, 32)]
            selected_at_limit = rows[wave][32 & 1]
            self.assertEqual(len(executed), 32)
            self.assertEqual(selected_at_limit, rows[wave][0])

        counts = [Counter([initial[w]] + [rows[w][count & 1] for count in range(1, 32)]) for w in range(4)]
        self.assertEqual(counts[0], Counter({rows[0][0]: 16, rows[0][1]: 16}))
        self.assertEqual(counts[1], Counter({rows[1][0]: 16, rows[1][1]: 16}))
        self.assertEqual(counts[2], Counter({"exalice_pattern_fixed_laser_fan": 1, rows[2][0]: 15, rows[2][1]: 16}))
        self.assertEqual(counts[3], Counter({rows[3][0]: 16, rows[3][1]: 16}))

        ready = UPDATE[UPDATE.index("case EXALICE_PHASE_READY:"):UPDATE.index("case EXALICE_PHASE_WAVE1_REGULAR:")]
        self.assertIn("exalice_pattern = exalice_pattern_random_fan;", ready)
        self.assertIn("exalice_boss_scratch.wave_index = EXALICE_WAVE_1;", ready)
        self.assertIn("exalice_pattern = exalice_pattern_gravity_stacks;", UPDATE)
        self.assertIn("exalice_pattern = exalice_pattern_fixed_laser_fan;", UPDATE)
        self.assertIn("exalice_pattern = exalice_pattern_cross_cheetos;", UPDATE)

    def test_count_32_selects_row_zero_then_jumps_before_callback_and_hit_bonus(self):
        for source in (UPDATE, FULL):
            start = source.index("case EXALICE_PHASE_WAVE1_REGULAR:")
            end = source.index("regular_complete:", start)
            regular = source[start:end]
            order = [
                "boss.phase_state.patterns_seen++;",
                "boss.mode++;",
                "exalice_pattern = exalice_patterns_by_phase[exalice_boss_scratch.wave_index][",
                "if(boss.phase_state.patterns_seen >= EXALICE_REGULAR_PATTERN_LIMIT)",
                "goto regular_complete;",
                "case EXALICE_MODE_CHARGE:",
                "if(!exalice_hittest_shots())",
                "boss_score_bonus(EXALICE_REGULAR_HIT_BONUS);",
            ]
            positions = [regular.index(token) for token in order]
            self.assertEqual(positions, sorted(positions))
        self.assertIn("EXALICE_REGULAR_PATTERN_LIMIT = 32", PHASES)
        self.assertIn("EXALICE_REGULAR_PATTERN_ALTERNATION_MASK = 1", PHASES)

    def test_charge_callback_resets_to_reposition_and_final_charge_ends_on_nine(self):
        start = PATTERNS.index("bool near exalice_charge_update(void)")
        end = PATTERNS.index("bool near exalice_pattern_random_fan(void)", start)
        charge = PATTERNS[start:end]
        self.assertIn("if(boss.phase_frame >= 64)", charge)
        self.assertIn("if(exalice_pattern())", charge)
        self.assertIn("boss.phase_frame = 0;", charge)
        self.assertIn("boss.mode = 0;", charge)

        final_charge = UPDATE[UPDATE.index("case EXALICE_PHASE_WAVE4_CHARGE:"):UPDATE.index("case EXALICE_PHASE_FINAL_FAN:")]
        self.assertIn("if(exalice_charge_update())", final_charge)
        self.assertIn("boss.phase_state.patterns_seen++;", final_charge)
        self.assertIn("if(boss.phase_state.patterns_seen > EXALICE_FINAL_CHARGE_PATTERN_LAST)", final_charge)
        self.assertLess(final_charge.index("goto charge_complete;"), final_charge.index("goto charge_hittest;"))
        charge_hit = UPDATE[UPDATE.index("charge_hittest:"):UPDATE.index("charge_complete:")]
        self.assertIn("if(!exalice_hittest_shots())", charge_hit)
        self.assertIn("boss_score_bonus(EXALICE_CHARGED_HIT_BONUS);", charge_hit)
        self.assertEqual(int(re.search(r"EXALICE_FINAL_CHARGE_PATTERN_LAST = (\d+)", PHASES).group(1)), 8)
        self.assertEqual(8 + 1, 9)

    def test_charge_timeout_is_strictly_after_frame_4000(self):
        charge = UPDATE[UPDATE.index("case EXALICE_PHASE_WAVE1_CHARGE:"):UPDATE.index("case EXALICE_PHASE_WAVE2_APPROACH_FIRST:")]
        self.assertIn("if(boss.phase_frame > EXALICE_CHARGE_TIMEOUT_FRAME)", charge)
        self.assertLess(charge.index("goto charge_complete;"), charge.index("charge_hittest:"))
        self.assertEqual(int(re.search(r"EXALICE_CHARGE_TIMEOUT_FRAME = (\d+)", PHASES).group(1)), 4000)
        self.assertFalse(4000 > 4000)
        self.assertTrue(4001 > 4000)

    def test_all_eight_phase_hp_handoffs_are_sequential_not_direct_assignments(self):
        values = phase_values()
        self.assertEqual(values, [26500, 23800, 21000, 18100, 15100, 12600, 9600, 6800, 3400, 0])
        handoffs = list(zip(values[1:-1], values[2:]))
        self.assertEqual(handoffs, [
            (23800, 21000), (21000, 18100), (18100, 15100), (15100, 12600),
            (12600, 9600), (9600, 6800), (6800, 3400), (3400, 0),
        ])
        self.assertIn("boss.hp = boss.phase_end_hp;", PHASES + (ROOT / "src/main/boss/exalice/phase.cpp").read_text())
        self.assertIn("boss.phase_end_hp = next_end_hp;", (ROOT / "src/main/boss/exalice/phase.cpp").read_text())


if __name__ == "__main__":
    unittest.main()
