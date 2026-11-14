"""Stage-three midboss movement, three attack leaves and terminal dispatch."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = (ROOT / "src/main/midboss/stage3_patterns.cpp").read_text()
UPDATE = (ROOT / "src/main/midboss/stage3.cpp").read_text()
PATTERN_HPP = (ROOT / "src/main/midboss/stage3_patterns.hpp").read_text()
STAGE3_HPP = (ROOT / "src/main/midboss/stage3.hpp").read_text()
SCRATCH = (ROOT / "src/main/midboss/stage3_scratch.hpp").read_text()


def number(name):
    for source in (PATTERNS, UPDATE, PATTERN_HPP, STAGE3_HPP, SCRATCH):
        needle = name + " = "
        for line in source.splitlines():
            if needle in line:
                value = line.split(needle, 1)[1].split(";", 1)[0].strip()
                return int(value, 0)
    raise AssertionError(f"missing Stage 3 constant {name}")


def function(source, name, next_name=None):
    start = source.index(f"void near {name}(void)")
    if next_name is None:
        return source[start:]
    end = source.index(f"void near {next_name}(void)", start + 1)
    return source[start:end]


class Midboss3LifecycleTests(unittest.TestCase):
    def test_reposition_has_twelve_disappear_ticks_and_eight_return_ticks(self):
        leaf = function(PATTERNS, "midboss3_reposition", "midboss3_gather_charge")
        self.assertIn("(midboss.phase_frame & MIDBOSS3_REPOSITION_TICK_MASK) == 0", leaf)
        self.assertEqual(number("MIDBOSS3_REPOSITION_TICK_MASK"), 3)
        self.assertEqual(number("MIDBOSS3_REPOS_SPRITE_LIMIT"), 220)
        self.assertEqual(number("MIDBOSS3_REPOS_SPRITE_LAST"), 219)
        self.assertEqual(number("MIDBOSS3_SPRITE_STILL"), 208)
        self.assertEqual(number("MIDBOSS3_SPRITE_INVINCIBLE"), 212)
        self.assertEqual(number("MIDBOSS3_REPOSITION_Y_STEP_PX"), 12)

        sprite = number("MIDBOSS3_SPRITE_STILL")
        returning = 0
        y_delta = 0
        x = 0
        phase_frame = number("MIDBOSS3_PATTERN_REPOSITION_FRAME")
        disappear_ticks = return_ticks = 0
        completion_frame = None
        for frame in range(phase_frame, phase_frame + 100):
            if frame & number("MIDBOSS3_REPOSITION_TICK_MASK"):
                continue
            if not returning:
                sprite += 1
                disappear_ticks += 1
                if sprite >= number("MIDBOSS3_REPOS_SPRITE_LIMIT"):
                    sprite = number("MIDBOSS3_REPOS_SPRITE_LAST")
                    y_delta += number("MIDBOSS3_REPOSITION_Y_STEP_PX") * 16
                    x = max(64 * 16, min(320 * 16, 400 * 16))
                    returning += 1
            else:
                sprite -= 1
                return_ticks += 1
                if sprite < number("MIDBOSS3_SPRITE_INVINCIBLE"):
                    sprite = number("MIDBOSS3_SPRITE_STILL")
                    returning = 0
                    completion_frame = frame
                    break
        self.assertEqual((disappear_ticks, return_ticks), (12, 8))
        self.assertEqual((sprite, returning, y_delta), (208, 0, 12 * 16))
        self.assertEqual(completion_frame, 172)
        self.assertEqual(x, 320 * 16)
        self.assertIn("midboss.phase_frame = 0;", leaf)
        self.assertIn("midboss3_scratch.active_attack = 0;", leaf)

    def test_reposition_clamps_player_x_to_the_arena_edges(self):
        self.assertEqual((number("MIDBOSS3_ARENA_LEFT_PX"), number("MIDBOSS3_ARENA_RIGHT_PX")), (64, 320))
        clamp = lambda x: max(64, min(320, x))
        self.assertEqual([clamp(x) for x in (24, 64, 200, 320, 400)], [64, 64, 200, 320, 320])
        leaf = function(PATTERNS, "midboss3_reposition", "midboss3_gather_charge")
        self.assertIn("midboss.pos.cur.x = player_pos.cur.x;", leaf)
        self.assertIn("if(midboss.pos.cur.x.v < to_sp(MIDBOSS3_ARENA_LEFT_PX))", leaf)
        self.assertIn("else if(midboss.pos.cur.x.v > to_sp(MIDBOSS3_ARENA_RIGHT_PX))", leaf)

    def test_gather_charge_uses_color_order_and_sprite_keyframes(self):
        leaf = function(PATTERNS, "midboss3_gather_charge", "midboss3_pattern_1")
        self.assertIn("gather_add_only_3stack(midboss.phase_frame - 1, MIDBOSS3_GATHER_COLOR_FIRST, MIDBOSS3_GATHER_COLOR_SECOND);", leaf)
        self.assertEqual((number("MIDBOSS3_GATHER_COLOR_FIRST"), number("MIDBOSS3_GATHER_COLOR_SECOND")), (11, 10))
        self.assertEqual((number("MIDBOSS3_CHARGE_SOUND"), number("MIDBOSS3_CHARGE_SPRITE_FIRST"), number("MIDBOSS3_CHARGE_SPRITE_SECOND")), (8, 210, 211))
        self.assertLess(leaf.index("if(midboss.phase_frame == 1)"), leaf.index("if(midboss.phase_frame == 16)"))
        self.assertIn("snd_se_play(MIDBOSS3_CHARGE_SOUND);", leaf)

    def test_pattern_one_has_three_distinct_blue_red_blue_spread_stacks(self):
        leaf = function(PATTERNS, "midboss3_pattern_1", "midboss3_pattern_2")
        self.assertEqual((number("MIDBOSS3_CHARGE_FRAMES"), number("MIDBOSS3_VOLLEY_FIRST_FRAME"), number("MIDBOSS3_VOLLEY_SECOND_FRAME"), number("MIDBOSS3_VOLLEY_THIRD_FRAME")), (32, 32, 48, 64))
        self.assertIn("bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;", leaf)
        self.assertIn("bullet_template.patnum = MIDBOSS3_PAT_BALL_RED;", leaf)
        self.assertIn("midboss3_set_spread_stack(MIDBOSS3_P1_FIRST_SPREAD, MIDBOSS3_P1_FIRST_DELTA, MIDBOSS3_P1_STACK_COUNT, 0.5f);", leaf)
        self.assertIn("midboss3_set_spread_stack(MIDBOSS3_P1_SECOND_SPREAD, MIDBOSS3_P1_SECOND_DELTA, MIDBOSS3_P1_STACK_COUNT, 0.5f);", leaf)
        self.assertIn("midboss3_set_spread_stack(MIDBOSS3_P1_THIRD_SPREAD, MIDBOSS3_P1_THIRD_DELTA, MIDBOSS3_P1_STACK_COUNT, 0.5f);", leaf)
        self.assertEqual((number("MIDBOSS3_P1_FIRST_SPREAD"), number("MIDBOSS3_P1_FIRST_DELTA"), number("MIDBOSS3_P1_STACK_COUNT")), (3, 16, 4))
        self.assertEqual((number("MIDBOSS3_P1_SECOND_SPREAD"), number("MIDBOSS3_P1_SECOND_DELTA")), (4, 5))
        self.assertEqual((number("MIDBOSS3_P1_THIRD_SPREAD"), number("MIDBOSS3_P1_THIRD_DELTA")), (7, 10))
        self.assertIn("bullet_template.speed.v = midboss3_speed(1.5f);", leaf)
        self.assertIn("bullet_template.speed.v = midboss3_speed(3.0f);", leaf)
        self.assertIn("bullet_template.speed.v = midboss3_speed(2.0f);", leaf)
        self.assertIn("bullet_template.angle = MIDBOSS3_P1_INITIAL_ANGLE;", leaf)
        self.assertEqual(number("MIDBOSS3_P1_INITIAL_ANGLE"), 0x40)

    def test_pattern_two_uses_aimed_stack_then_two_rank_specific_spreads(self):
        leaf = function(PATTERNS, "midboss3_pattern_2", "midboss3_pattern_3")
        self.assertIn("bullet_template.group = BG_STACK_AIMED;", leaf)
        self.assertIn("midboss3_set_stack(MIDBOSS3_P2_STACK_COUNT, 0.5f);", leaf)
        self.assertIn("bullet_template.group = BG_SPREAD_STACK_AIMED;", leaf)
        self.assertIn("midboss3_set_spread_for_rank(MIDBOSS3_P2F_E_COUNT, MIDBOSS3_P2F_E_STEP, MIDBOSS3_P2F_N_COUNT, MIDBOSS3_P2F_N_STEP, MIDBOSS3_P2F_H_COUNT, MIDBOSS3_P2F_H_STEP, MIDBOSS3_P2F_L_COUNT, MIDBOSS3_P2F_L_STEP);", leaf)
        self.assertIn("midboss3_set_spread_for_rank(MIDBOSS3_P2T_E_COUNT, MIDBOSS3_P2T_E_STEP, MIDBOSS3_P2T_N_COUNT, MIDBOSS3_P2T_N_STEP, MIDBOSS3_P2T_H_COUNT, MIDBOSS3_P2T_H_STEP, MIDBOSS3_P2T_L_COUNT, MIDBOSS3_P2T_L_STEP);", leaf)
        self.assertEqual([number("MIDBOSS3_P2F_" + suffix) for suffix in ("E_COUNT", "E_STEP", "N_COUNT", "N_STEP", "H_COUNT", "H_STEP", "L_COUNT", "L_STEP")], [1, 1, 2, 4, 3, 3, 4, 4])
        self.assertEqual([number("MIDBOSS3_P2T_" + suffix) for suffix in ("E_COUNT", "E_STEP", "N_COUNT", "N_STEP", "H_COUNT", "H_STEP", "L_COUNT", "L_STEP")], [1, 1, 3, 5, 4, 5, 5, 4])
        self.assertEqual(number("MIDBOSS3_P2_STACK_COUNT"), 8)
        self.assertNotIn("bullet_template_tune();", leaf)

    def test_pattern_three_uses_three_diamond_spread_shapes_and_real_tuning(self):
        leaf = function(PATTERNS, "midboss3_pattern_3")
        self.assertIn("bullet_template.patnum = MIDBOSS3_PAT_DIAMOND_BLUE;", leaf)
        self.assertIn("bullet_template.speed.v = midboss3_speed(3.0f);", leaf)
        self.assertIn("bullet_template.angle = MIDBOSS3_P1_INITIAL_ANGLE;", leaf)
        self.assertEqual((number("MIDBOSS3_P3_FIRST_SPREAD"), number("MIDBOSS3_P3_FIRST_DELTA")), (16, 8))
        self.assertEqual((number("MIDBOSS3_P3_SECOND_SPREAD"), number("MIDBOSS3_P3_SECOND_DELTA")), (21, 4))
        self.assertIn("bullet_template.spread = MIDBOSS3_P3_FIRST_SPREAD;", leaf)
        self.assertIn("bullet_template.spread_angle_delta = MIDBOSS3_P3_FIRST_DELTA;", leaf)
        self.assertIn("bullet_template.spread = MIDBOSS3_P3_SECOND_SPREAD;", leaf)
        self.assertIn("bullet_template.spread_angle_delta = MIDBOSS3_P3_SECOND_DELTA;", leaf)
        self.assertIn("bullet_template_tune();", leaf)

    def test_every_pattern_charges_before_frame_thirty_two_and_repositions_at_ninety_six(self):
        for name, next_name in (("midboss3_pattern_1", "midboss3_pattern_2"),
                                ("midboss3_pattern_2", "midboss3_pattern_3")):
            leaf = function(PATTERNS, name, next_name)
            self.assertIn("if(midboss.phase_frame < MIDBOSS3_CHARGE_FRAMES)", leaf)
            self.assertIn("midboss3_gather_charge();", leaf)
            self.assertIn("if(midboss.phase_frame >= MIDBOSS3_PATTERN_REPOSITION_FRAME)", leaf)
            self.assertIn("midboss3_reposition();", leaf)
        leaf = function(PATTERNS, "midboss3_pattern_3")
        self.assertIn("if(midboss.phase_frame < MIDBOSS3_CHARGE_FRAMES)", leaf)
        self.assertIn("if(midboss.phase_frame >= MIDBOSS3_PATTERN_REPOSITION_FRAME)", leaf)
        self.assertEqual(number("MIDBOSS3_PATTERN_REPOSITION_FRAME"), 96)

    def test_controller_runs_twelve_attacks_in_four_complete_three_pattern_cycles(self):
        budget = number("MIDBOSS3_PATTERNS_MAX")
        self.assertEqual(budget, 12)
        pattern = number("MIDBOSS3_ATTACK_SPREAD_STACKS")
        done = 1
        executed = []
        while done <= budget:
            executed.append(pattern)
            pattern = (done % 3) + number("MIDBOSS3_ATTACK_SPREAD_STACKS")
            done += 1
            if done >= budget + 1:
                break
        self.assertEqual(executed, [1, 2, 3] * 4)
        self.assertEqual(done, 13)
        update = UPDATE[UPDATE.index("case MIDBOSS3_PHASE_ATTACKS:"):UPDATE.index("explode:")]
        self.assertIn("midboss3_pattern = (midboss3_patterns_done % 3) + MIDBOSS3_ATTACK_SPREAD_STACKS;", update)
        self.assertLess(update.index("midboss3_pattern = (midboss3_patterns_done % 3)"), update.index("midboss3_patterns_done++;"))
        self.assertIn("if(midboss3_patterns_done >= (MIDBOSS3_PATTERNS_MAX + 1))", update)
        self.assertIn("goto explode;", update)

    def test_entrance_and_timeout_defeat_preserve_hp_reward_distinction(self):
        update = UPDATE[UPDATE.index("void pascal far midboss3_update(void)"):]
        entrance = update[update.index("case MIDBOSS3_PHASE_ENTRANCE:"):update.index("case MIDBOSS3_PHASE_ATTACKS:")]
        self.assertIn("if(midboss.phase_frame >= 192)", entrance)
        self.assertIn("midboss3_pattern = MIDBOSS3_ATTACK_SPREAD_STACKS;", entrance)
        self.assertIn("midboss3_patterns_done = 1;", entrance)
        attacks = update[update.index("case MIDBOSS3_PHASE_ATTACKS:"):update.index("explode:")]
        self.assertLess(attacks.index("if(midboss3_patterns_done >= (MIDBOSS3_PATTERNS_MAX + 1))"), attacks.index("if(midboss.sprite < MIDBOSS3_SPRITE_INVINCIBLE)"))
        self.assertLess(attacks.index("if(midboss.hp > 0)"), attacks.index("bullet_zap.active = true;"))
        self.assertIn("midboss_score_bonus(15);", attacks)
        self.assertIn("items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_1UP);", attacks)

    def test_sprite_threshold_controls_vulnerability_during_disappear_and_return(self):
        update = UPDATE[UPDATE.index("if(midboss.sprite < MIDBOSS3_SPRITE_INVINCIBLE)"):UPDATE.index("if(midboss.hp > 0)")]
        self.assertIn("stage3_midboss_hittest_shots(to_sp(24), to_sp(24));", update)
        invincible = number("MIDBOSS3_SPRITE_INVINCIBLE")
        disappear = [209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 219]
        return_path = [218, 217, 216, 215, 214, 213, 212, 208]
        self.assertEqual([sprite < invincible for sprite in disappear], [True, True, True] + [False] * 9)
        self.assertEqual([sprite < invincible for sprite in return_path], [False] * 7 + [True])

    def test_explosion_tail_uses_big_phase_sprite_sparks_and_shared_defeat_update(self):
        explode = UPDATE[UPDATE.index("explode:"):]
        self.assertIn("midboss.phase = MIDBOSS3_PHASE_EXPLODE_BIG;", explode)
        self.assertIn("midboss.sprite = MIDBOSS3_SPRITE_EXPLODE;", explode)
        self.assertIn("midboss.phase_frame = 0;", explode)
        self.assertIn("sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(8), 48);", explode)
        self.assertIn("snd_se_play(12);", explode)
        self.assertIn("midboss_defeat_update();", explode)
        self.assertIn("hud_hp_update_and_render(midboss.hp, MIDBOSS3_HP_TOTAL);", explode)


if __name__ == "__main__":
    unittest.main()
