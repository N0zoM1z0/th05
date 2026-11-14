"""Full EX-Alice eighteen-phase Boss controller, eight attack waves and final fan."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FULL = (ROOT / "src/main/boss/exalice/full_context.cpp").read_text()
PHASES = (ROOT / "src/main/boss/exalice/update_phases.hpp").read_text()
PROTOCOL = (ROOT / "src/main/boss/exalice/bomb_phase_protocol.hpp").read_text()
COMBAT = (ROOT / "src/main/boss/exalice/combat_layout.hpp").read_text()
SCRATCH = (ROOT / "src/main/boss/exalice/boss_scratch.hpp").read_text()
PATTERN_TABLE = (ROOT / "src/main/boss/exalice/pattern_pairs.cpp").read_text()
FINAL_RULES = (ROOT / "src/main/boss/exalice/final_attack_rules.hpp").read_text()
FINAL_PATTERNS = (ROOT / "src/main/boss/exalice/final_patterns.cpp").read_text()
PHASE_HELPER = (ROOT / "src/main/boss/exalice/phase.cpp").read_text()
GENERIC = (ROOT / "src/main/boss/generic.hpp").read_text()


def number(name, sources=(FULL, PHASES, PROTOCOL, COMBAT, FINAL_RULES)):
    for source in sources:
        match = re.search(rf"\b{re.escape(name)}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)\b", source)
        if match:
            return int(match.group(1), 0)
        match = re.search(rf"#define\s+{re.escape(name)}\s+(0[xX][0-9A-Fa-f]+|[0-9]+)\b", source)
        if match:
            return int(match.group(1), 0)
    raise AssertionError(f"missing EX-Alice constant {name}")


def phase(name, next_marker):
    start = FULL.index(f"case {name}:")
    end = FULL.index(next_marker, start + 1)
    return FULL[start:end]


def hp_ladder():
    return [number(name) for name in (
        "EXALICE_HP_INITIAL", "EXALICE_HP_SETUP_END",
        "EXALICE_HP_WAVE1_REGULAR_END", "EXALICE_HP_WAVE1_CHARGE_END",
        "EXALICE_HP_WAVE2_REGULAR_END", "EXALICE_HP_WAVE2_CHARGE_END",
        "EXALICE_HP_WAVE3_REGULAR_END", "EXALICE_HP_WAVE3_CHARGE_END",
        "EXALICE_HP_WAVE4_REGULAR_END", "EXALICE_HP_LAST_CHARGE_END")]


class ExAliceFullLifecycleTests(unittest.TestCase):
    def test_all_eighteen_phase_codes_form_four_regular_charge_pairs(self):
        names = [
            "EXALICE_PHASE_SETUP", "EXALICE_PHASE_READY", "EXALICE_PHASE_WAVE1_REGULAR",
            "EXALICE_PHASE_WAVE1_APPROACH", "EXALICE_PHASE_WAVE1_CHARGE",
            "EXALICE_PHASE_WAVE2_APPROACH_FIRST", "EXALICE_PHASE_WAVE2_REGULAR",
            "EXALICE_PHASE_WAVE2_APPROACH_SECOND", "EXALICE_PHASE_WAVE2_CHARGE",
            "EXALICE_PHASE_WAVE3_APPROACH_FIRST", "EXALICE_PHASE_WAVE3_REGULAR",
            "EXALICE_PHASE_WAVE3_APPROACH_SECOND", "EXALICE_PHASE_WAVE3_CHARGE",
            "EXALICE_PHASE_WAVE4_APPROACH_FIRST", "EXALICE_PHASE_WAVE4_REGULAR",
            "EXALICE_PHASE_WAVE4_APPROACH_SECOND", "EXALICE_PHASE_WAVE4_CHARGE",
            "EXALICE_PHASE_FINAL_FAN",
        ]
        self.assertEqual([number(name) for name in names], list(range(18)))
        self.assertEqual([number(f"EXALICE_WAVE_{i}") for i in range(1, 5)], [0, 1, 2, 3])
        self.assertEqual((number("EXALICE_MODE_REPOSITION"), number("EXALICE_MODE_CHARGE")), (0, 1))

    def test_full_hp_ladder_contains_eight_attack_endpoints_and_final_zero(self):
        self.assertEqual(hp_ladder(), [26500, 23800, 21000, 18100, 15100, 12600, 9600, 6800, 3400, 0])
        self.assertTrue(all(a > b for a, b in zip(hp_ladder(), hp_ladder()[1:])))
        helper = FULL[FULL.index("void pascal near exalice_phase_next("):FULL.index("// The first three charged")]
        self.assertLess(helper.index("boss.hp = boss.phase_end_hp;"), helper.index("boss.phase_end_hp = next_end_hp;"))
        self.assertIn("boss.phase++;", helper)
        self.assertIn("boss.phase_frame = EXALICE_NEW_PHASE_FIRST_FRAME;", helper)
        self.assertIn("boss.phase_state.patterns_seen = EXALICE_NEW_PHASE_PATTERN_COUNT;", helper)

    def test_setup_and_ready_have_independent_192_and_64_frame_invincible_clocks(self):
        self.assertEqual((number("EXALICE_FIRST_FRAME"), number("EXALICE_SETUP_END_FRAME"), number("EXALICE_READY_END_FRAME")), (1, 192, 64))
        setup = phase("EXALICE_PHASE_SETUP", "case EXALICE_PHASE_READY:")
        ready = phase("EXALICE_PHASE_READY", "case EXALICE_PHASE_WAVE1_REGULAR:")
        self.assertIn("if(boss.phase_frame == EXALICE_FIRST_FRAME)", setup)
        self.assertIn("boss.hp = EXALICE_HP_INITIAL;", setup)
        self.assertIn("boss.phase_end_hp = EXALICE_HP_SETUP_END;", setup)
        self.assertIn("boss_hittest_shots_invincible();", setup)
        self.assertIn("if(boss.phase_frame >= EXALICE_SETUP_END_FRAME)", setup)
        self.assertIn("if(boss.phase_frame >= EXALICE_READY_END_FRAME)", ready)
        self.assertIn("boss.mode = EXALICE_MODE_CHARGE;", ready)
        self.assertIn("boss.phase_state.patterns_seen = EXALICE_NEW_PHASE_PATTERN_COUNT;", ready)
        self.assertIn("exalice_boss_scratch.pattern_byte15.ready_direction_seed = EXALICE_READY_DIRECTION_SEED;", ready)
        self.assertIn("exalice_pattern = exalice_pattern_random_fan;", ready)
        self.assertIn("exalice_boss_scratch.wave_index = EXALICE_WAVE_1;", ready)

    def test_regular_attack_reposition_uses_32_pattern_count_and_skips_count_32_callback(self):
        self.assertEqual((number("EXALICE_RANDOM_FLYSTEP_LEAD_FRAMES"), number("EXALICE_REGULAR_PATTERN_LIMIT"), number("EXALICE_REGULAR_PATTERN_ALTERNATION_MASK")), (32, 32, 1))
        regular = phase("EXALICE_PHASE_WAVE1_REGULAR", "case EXALICE_PHASE_WAVE1_APPROACH:")
        ordered = [
            regular.index("boss.phase_state.patterns_seen++"),
            regular.index("boss.mode++"),
            regular.index("exalice_pattern = exalice_patterns_by_phase["),
            regular.index("if(boss.phase_state.patterns_seen >= EXALICE_REGULAR_PATTERN_LIMIT)"),
            regular.index("goto regular_complete;"),
            regular.index("if(!exalice_hittest_shots())"),
            regular.index("boss_score_bonus(EXALICE_REGULAR_HIT_BONUS);"),
        ]
        self.assertEqual(ordered, sorted(ordered))
        self.assertIn("boss_flystep_random(boss.phase_frame - EXALICE_RANDOM_FLYSTEP_LEAD_FRAMES)", regular)
        self.assertEqual(number("EXALICE_PATTERN_FIRST_FRAME"), 0)
        self.assertIn("boss.phase_frame = EXALICE_PATTERN_FIRST_FRAME;", regular)
        rows = re.search(r"exalice_patterns_by_phase\[4\]\[2\]\s*=\s*\{(.*?)\};", PATTERN_TABLE, re.S).group(1)
        self.assertEqual(len(re.findall(r"\{[^{}]+\}", rows)), 4)

    def test_each_regular_and_charge_transition_installs_the_next_attack_family(self):
        expected = {
            "EXALICE_WAVE_1": "exalice_pattern_firewave_fans",
            "EXALICE_WAVE_2": "exalice_pattern_bouncing_rings",
            "EXALICE_WAVE_3": "exalice_pattern_sweeping_lasers",
            "EXALICE_WAVE_4": "exalice_pattern_spiral_gather",
        }
        for wave, attack in expected.items():
            self.assertIn(f"case {wave}:", FULL)
            self.assertIn(f"{attack});", FULL)
        advance = FULL[FULL.index("#define EXALICE_WAVE_ADVANCE"):FULL.index("// Each later wave")]
        self.assertIn("exalice_pattern = next_attack", advance)
        for attack in (
            "exalice_pattern_firewave_fans", "exalice_pattern_bouncing_rings",
            "exalice_pattern_sweeping_lasers", "exalice_pattern_spiral_gather",
            "exalice_pattern_gravity_stacks", "exalice_pattern_fixed_laser_fan",
            "exalice_pattern_cross_cheetos",
        ):
            self.assertIn(attack, FULL)
        self.assertIn("exalice_pattern = exalice_pattern_random_fan;", FULL)
        self.assertIn("exalice_pattern_final_fan();", FULL)

    def test_approach_states_advance_to_charge_without_resetting_the_wave_selector(self):
        approach = FULL[FULL.index("approach:\n"):FULL.index("case EXALICE_PHASE_WAVE1_CHARGE:")]
        self.assertIn("boss_flystep_towards(", approach)
        self.assertIn("boss.phase_frame = EXALICE_NEW_PHASE_FIRST_FRAME;", approach)
        self.assertIn("boss.phase++;", approach)
        self.assertIn("boss.mode = EXALICE_MODE_CHARGE;", approach)
        resume = FULL[FULL.index("#define EXALICE_RESUME_WAVE"):FULL.index("// Wave 1 uses")]
        self.assertIn("goto approach;", resume)
        self.assertIn("goto regular_attack", resume)
        for name in ("EXALICE_PHASE_WAVE2_APPROACH_FIRST", "EXALICE_PHASE_WAVE3_APPROACH_FIRST", "EXALICE_PHASE_WAVE4_APPROACH_FIRST"):
            block_start = FULL.index(f"case {name}:")
            self.assertIn("EXALICE_RESUME_WAVE(", FULL[block_start:block_start + 700])

    def test_charge_timeout_is_strictly_greater_than_four_thousand(self):
        self.assertEqual(number("EXALICE_CHARGE_TIMEOUT_FRAME"), 4000)
        for name, next_name in (
            ("EXALICE_PHASE_WAVE1_CHARGE", "case EXALICE_PHASE_WAVE2_APPROACH_FIRST:"),
            ("EXALICE_PHASE_WAVE2_CHARGE", "case EXALICE_PHASE_WAVE3_APPROACH_FIRST:"),
            ("EXALICE_PHASE_WAVE3_CHARGE", "case EXALICE_PHASE_WAVE4_APPROACH_FIRST:"),
        ):
            block = phase(name, next_name)
            self.assertIn("if(boss.phase_frame > EXALICE_CHARGE_TIMEOUT_FRAME)", block)
            self.assertLess(block.index("goto charge_complete;"), block.index("charge_hittest:"))
        self.assertFalse(4000 > 4000)
        self.assertTrue(4001 > 4000)

    def test_wave_four_charge_ends_on_ninth_successful_callback_before_hit_gate(self):
        self.assertEqual(number("EXALICE_FINAL_CHARGE_PATTERN_LAST"), 8)
        block = phase("EXALICE_PHASE_WAVE4_CHARGE", "case EXALICE_PHASE_FINAL_FAN:")
        self.assertIn("if(exalice_charge_update())", block)
        self.assertIn("boss.phase_state.patterns_seen++;", block)
        self.assertIn("if(boss.phase_state.patterns_seen > EXALICE_FINAL_CHARGE_PATTERN_LAST)", block)
        self.assertLess(block.index("goto charge_complete;"), block.index("goto charge_hittest;"))
        shared_complete = phase("EXALICE_PHASE_WAVE1_CHARGE", "case EXALICE_PHASE_WAVE2_APPROACH_FIRST:")
        self.assertIn("case EXALICE_WAVE_4:", shared_complete)
        self.assertIn("exalice_phase_next(ET_VERTICAL, EXALICE_HP_LAST_CHARGE_END);", shared_complete)
        self.assertIn("exalice_boss_scratch.wave_index++;", shared_complete)

    def test_bomb_timer_decrements_before_frame_dispatch_and_gate_reloads_to_39(self):
        self.assertEqual((number("EXALICE_BOMB_INVINCIBILITY_RELOAD"), number("EXALICE_BOMB_INVINCIBILITY_EXPIRED")), (39, 0))
        self.assertLess(FULL.index("exalice_bomb_invincibility--;"), FULL.index("boss.phase_frame++;"))
        gate = FULL[FULL.index("int far exalice_hittest_shots(void)"):FULL.index("void pascal near exalice_phase_next(")]
        self.assertLess(gate.index("if(bombing)"), gate.index("if(exalice_bomb_invincibility == EXALICE_BOMB_INVINCIBILITY_EXPIRED)"))
        self.assertIn("exalice_bomb_invincibility = EXALICE_BOMB_INVINCIBILITY_RELOAD;", gate)
        self.assertIn("return boss_hittest_shots();", gate)
        self.assertIn("return EXALICE_SUPPRESSED_SHOT_RESULT;", gate)

    def test_final_fan_runs_before_inclusive_5000_timeout_and_timeout_skips_hit_bonus(self):
        self.assertEqual(number("EXALICE_FINAL_FAN_TIMEOUT_FRAME"), 5000)
        final = phase("EXALICE_PHASE_FINAL_FAN", "default:")
        self.assertIn("exalice_pattern_final_fan();", final)
        self.assertLess(final.index("exalice_pattern_final_fan();"), final.index("if(boss.phase_frame <= EXALICE_FINAL_FAN_TIMEOUT_FRAME)"))
        self.assertLess(final.index("if(boss.phase_frame <= EXALICE_FINAL_FAN_TIMEOUT_FRAME)"), final.index("boss.phase_state.defeat_bonus = true;"))
        self.assertIn("boss.phase = PHASE_BOSS_EXPLODE_SMALL;", final)
        self.assertIn("boss_custombullets_render = nullfunc_near;", final)
        self.assertIn("bullet_zap_drop_point_items = false;", final)
        self.assertTrue(5000 <= number("EXALICE_FINAL_FAN_TIMEOUT_FRAME"))
        self.assertFalse(5001 <= number("EXALICE_FINAL_FAN_TIMEOUT_FRAME"))

    def test_final_palette_zero_and_frame_resets_are_named_by_lifetime(self):
        self.assertIn("static const int EXALICE_PATTERN_FIRST_FRAME = 0;", FULL)
        self.assertIn("boss.phase_frame = EXALICE_PATTERN_FIRST_FRAME;", FULL)
        self.assertIn("boss.phase_frame = EXALICE_NEW_PHASE_FIRST_FRAME;", FULL)
        self.assertIn("boss.phase_state.patterns_seen = EXALICE_NEW_PHASE_PATTERN_COUNT;", FULL)
        self.assertIn("Palettes.colors[0].c.r == EXALICE_PALETTE_BLACK", FULL)
        self.assertIn("EXALICE_PALETTE_BLACK = 0", COMBAT)
        self.assertNotIn("boss.phase_frame = 0;", FULL)
        self.assertNotIn("boss.phase_state.patterns_seen = 0;", FULL)

    def test_shared_tail_updates_cheetos_firewaves_and_hud_on_every_phase(self):
        tail = FULL[FULL.index("    cheetos_update();", FULL.index("void pascal far exalice_update(void)")):]
        self.assertTrue(tail.startswith("    cheetos_update();\n    firewaves_update();\n    hud_hp_update_and_render(boss.hp, EXALICE_HP_INITIAL);"))


if __name__ == "__main__":
    unittest.main()
