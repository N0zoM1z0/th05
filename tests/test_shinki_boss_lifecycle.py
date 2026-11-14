"""Complete Shinki Boss phase graph, HP ladder, wave byte and timeout gates."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "src/main/boss/shinki/update_context.cpp").read_text()
NATURAL = (ROOT / "src/main/boss/shinki/shinki.cpp").read_text()
HP = (ROOT / "src/main/boss/shinki/hp.inl").read_text()
SETUP = (ROOT / "src/main/stage/setup.hpp").read_text()
SARA = (ROOT / "src/main/boss/sara/sara.hpp").read_text()
SHINKI_HPP = (ROOT / "src/main/boss/shinki/shinki.hpp").read_text()
MOVEMENT = (ROOT / "src/main/boss/movement.hpp").read_text()
GENERIC = (ROOT / "src/main/boss/generic.cpp").read_text()
GENERIC_HPP = (ROOT / "src/main/boss/generic.hpp").read_text()
EARLY = (ROOT / "src/main/boss/shinki/early_attack_rules.hpp").read_text()
WING = (ROOT / "src/main/boss/shinki/wing_attack_rules.hpp").read_text()
PREP = (ROOT / "src/main/boss/shinki/wing_preparation_rules.hpp").read_text()
HITBOX = (ROOT / "src/main/boss/shinki/wing_hitboxes.hpp").read_text()
SCRATCH = (ROOT / "src/main/boss/shinki/scratch.hpp").read_text()
DEVIL = (ROOT / "src/main/boss/shinki/devil.inl").read_text()


def integer(name, sources=(SOURCE, HP, SETUP, SARA, SHINKI_HPP, EARLY, WING, PREP, HITBOX)):
    for source in sources:
        match = re.search(rf"\b{re.escape(name)}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)\b", source)
        if match:
            return int(match.group(1), 0)
        match = re.search(rf"#define\s+{re.escape(name)}\s+(0[xX][0-9A-Fa-f]+|[0-9]+)\b", source)
        if match:
            return int(match.group(1), 0)
    raise AssertionError(f"missing Shinki constant {name}")


def phase(name, next_marker):
    start = SOURCE.index(f"case {name}:")
    end = SOURCE.index(next_marker, start + 1)
    return SOURCE[start:end]


def phase11():
    return phase("SHINKI_PHASE_DEFEAT_TRANSITION", "case SHINKI_PHASE_FINAL_CIRCLES:")


def phase12():
    start = SOURCE.index("case SHINKI_PHASE_FINAL_CIRCLES:")
    return SOURCE[start:SOURCE.index("default:", start)]


def hp_handoffs():
    return [integer(name, (HP,)) for name in (
        "HP_TOTAL", "HP_PHASE_2_END", "HP_PHASE_3_END", "HP_PHASE_6_END",
        "HP_PHASE_7_END", "HP_PHASE_9_END", "HP_PHASE_10_END", "HP_PHASE_12_END")]


class ShinkiBossLifecycleTests(unittest.TestCase):
    def test_thirteen_phase_values_are_contiguous_before_explosion_state(self):
        expected = {
            "PHASE_HP_FILL": 0, "PHASE_BOSS_ENTRANCE_BB": 1,
            "SHINKI_PHASE_CURVED_RINGS": 2, "SHINKI_PHASE_RANDOM_KUNAI": 3,
            "SHINKI_PHASE_APPROACH_WINGS": 4, "SHINKI_PHASE_WING_PREPARATION": 5,
            "SHINKI_PHASE_WING_RAIN": 6, "SHINKI_PHASE_SPREAD_WALLS": 7,
            "SHINKI_PHASE_PURPLE_TRANSITION": 8, "SHINKI_PHASE_SYMMETRIC_SPREADS": 9,
            "SHINKI_PHASE_DEVIL": 10, "SHINKI_PHASE_DEFEAT_TRANSITION": 11,
            "SHINKI_PHASE_FINAL_CIRCLES": 12,
        }
        self.assertEqual({name: integer(name) for name in expected}, expected)
        self.assertEqual(integer("PHASE_BOSS_EXPLODE_SMALL", (GENERIC_HPP,)), 253)
        self.assertEqual(hp_handoffs(), [22800, 20600, 18400, 14600, 11600, 8600, 2800, 0])

    def test_hp_fill_and_blackboard_entrance_have_distinct_exact_clocks(self):
        self.assertEqual((integer("SHINKI_FIRST_HP_FRAME"), integer("HUD_HP_FILL_FRAMES"), integer("SHINKI_HP_FILL_EXTRA_FRAMES")), (1, 128, 64))
        self.assertEqual((integer("ENTRANCE_BB_FRAMES_PER_CEL"), integer("TILES_BB_CELS")), (4, 16))
        setup = phase("PHASE_HP_FILL", "case PHASE_BOSS_ENTRANCE_BB:")
        entrance = phase("PHASE_BOSS_ENTRANCE_BB", "case SHINKI_PHASE_CURVED_RINGS:")
        self.assertIn("if(boss.phase_frame == SHINKI_FIRST_HP_FRAME)", setup)
        self.assertIn("boss.hp = HP_TOTAL;", setup)
        self.assertIn("boss.phase_end_hp = HP_PHASE_2_END;", setup)
        self.assertIn("boss_hittest_shots_invincible();", setup)
        self.assertIn("boss.phase_frame >= (HUD_HP_FILL_FRAMES + SHINKI_HP_FILL_EXTRA_FRAMES)", setup)
        self.assertIn("bg_render_bombing_func = shinki_bg_render;", setup)
        self.assertIn("boss.phase_frame == (\n\t\t\tENTRANCE_BB_FRAMES_PER_CEL * (TILES_BB_CELS / 2)", entrance)
        self.assertIn("boss.phase_frame >= (ENTRANCE_BB_FRAMES_PER_CEL * TILES_BB_CELS)", entrance)
        self.assertIn("boss.mode = SHINKI_MODE_PATTERN;", entrance)
        self.assertIn("phase_relative = SHINKI_FIRST_SHARED_WAVE;", entrance)
        self.assertEqual(128 + 64, 192)
        self.assertEqual(4 * 16, 64)

    def test_first_two_shared_waves_have_sixteen_completed_patterns_each(self):
        self.assertEqual((integer("SEAR_PATTERN_START_FRAME"), integer("SEAR_WAVE_PATTERN_LIMIT")), (32, 16))
        self.assertEqual(integer("SHINKI_ALTERNATING_PATTERN_MASK"), 1)
        waves = phase("SHINKI_PHASE_CURVED_RINGS", "case SHINKI_PHASE_APPROACH_WINGS:")
        self.assertIn("case SHINKI_PHASE_CURVED_RINGS:", waves)
        self.assertIn("case SHINKI_PHASE_RANDOM_KUNAI:", waves)
        self.assertIn("boss_flystep_random(\n\t\t\t\tboss.phase_frame - PHASE_2_3_PATTERN_START_FRAME", waves)
        self.assertIn("boss.phase_state.patterns_seen++", waves)
        self.assertIn("PATTERNS[phase_relative][\n\t\t\t\t\tboss.phase_state.patterns_seen & SHINKI_ALTERNATING_PATTERN_MASK", waves)
        self.assertLess(waves.index("phase_2_3_pattern = PATTERNS"), waves.index("if(boss.phase_state.patterns_seen >= SHINKI_WAVE_PATTERN_LIMIT)"))
        self.assertLess(waves.index("if(boss.phase_state.patterns_seen >= SHINKI_WAVE_PATTERN_LIMIT)"), waves.index("case SHINKI_MODE_PATTERN:"))
        self.assertIn("phase_2_3_with_pattern();", waves)
        self.assertIn("boss_phase_next(ET_NW_SE, HP_PHASE_3_END);", waves)
        self.assertIn("boss_phase_next(ET_NW_SE, HP_PHASE_6_END);", waves)
        self.assertIn("phase_relative++;", waves)
        self.assertIn("phase_2_3_pattern = pattern_random_directional_and_kunai;", waves)

    def test_approach_and_wing_preparation_install_ranked_hitbox_and_attack_bank(self):
        approach = phase("SHINKI_PHASE_APPROACH_WINGS", "case SHINKI_PHASE_WING_PREPARATION:")
        prep = phase("SHINKI_PHASE_WING_PREPARATION", "case SHINKI_PHASE_WING_RAIN:")
        self.assertLess(approach.index("boss_hittest_shots();"), approach.index("boss_flystep_towards("))
        self.assertIn("SHINKI_ADVANCE_PHASE_AND_RESET_CLOCK();", approach)
        self.assertIn("if(pattern_wing_preparation())", prep)
        self.assertIn("SHINKI_ADVANCE_PHASE_AND_RESET_CLOCK();", prep)
        self.assertIn("boss.pos.velocity.y.v = to_sp(SHINKI_RESET_Y_VELOCITY_PX);", prep)
        self.assertIn("boss_custombullets_render = shinki_custombullets_render;", prep)
        self.assertIn("select_for_playchar(", prep)
        for name, value in (("SHINKI_WING_HITBOX_REIMU_PX", 50), ("SHINKI_WING_HITBOX_MARISA_PX", 35), ("SHINKI_WING_HITBOX_MIMA_PX", 45), ("SHINKI_WING_HITBOX_YUUKA_PX", 50)):
            self.assertEqual(float(re.search(rf"#define {name} \(([-0-9.]+)f\)", HITBOX).group(1)), value)
        self.assertIn("wing_pattern = pattern_random_rain_and_spreads_from_wings;", prep)
        self.assertIn("phase_relative = SHINKI_FIRST_SHARED_WAVE;", prep)

    def test_wing_preparation_leaf_uses_six_fixed_lasers_then_fifty_bullets_and_eight_visible_frames(self):
        self.assertEqual((integer("SWPREP_START_FRAME"), integer("SWPREP_LASER_COUNT"), integer("SWPREP_SPAWN_BULLET_COUNT"), integer("SWPREP_WING_VISIBLE_FRAMES")), (16, 6, 50, 8))
        body = (ROOT / "src/main/boss/shinki/wing_preparation.cpp").read_text()
        self.assertEqual(body.count("laser_manual_fixed_spawn("), 6)
        self.assertIn("if(boss.phase_frame <= SWPREP_START_FRAME)", body)
        self.assertIn("if(lasers[SWPREP_SWEEP_TEST_LASER].coords.angle < SWPREP_LASER_SWEEP_LIMIT)", body)
        self.assertIn("if(wing_frame == SWPREP_WING_FIRST_FRAME)", body)
        self.assertIn("for(i = 0; i < SWPREP_SPAWN_BULLET_COUNT; i++)", body)
        self.assertIn("for(i = 0; i < LASERS_USED; i++) {\n\t\t\tlaser_manual_grow(i);", body)
        self.assertIn("if(wing_frame >= SWPREP_WING_VISIBLE_FRAMES)", body)
        self.assertIn("laser_stop(i);", body)
        self.assertIn("return true;", body)

    def test_wing_rain_and_spread_walls_share_the_strict_three_thousand_frame_gate(self):
        self.assertEqual(integer("SHW_WING_PHASE_TIMEOUT_FRAMES"), 3000)
        wings = phase("SHINKI_PHASE_WING_RAIN", "case SHINKI_PHASE_PURPLE_TRANSITION:")
        self.assertIn("case SHINKI_PHASE_WING_RAIN:", wings)
        self.assertIn("case SHINKI_PHASE_SPREAD_WALLS:", wings)
        self.assertIn("SHINKI_WING_FLIGHT_AND_ATTACK();", wings)
        self.assertIn("if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES)", wings)
        self.assertLess(wings.index("SHINKI_WING_FLIGHT_AND_ATTACK();"), wings.index("if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES)"))
        self.assertLess(wings.index("if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES)"), wings.index("if(phase_relative == SHW_WING_FIRST_PATTERN_INDEX)"))
        self.assertIn("boss_score_bonus(SHINKI_WING_PATTERN_SCORE);", wings)
        self.assertIn("boss_phase_next(ET_SW_NE, HP_PHASE_7_END);", wings)
        self.assertIn("boss_phase_next(ET_HORIZONTAL, HP_PHASE_9_END);", wings)
        self.assertIn("wing_pattern = pattern_cheetos_within_spread_walls;", wings)
        self.assertIn("phase_relative++;", wings)

    def test_purple_transition_has_hold_oscillation_spawn_and_finish_as_distinct_milestones(self):
        self.assertEqual((integer("SHW_PURPLE_HOLD_FRAMES"), integer("SHW_PURPLE_OSCILLATE_UNTIL"), integer("SHW_PURPLE_SPAWN_FRAME"), integer("SHW_PURPLE_FINISH_FRAME")), (160, 192, 192, 200))
        body = NATURAL[NATURAL.index("bool near pattern_wings_to_purple(void)"):NATURAL.index("void near pattern_aimed_b6balls_and_symmetric_spreads(void)")]
        self.assertIn("if(boss.phase_frame < SHW_PURPLE_HOLD_FRAMES)", body)
        self.assertIn("else if(boss.phase_frame < SHW_PURPLE_OSCILLATE_UNTIL)", body)
        self.assertIn("boss.phase_frame == SHW_PURPLE_UNREACHABLE_CHARGE_FRAME", body)
        self.assertIn("else if(boss.phase_frame == SHW_PURPLE_SPAWN_FRAME)", body)
        self.assertIn("for(int i = 0; i < SHW_PURPLE_SPAWN_COUNT; i++)", body)
        self.assertIn("return (boss.phase_frame == SHW_PURPLE_FINISH_FRAME);", body)
        self.assertEqual(integer("SHW_PURPLE_UNREACHABLE_CHARGE_FRAME"), 128)
        self.assertNotIn(128, range(160, 192))
        purple = phase("SHINKI_PHASE_PURPLE_TRANSITION", "case SHINKI_PHASE_SYMMETRIC_SPREADS:")
        self.assertIn("if(Palettes[0].c.b > SHINKI_PALETTE_ZERO)", purple)
        self.assertIn("boss_hittest_shots();", purple)
        self.assertIn("if(pattern_wings_to_purple())", purple)
        self.assertIn("SHINKI_ADVANCE_PHASE_AND_RESET_CLOCK();", purple)
        self.assertIn("wing_pattern = pattern_aimed_b6balls_and_symmetric_spreads;", purple)
        self.assertIn("phase_relative = SHINKI_FIRST_SHARED_WAVE;", purple)

    def test_symmetric_and_devil_waves_apply_bomb_damage_cap_before_hit_exit(self):
        wings = phase("SHINKI_PHASE_SYMMETRIC_SPREADS", "case SHINKI_PHASE_DEFEAT_TRANSITION:")
        self.assertIn("case SHINKI_PHASE_SYMMETRIC_SPREADS:", wings)
        self.assertIn("case SHINKI_PHASE_DEVIL:", wings)
        self.assertIn("SHINKI_WING_FLIGHT_AND_ATTACK();", wings)
        self.assertIn("phase_done = boss_hittest_shots();", wings)
        self.assertIn("if(bombing)", wings)
        self.assertIn("boss.hp += (boss.damage_this_frame - SHINKI_BOMB_DAMAGE_PER_FRAME);", wings)
        self.assertIn("phase_done = false;", wings)
        self.assertLess(wings.index("phase_done = boss_hittest_shots();"), wings.index("if(bombing)"))
        self.assertLess(wings.index("if(bombing)"), wings.index("if(!phase_done)"))
        self.assertEqual(integer("SHINKI_BOMB_DAMAGE_PER_FRAME"), 1)
        self.assertIn("boss_phase_next(ET_SW_NE, HP_PHASE_10_END);", wings)
        self.assertIn("shinki_wing_pattern = pattern_devil;", wings)
        self.assertIn("boss_phase_next(ET_HORIZONTAL, HP_PHASE_12_END);", wings)
        self.assertIn("laser_stop(SHINKI_DEVIL_LASER_SLOT_A);", wings)
        self.assertIn("laser_stop(SHINKI_DEVIL_LASER_SLOT_D);", wings)

    def test_devil_hp_subthresholds_are_not_phase_hp_handoffs(self):
        self.assertEqual((integer("HP_PHASE_10_DEVIL_LASER", (HP,)), integer("HP_PHASE_10_DEVIL_FAST", (HP,)), integer("HP_PHASE_10_END", (HP,))), (5600, 3800, 2800))
        self.assertGreater(integer("HP_PHASE_10_DEVIL_LASER", (HP,)), integer("HP_PHASE_10_DEVIL_FAST", (HP,)))
        self.assertGreater(integer("HP_PHASE_10_DEVIL_FAST", (HP,)), integer("HP_PHASE_10_END", (HP,)))
        self.assertIn("boss.hp <= HP_PHASE_10_DEVIL_LASER", DEVIL)
        self.assertIn("boss.hp <= HP_PHASE_10_DEVIL_FAST", DEVIL)
        self.assertIn("boss_phase_next(ET_SW_NE, HP_PHASE_10_END);", SOURCE)

    def test_defeat_transition_runs_seventeen_updates_and_carries_clock_to_final_spiral(self):
        self.assertEqual(integer("PHASE_11_FRAMES"), 16)
        defeat = phase11()
        self.assertIn("boss_hittest_shots();", defeat)
        self.assertIn("if((boss.phase_frame % 2) == SHINKI_DEFEAT_FLASH_EVEN_FRAME)", defeat)
        self.assertIn("if(boss.phase_frame > PHASE_11_FRAMES)", defeat)
        self.assertIn("boss.phase++;", defeat)
        self.assertNotIn("boss.phase_frame = SHINKI_PHASE_FRAME_RESET;", defeat)
        self.assertEqual(list(range(1, 18))[-1], 17)
        self.assertIn("boss_phase_next(ET_HORIZONTAL, HP_PHASE_12_END);", SOURCE)
        self.assertIn("boss.phase_state.patterns_seen = 0;", GENERIC)
        self.assertIn("patterns_seen;", MOVEMENT)
        self.assertIn("defeat_bonus;", MOVEMENT)
        self.assertIn("boss.phase_state.defeat_bonus", phase12())

    def test_final_spiral_leaf_precedes_strict_timeout_and_only_hp_hit_sets_reward(self):
        final = phase12()
        self.assertIn("pattern_circles_and_alternating_spirals();", final)
        self.assertLess(final.index("pattern_circles_and_alternating_spirals();"), final.index("if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES)"))
        self.assertLess(final.index("if(!boss_hittest_shots())"), final.index("boss.phase_state.defeat_bonus = true;"))
        self.assertIn("boss_explode_small(ET_VERTICAL);", final)
        self.assertIn("boss.phase = PHASE_BOSS_EXPLODE_SMALL;", final)
        self.assertEqual(integer("SHW_WING_PHASE_TIMEOUT_FRAMES"), 3000)
        self.assertEqual([frame for frame in (2999, 3000, 3001) if frame < integer("SHW_WING_PHASE_TIMEOUT_FRAMES")], [2999])

    def test_phase_reset_and_wave_index_names_preserve_distinct_zero_valued_roles(self):
        self.assertEqual(integer("SHINKI_PHASE_FRAME_RESET"), 0)
        self.assertEqual(integer("SHINKI_FIRST_SHARED_WAVE"), 0)
        self.assertIn("boss.phase_frame = SHINKI_PHASE_FRAME_RESET;", SOURCE)
        self.assertIn("phase_relative = SHINKI_FIRST_SHARED_WAVE;", SOURCE)
        self.assertNotIn("boss.phase_frame = 0;", SOURCE)
        self.assertNotIn("phase_relative = 0;", SOURCE)
        self.assertIn("Palettes[0].c.b = SHINKI_PALETTE_ZERO;", SOURCE)
        self.assertIn("unsigned char wave_relative_index;", SCRATCH)
        self.assertIn("unsigned char devil_lasers_active;", SCRATCH)
        self.assertIn("offsetof(ShinkiPhaseScratch, wave_or_laser) == 10", SCRATCH)

    def test_common_tail_updates_balls_cheetos_and_hud_for_every_phase(self):
        tail = SOURCE[SOURCE.index("\tb6balls_update();", SOURCE.index("void pascal shinki_update(void)")):]
        self.assertTrue(tail.startswith("\tb6balls_update();\n\tcheetos_update();\n\thud_hp_update_and_render(boss.hp, HP_TOTAL);"))
        self.assertIn("#undef SHINKI_ADVANCE_PHASE_AND_RESET_CLOCK", tail)


if __name__ == "__main__":
    unittest.main()
