"""Full 1,018-byte paired Mai/Yuki controller and survivor handoff."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/mai_yuki/update_context.cpp").read_text()
HEADER = (ROOT / "src/main/boss/mai_yuki/update.hpp").read_text()
RULES = (ROOT / "src/main/boss/mai_yuki/paired_attack_rules.hpp").read_text()
EFFECTS = (ROOT / "src/main/boss/mai_yuki/transition_effects.hpp").read_text()
HIT = (ROOT / "src/main/boss/mai_yuki/hit_result.hpp").read_text()


def number(name):
    for source in (UPDATE, HEADER, RULES, EFFECTS, HIT):
        for line in source.splitlines():
            needle = name + " = "
            if needle in line:
                raw = line.split(needle, 1)[1].split(";", 1)[0].strip().rstrip(",")
                try:
                    return int(raw, 0)
                except ValueError:
                    continue
    raise AssertionError(f"missing paired-fight constant {name}")


def macro(name):
    for source in (UPDATE, HEADER, RULES, EFFECTS, HIT):
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("#define " + name + " "):
                return int(stripped.split(None, 2)[2], 0)
    raise AssertionError(f"missing paired-fight rule {name}")


def phase(name, next_name):
    start = UPDATE.index(f"case {name}:")
    end = UPDATE.index(f"case {next_name}:", start + 1)
    return UPDATE[start:end]


def combat_phase():
    start = UPDATE.index("case MY_PHASE_COMBAT:")
    end = UPDATE.index("case MY_PHASE_EXPLODE_SMALL:", start + 1)
    return UPDATE[start:end]


def pattern_band(count):
    if count < number("MY_PATTERN_FIRST_END"):
        return "first"
    if count < number("MY_PATTERN_LASER_END"):
        return "laser"
    if count < number("MY_PATTERN_FINAL_END"):
        return "final"
    return "mai-defeat-timeout"


class MaiYukiLifecycleTests(unittest.TestCase):
    def test_six_phase_codes_and_two_fighter_hp_totals_are_original(self):
        self.assertEqual({
            "MY_PHASE_SETUP": number("MY_PHASE_SETUP"),
            "MY_PHASE_READY": number("MY_PHASE_READY"),
            "MY_PHASE_COMBAT": number("MY_PHASE_COMBAT"),
            "MY_PHASE_EXPLODE_SMALL": number("MY_PHASE_EXPLODE_SMALL"),
            "MY_PHASE_EXPLODE_BIG": number("MY_PHASE_EXPLODE_BIG"),
            "MY_PHASE_SURVIVOR_DIALOG": number("MY_PHASE_SURVIVOR_DIALOG"),
        }, {"MY_PHASE_SETUP": 0, "MY_PHASE_READY": 1, "MY_PHASE_COMBAT": 2,
            "MY_PHASE_EXPLODE_SMALL": 253, "MY_PHASE_EXPLODE_BIG": 254,
            "MY_PHASE_SURVIVOR_DIALOG": 255})
        self.assertEqual((number("MY_SHARED_HP"), number("MY_BOTH_HP_TOTAL"), number("MY_SURVIVOR_HP")), (4500, 9000, 7900))

    def test_setup_initializes_both_bosses_and_ready_uses_a_distinct_64_frame_gate(self):
        self.assertEqual((number("MY_SETUP_ENTRY_FRAME"), number("MY_SETUP_EXIT_FRAME"), number("MY_READY_EXIT_FRAME")), (1, 128, 64))
        setup = phase("MY_PHASE_SETUP", "MY_PHASE_READY")
        ready = phase("MY_PHASE_READY", "MY_PHASE_COMBAT")
        self.assertIn("boss.hp = MY_SHARED_HP;", setup)
        self.assertIn("boss2.hp = MY_SHARED_HP;", setup)
        self.assertIn("boss.phase_end_hp = MY_HP_END_UNSET;", setup)
        self.assertIn("boss2.phase_end_hp = MY_HP_END_UNSET;", setup)
        self.assertIn("MY_INVINCIBLE_PAIR_HITTEST();", setup)
        self.assertIn("if(boss.phase_frame >= MY_SETUP_EXIT_FRAME)", setup)
        self.assertIn("if(boss.phase_frame < MY_READY_EXIT_FRAME)", ready)
        self.assertIn("mai_pattern_current = mai_pattern_random_crosses;", ready)
        self.assertIn("yuki_pattern_current = yuki_pattern_random_aimed_fan;", ready)
        self.assertIn("boss_custombullets_render = cheetos_render;", ready)

    def test_homing_target_tracks_the_lower_boss_and_all_origins_share_the_boss(self):
        self.assertIn("if(boss.pos.cur.y.v > boss2.pos.cur.y.v)", UPDATE)
        self.assertIn("homing_target = boss.pos.cur;", UPDATE)
        self.assertIn("homing_target = boss2.pos.cur;", UPDATE)

    def test_pattern_schedule_is_ten_first_five_laser_and_twenty_one_final_callbacks(self):
        self.assertEqual((number("MY_PATTERN_FIRST_END"), number("MY_PATTERN_LASER_END"), number("MY_PATTERN_FINAL_END")), (10, 15, 36))
        self.assertEqual((number("MY_PATTERN_HP_GATE_FIRST"), number("MY_PATTERN_HP_GATE_SECOND")), (9, 14))
        self.assertEqual([pattern_band(i) for i in range(36)].count("first"), 10)
        self.assertEqual([pattern_band(i) for i in range(36)].count("laser"), 5)
        self.assertEqual([pattern_band(i) for i in range(36)].count("final"), 21)
        self.assertEqual(pattern_band(36), "mai-defeat-timeout")
        self.assertIn("MY_SELECT_PATTERN_PAIR(MAI_PATTERNS_FIRST, YUKI_PATTERNS_FIRST);", UPDATE)
        self.assertIn("mai_pattern_current = mai_pattern_tracking_laser;", UPDATE)
        self.assertIn("MY_SELECT_PATTERN_PAIR(MAI_PATTERNS_FINAL, YUKI_PATTERNS_FINAL);", UPDATE)

    def test_two_combined_hp_gates_are_strict_and_jump_to_pattern_counts_nine_and_fourteen(self):
        self.assertEqual((number("MY_HP_GATE_FIRST"), number("MY_HP_GATE_SECOND")), (5500, 2250))
        combat = combat_phase()
        self.assertIn("((boss.hp + boss2.hp) < MY_HP_GATE_FIRST)", combat)
        self.assertIn("((boss.hp + boss2.hp) < MY_HP_GATE_SECOND)", combat)
        self.assertIn("MY_ENTER_REPOSITION_GATE(MY_PATTERN_HP_GATE_FIRST);", combat)
        self.assertIn("MY_ENTER_REPOSITION_GATE(MY_PATTERN_HP_GATE_SECOND);", combat)
        gate = UPDATE[UPDATE.index("#define MY_ENTER_REPOSITION_GATE(gate)"):UPDATE.index("// Ordinary shared-fight phase advances")]
        self.assertIn("boss.mode = MY_MODE_REPOSITION;", gate)
        self.assertIn("boss.phase_frame = MY_PHASE_FRAME_RESET;", gate)
        self.assertIn("boss.phase_state.patterns_seen = gate", gate)
        self.assertEqual([hp for hp in (5501, 5500, 5499, 2251, 2250, 2249) if hp < 5500], [5499, 2251, 2250, 2249])

    def test_reposition_uses_long_lead_only_at_the_two_gate_counts_and_clears_on_frame_sixteen(self):
        self.assertEqual((number("MY_REPOSITION_LASER_LEAD_FRAMES"), number("MY_REPOSITION_NORMAL_LEAD_FRAMES"), number("MY_REPOSITION_CLEAR_FRAME")), (64, 16, 16))
        combat = combat_phase()
        self.assertIn("state_result = boss.phase_frame - MY_REPOSITION_LASER_LEAD_FRAMES;", combat)
        self.assertIn("state_result = boss.phase_frame - MY_REPOSITION_NORMAL_LEAD_FRAMES;", combat)
        self.assertIn("if(boss.phase_frame == MY_REPOSITION_CLEAR_FRAME)", combat)
        self.assertIn("boss_explode_small(ET_NW_SE);", combat)
        self.assertIn("boss2_explode_small(ET_SW_NE);", combat)
        self.assertIn("snd_se_play(MY_SHARED_GATE_WARNING_SE);", combat)
        self.assertEqual(number("MY_BULLET_CLEAR_MINIMUM"), 20)

    def test_pattern_exhaustion_forces_mai_defeat_without_setting_hit_reward(self):
        combat = combat_phase()
        terminal = combat[combat.index("else {\n                    boss.phase_state.patterns_seen = MY_PATTERN_COUNT_RESET;"):combat.index("case MY_MODE_ATTACK:")]
        self.assertIn("state_result = MY_HIT_MAI_DEFEATED;", terminal)
        self.assertIn("goto start_small_explosion;", terminal)
        self.assertNotIn("boss.phase_state.defeat_bonus = true;", terminal)
        self.assertLess(combat.index("if(state_result == MY_HIT_NONE)"), combat.index("boss.phase_state.defeat_bonus = true;"))
        self.assertIn("state_result - MY_HIT_TO_STORED_DEFEATED_INDEX", combat)
        self.assertIn("if(lasers[0].flag != LF_FREE)", combat)
        self.assertIn("laser_stop(MY_FIRST_LASER_TO_STOP);", combat)

    def test_hit_result_mapping_is_none_mai_yuki_to_loser_indices_zero_and_one(self):
        self.assertEqual((number("MY_HIT_NONE"), number("MY_HIT_MAI_DEFEATED"), number("MY_HIT_YUKI_DEFEATED")), (0, 1, 2))
        self.assertEqual(number("MY_HIT_TO_STORED_DEFEATED_INDEX"), 1)
        self.assertIn("MY_DEFEATED_MAI =\n    MY_HIT_MAI_DEFEATED - MY_HIT_TO_STORED_DEFEATED_INDEX;", HIT)
        self.assertIn("MY_DEFEATED_YUKI =\n    MY_HIT_YUKI_DEFEATED - MY_HIT_TO_STORED_DEFEATED_INDEX;", HIT)
        self.assertIn("unsigned char pattern_count;", HIT)
        self.assertIn("unsigned char defeated_character;", HIT)
        self.assertIn("MY_DEFEATED_CHARACTER(boss2.phase_state)", UPDATE)

    def test_small_explosion_has_distinct_frame_sixteen_and_thirty_two_handoffs(self):
        self.assertEqual((number("MY_SMALL_EXPLOSION_FIRST_FRAME"), number("MY_SMALL_EXPLOSION_BIG_FRAME")), (16, 32))
        small = phase("MY_PHASE_EXPLODE_SMALL", "MY_PHASE_EXPLODE_BIG")
        self.assertIn("if(boss.phase_frame == MY_SMALL_EXPLOSION_FIRST_FRAME)", small)
        self.assertIn("if(boss.phase_frame == MY_SMALL_EXPLOSION_BIG_FRAME)", small)
        self.assertIn("if(MY_MAI_WAS_DEFEATED())", small)
        self.assertIn("boss.phase++;", small)
        self.assertIn("bullet_zap.active = boss.phase_state.defeat_bonus;", small)
        self.assertIn("player_invincibility_time = MY_POST_EXPLOSION_INVINCIBILITY_FRAMES;", small)
        self.assertEqual(number("MY_POST_EXPLOSION_INVINCIBILITY_FRAMES"), 255)

    def test_big_explosion_shakes_twelve_frames_advances_sprite_every_eight_and_exits_at_sixty_four(self):
        self.assertEqual((number("MY_BIG_EXPLOSION_SHAKE_FRAMES"), number("MY_BIG_EXPLOSION_SPRITE_FRAMES"), number("MY_BIG_EXPLOSION_EXIT_FRAME")), (12, 8, 64))
        big = phase("MY_PHASE_EXPLODE_BIG", "MY_PHASE_SURVIVOR_DIALOG")
        self.assertIn("if(boss.phase_frame < MY_BIG_EXPLOSION_SHAKE_FRAMES)", big)
        self.assertIn("bg_render_bombing_func = tiles_render_all;", big)
        self.assertIn("slowdown_factor = MY_BIG_EXPLOSION_SLOWDOWN;", big)
        self.assertIn("if((boss.phase_frame % MY_BIG_EXPLOSION_SPRITE_FRAMES) == 0)", big)
        self.assertIn("if(boss.phase_frame >= MY_BIG_EXPLOSION_EXIT_FRAME)", big)

    def test_survivor_dialog_selects_the_actual_living_boss_and_restores_7900_hp(self):
        self.assertEqual((number("MY_SURVIVOR_DIALOG_ENTRY_FRAME"), number("MY_SURVIVOR_DIALOG_PALETTE_TONE"), number("MY_SURVIVOR_HP")), (1, 60, 7900))
        survivor = phase("MY_PHASE_SURVIVOR_DIALOG", "MY_PHASE_SURVIVOR_DIALOG") if UPDATE.count("case MY_PHASE_SURVIVOR_DIALOG:") > 1 else UPDATE[UPDATE.index("case MY_PHASE_SURVIVOR_DIALOG:"):]
        self.assertIn("PaletteTone = MY_SURVIVOR_DIALOG_PALETTE_TONE;", survivor)
        self.assertIn("if(boss.phase_frame == MY_SURVIVOR_DIALOG_ENTRY_FRAME)", survivor)
        self.assertIn("dialog_load(MY_DIALOG_YUKI);", survivor)
        self.assertIn("boss.pos.cur = boss2.pos.cur;", survivor)
        self.assertIn("boss_update = yuki_update;", survivor)
        self.assertIn("dialog_load(MY_DIALOG_MAI);", survivor)
        self.assertIn("boss_update = mai_update;", survivor)
        self.assertIn("boss_fg_render = mai_yuki_survivor_render;", survivor)
        self.assertIn("boss.hp = MY_SURVIVOR_HP;", survivor)
        self.assertIn("hud_hp_update_and_render(boss.hp + boss2.hp, MY_BOTH_HP_TOTAL);", UPDATE)

    def test_reset_sentinels_do_not_alias_the_survivor_phase_or_defeated_identity(self):
        self.assertEqual((number("MY_PHASE_FRAME_RESET"), number("MY_PATTERN_COUNT_RESET"), number("MY_HP_END_UNSET")), (0, 0, 0))
        self.assertEqual(number("MY_SURVIVOR_RESET_PHASE"), 0)
        self.assertIn("MY_PHASE_FRAME_RESET", UPDATE)
        self.assertIn("MY_PATTERN_COUNT_RESET", UPDATE)
        self.assertIn("MY_HP_END_UNSET", UPDATE)
        self.assertIn("defeated_character", HIT)


if __name__ == "__main__":
    unittest.main()
