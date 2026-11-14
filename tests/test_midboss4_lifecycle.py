"""Stage-four midboss's complete 798-byte update and three pattern leaves."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
STAGE4 = (ROOT / "src/main/midboss/stage4.cpp").read_text()
STAGE4_HPP = (ROOT / "src/main/midboss/stage4.hpp").read_text()
SCRATCH = (ROOT / "src/main/midboss/stage4_scratch.hpp").read_text()
TRANSITION = (ROOT / "src/main/midboss/transition4.cpp").read_text()


def number(name):
    match = re.search(rf"\b{name}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)", STAGE4 + STAGE4_HPP)
    if not match:
        raise AssertionError(f"missing Stage 4 constant {name}")
    return int(match.group(1), 0)


def function(name, next_name):
    start = STAGE4.index(f"void near {name}(void)")
    end = STAGE4.index(f"void near {next_name}(void)", start + 1)
    return STAGE4[start:end]


def stage4_pattern_sequence(budget):
    pattern = number("MIDBOSS4_PATTERN_RANDOM_CLOUDS")
    done = 0
    executed = []
    while True:
        executed.append(pattern)
        done += 1
        pattern = (done % number("MIDBOSS4_PATTERN_VARIANT_MODULUS")) + number("MIDBOSS4_PATTERN_RANDOM_CLOUDS")
        if done >= budget:
            return executed, done, pattern


class Midboss4LifecycleTests(unittest.TestCase):
    def test_random_cloud_attack_telegraph_and_five_inclusive_volleys(self):
        leaf = function("midboss4_pattern_random_clouds", "midboss4_pattern_spiral_rings")
        self.assertIn("if(midboss.phase_frame == MIDBOSS4_PATTERN_CHARGE_FRAME)", leaf)
        self.assertIn("snd_se_play(MIDBOSS4_CHARGE_SOUND);", leaf)
        self.assertIn("bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;", leaf)
        self.assertIn("bullet_template.spread = MIDBOSS4_CLOUD_SPREAD_COUNT;", leaf)
        self.assertIn("midboss.sprite = MIDBOSS4_SPRITE_CAST;", leaf)
        first, last, cadence = (number("MIDBOSS4_PATTERN_VOLLEY_FIRST"),
                                number("MIDBOSS4_PATTERN_VOLLEY_LAST"),
                                number("MIDBOSS4_CLOUD_VOLLEY_CADENCE"))
        frames = [f for f in range(first, last + 1) if f % cadence == 0]
        self.assertEqual(frames, [48, 56, 64, 72, 80])
        self.assertIn("bullet_template.speed.v = MIDBOSS4_CLOUD_INITIAL_SPEED_SP;", leaf)
        self.assertIn("for(int i = 0; i < MIDBOSS4_CLOUD_BULLET_COUNT; i++)", leaf)
        self.assertIn("bullet_template.speed.v += to_sp(MIDBOSS4_CLOUD_SPEED_STEP_PX);", leaf)
        self.assertIn("bullet_template.patnum = ((i & 1) ? MIDBOSS4_V_BLUE : 0);", leaf)
        self.assertEqual(number("MIDBOSS4_CLOUD_BULLET_COUNT"), 4)
        self.assertEqual(number("MIDBOSS4_CLOUD_INITIAL_SPEED_SP"), 8)
        self.assertEqual(number("MIDBOSS4_CLOUD_SPEED_STEP_PX"), 1)
        self.assertEqual([8 + 16 * i for i in range(4)], [8, 24, 40, 56])
        self.assertEqual(len(frames) * number("MIDBOSS4_CLOUD_BULLET_COUNT"), 20)

    def test_random_cloud_spawn_rectangle_and_alternating_pattern_slots(self):
        leaf = function("midboss4_pattern_random_clouds", "midboss4_pattern_spiral_rings")
        self.assertIn("randring2_next16_mod(to_sp(MIDBOSS4_CLOUD_ORIGIN_RANGE_PX))", leaf)
        self.assertIn("midboss.pos.cur.x.v - to_sp(MIDBOSS4_CLOUD_ORIGIN_X_OFFSET_PX)", leaf)
        self.assertIn("midboss.pos.cur.y.v - to_sp(MIDBOSS4_CLOUD_ORIGIN_Y_OFFSET_PX)", leaf)
        self.assertEqual(number("MIDBOSS4_CLOUD_ORIGIN_RANGE_PX"), 48)
        self.assertEqual(number("MIDBOSS4_CLOUD_ORIGIN_X_OFFSET_PX"), 24)
        self.assertEqual(number("MIDBOSS4_CLOUD_ORIGIN_Y_OFFSET_PX"), 32)
        slots = [((i & 1) != 0) for i in range(number("MIDBOSS4_CLOUD_BULLET_COUNT"))]
        self.assertEqual(slots, [False, True, False, True])

    def test_spiral_ring_attack_alternates_fast_cloud_and_slow_normal_ring(self):
        leaf = function("midboss4_pattern_spiral_rings", "midboss4_pattern_aimed_stacks")
        self.assertIn("bullet_template.group = BG_RING;", leaf)
        self.assertIn("bullet_template.spread = MIDBOSS4_RING_BULLET_COUNT;", leaf)
        self.assertIn("bullet_template.patnum = MIDBOSS4_V_RED;", leaf)
        self.assertEqual(number("MIDBOSS4_RING_BULLET_COUNT"), 16)
        first, last = number("MIDBOSS4_PATTERN_VOLLEY_FIRST"), number("MIDBOSS4_PATTERN_VOLLEY_LAST")
        cadence = number("MIDBOSS4_RING_VOLLEY_CADENCE")
        alternate = number("MIDBOSS4_SPIRAL_ALTERNATE_CADENCE")
        frames = [f for f in range(first, last + 1) if f % cadence == 0]
        self.assertEqual(frames, [48, 52, 56, 60, 64, 68, 72, 76, 80])
        fast = [f for f in frames if f % alternate == 0]
        slow = [f for f in frames if f % alternate != 0]
        self.assertEqual((fast, slow), ([48, 56, 64, 72, 80], [52, 60, 68, 76]))
        self.assertIn("bullet_template.speed.v = to_sp(MIDBOSS4_SPIRAL_FAST_SPEED_PX) + MIDBOSS4_SPIRAL_BASE_SPEED_SP;", leaf)
        self.assertIn("bullet_template.speed.v = to_sp(MIDBOSS4_SPIRAL_SLOW_SPEED_PX) + MIDBOSS4_SPIRAL_BASE_SPEED_SP;", leaf)
        self.assertIn("bullet_template.spawn_type = MIDBOSS4_CLOUD_FORWARDS;", leaf)
        self.assertIn("bullet_template.spawn_type = BST_NORMAL;", leaf)
        self.assertIn("bullet_template.angle += MIDBOSS4_SPIRAL_ANGLE_STEP;", leaf)
        self.assertEqual((number("MIDBOSS4_SPIRAL_FAST_SPEED_PX"),
                          number("MIDBOSS4_SPIRAL_SLOW_SPEED_PX"),
                          number("MIDBOSS4_SPIRAL_BASE_SPEED_SP")), (3, 2, 8))
        self.assertEqual((3 * 16 + 8, 2 * 16 + 8), (56, 40))

    def test_aimed_stack_attack_packs_four_semantic_fields_and_updates_angle_speed(self):
        leaf = STAGE4[STAGE4.index("void near midboss4_pattern_aimed_stacks(void)"):STAGE4.index("void pascal far midboss4_update(void)")]
        self.assertIn("bullet_template.group = BG_SPREAD_STACK_AIMED;", leaf)
        self.assertIn("bullet_template.angle = MIDBOSS4_STACK_INITIAL_ANGLE;", leaf)
        self.assertIn("3UL | (8UL << 8) | (4UL << 16) | (4UL << 24)", leaf)
        self.assertIn("bullet_template.speed.v = to_sp(MIDBOSS4_STACK_BASE_SPEED_PX);", leaf)
        self.assertIn("bullet_template.speed.v += MIDBOSS4_STACK_SPEED_STEP_SP;", leaf)
        self.assertIn("bullet_template.angle -= MIDBOSS4_STACK_ANGLE_STEP;", leaf)
        self.assertEqual((number("MIDBOSS4_STACK_INITIAL_ANGLE"),
                          number("MIDBOSS4_STACK_BASE_SPEED_PX"),
                          number("MIDBOSS4_STACK_SPEED_STEP_SP"),
                          number("MIDBOSS4_STACK_ANGLE_STEP")), (0x20, 1, 12, 8))
        angles = [(0x20 - 8 * i) & 0xFF for i in range(9)]
        speeds = [16 + 12 * i for i in range(9)]
        self.assertEqual(angles, [0x20, 0x18, 0x10, 0x08, 0x00, 0xF8, 0xF0, 0xE8, 0xE0])
        self.assertEqual(speeds, [16, 28, 40, 52, 64, 76, 88, 100, 112])

    def test_all_three_patterns_finish_inclusively_at_frame_ninety_six(self):
        end = number("MIDBOSS4_PATTERN_FINISH_FRAME")
        self.assertEqual(end, 96)
        leaves = [
            function("midboss4_pattern_random_clouds", "midboss4_pattern_spiral_rings"),
            function("midboss4_pattern_spiral_rings", "midboss4_pattern_aimed_stacks"),
            STAGE4[STAGE4.index("void near midboss4_pattern_aimed_stacks(void)"):STAGE4.index("void pascal far midboss4_update(void)")],
        ]
        for leaf in leaves:
            self.assertIn("if(midboss.phase_frame >= MIDBOSS4_PATTERN_FINISH_FRAME)", leaf)
            self.assertIn("midboss.sprite = MIDBOSS4_SPRITE_STILL;", leaf)
            self.assertIn("midboss.phase_frame = 0;", leaf)
            self.assertIn("pattern = MIDBOSS4_PATTERN_TRANSITION;", leaf)

    def test_pattern_dispatch_runs_six_clouds_five_spirals_five_stacks_before_defeat(self):
        budget = number("MIDBOSS4_PATTERN_BUDGET")
        sequence, done, pending = stage4_pattern_sequence(budget)
        self.assertEqual(budget, 16)
        self.assertEqual(len(sequence), 16)
        self.assertEqual((sequence.count(1), sequence.count(2), sequence.count(3)), (6, 5, 5))
        self.assertEqual((done, pending), (16, 2))
        update = STAGE4[STAGE4.index("void pascal far midboss4_update(void)"):]
        self.assertIn("pattern = ((patterns_done % MIDBOSS4_PATTERN_VARIANT_MODULUS) + MIDBOSS4_PATTERN_RANDOM_CLOUDS);", update)
        self.assertLess(update.index("patterns_done++;"), update.index("if(patterns_done >= MIDBOSS4_PATTERN_BUDGET)"))
        self.assertLess(update.index("pattern = ((patterns_done % MIDBOSS4_PATTERN_VARIANT_MODULUS)"),
                        update.index("if(patterns_done >= MIDBOSS4_PATTERN_BUDGET)"))

    def test_entrance_activates_vulnerability_and_enters_pattern_one_after_192_frames(self):
        update = STAGE4[STAGE4.index("void pascal far midboss4_update(void)"):]
        self.assertIn("midboss.phase_frame++;", update)
        entrance = update[update.index("case MIDBOSS4_PHASE_ENTRANCE:"):update.index("case MIDBOSS4_PHASE_PATTERNS:")]
        self.assertIn("if(midboss.phase_frame == MIDBOSS4_ENTRANCE_FIRST_FRAME)", entrance)
        self.assertIn("vulnerable = 1;", entrance)
        self.assertIn("midboss.pos.update_seg3();", entrance)
        self.assertIn("midboss_hittest_shots_damage(to_sp(MIDBOSS4_HIT_RADIUS_PIXELS), to_sp(MIDBOSS4_HIT_RADIUS_PIXELS), MIDBOSS4_HIT_EFFECT);", entrance)
        self.assertIn("if(midboss.phase_frame >= MIDBOSS4_ENTRANCE_END_FRAME)", entrance)
        self.assertIn("pattern = MIDBOSS4_PATTERN_RANDOM_CLOUDS;", entrance)
        self.assertIn("patterns_done = 0;", entrance)
        self.assertIn("midboss.pos.velocity.x.v = 0;", entrance)
        self.assertEqual((number("MIDBOSS4_ENTRANCE_FIRST_FRAME"), number("MIDBOSS4_ENTRANCE_END_FRAME")), (1, 192))

    def test_vulnerability_gate_precedes_hp_defeat_and_budget_timeout_skips_hit_reward(self):
        update = STAGE4[STAGE4.index("case MIDBOSS4_PHASE_PATTERNS:"):]
        positions = [
            update.index("if(midboss4_pattern_transition())"),
            update.index("if(vulnerable)"),
            update.index("stage4_midboss_hittest_shots("),
            update.index("if(midboss.hp > 0)"),
            update.index("bullet_zap.active = true;"),
            update.index("midboss_score_bonus(MIDBOSS4_DEFEAT_SCORE_UNITS);"),
            update.index("items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_BOMB);"),
            update.index("defeat:"),
        ]
        self.assertEqual(positions, sorted(positions))
        budget_branch = update[update.index("if(patterns_done >= MIDBOSS4_PATTERN_BUDGET)"):update.index("if(vulnerable)")]
        self.assertIn("goto defeat;", budget_branch)
        self.assertNotIn("bullet_zap.active = true;", budget_branch)
        self.assertNotIn("midboss_score_bonus(", budget_branch)
        self.assertNotIn("items_add(", budget_branch)

    def test_defeat_dispatch_sets_big_explosion_sparks_and_shared_tail(self):
        update = STAGE4[STAGE4.index("defeat:"):]
        self.assertIn("midboss.phase = MIDBOSS4_PHASE_EXPLODE_BIG;", update)
        self.assertIn("midboss.sprite = MIDBOSS4_SPRITE_EXPLODE;", update)
        self.assertIn("midboss.phase_frame = 0;", update)
        self.assertIn("sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(MIDBOSS4_DEFEAT_SPARK_RADIUS_PX), MIDBOSS4_DEFEAT_SPARK_COUNT);", update)
        self.assertIn("snd_se_play(MIDBOSS4_DEFEAT_SOUND);", update)
        self.assertEqual((number("MIDBOSS4_DEFEAT_SPARK_RADIUS_PX"),
                          number("MIDBOSS4_DEFEAT_SPARK_COUNT"),
                          number("MIDBOSS4_DEFEAT_SOUND")), (8, 48, 12))
        default = update[update.index("default:"):]
        self.assertIn("midboss_defeat_update();", default)
        self.assertIn("hud_hp_update_and_render(midboss.hp, MIDBOSS4_HP_TOTAL);", default)
        self.assertIn("return;", default)


if __name__ == "__main__":
    unittest.main()
