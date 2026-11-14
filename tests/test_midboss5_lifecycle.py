"""Stage-five midboss's 318-byte controller and 462-byte attack prefix."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/midboss/stage5.cpp").read_text()
PATTERNS = (ROOT / "src/main/midboss/stage5_patterns.cpp").read_text()
PATTERN_TABLE = (ROOT / "src/main/midboss/stage5_schedule_data.cpp").read_text()
RULES = (ROOT / "src/main/midboss/stage5_attack_rules.hpp").read_text()
HEADER = (ROOT / "src/main/midboss/stage5.hpp").read_text()
PATTERN_HPP = (ROOT / "src/main/midboss/stage5_patterns.hpp").read_text()
SCRATCH = (ROOT / "src/main/midboss/stage5_scratch.hpp").read_text()


def value(name):
    for source in (RULES, HEADER, PATTERN_HPP, SCRATCH, UPDATE, PATTERNS):
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("#define " + name + " "):
                return float(stripped.split(None, 2)[2].strip().rstrip("f"))
            needle = name + " = "
            if needle in line:
                raw = line.split(needle, 1)[1].split(";", 1)[0].strip()
                return int(raw, 0)
    raise AssertionError(f"missing Stage 5 constant {name}")


def function(source, name, next_name=None):
    def candidates(symbol):
        signatures = (
            f"bool near {symbol}(void)",
            f"void near {symbol}(void)",
            f"void pascal far {symbol}(void)",
        )
        return [source.index(signature) for signature in signatures if signature in source]
    starts = candidates(name)
    if not starts:
        raise AssertionError(f"missing function {name}")
    start = min(starts)
    if next_name is None:
        return source[start:]
    ends = [position for position in candidates(next_name) if position > start]
    if not ends:
        raise AssertionError(f"missing function boundary {next_name}")
    return source[start:min(ends)]


def stage5_sequence(budget):
    table = ["blue", "green", "aimed"]
    current = 0
    done = 0
    executed = []
    while True:
        executed.append(table[current])
        done += 1
        current = done % 3
        if done >= budget:
            return executed, done, table[current]


class Midboss5LifecycleTests(unittest.TestCase):
    def test_flystep_cycles_left_right_right_left_and_completes_at_frame_thirty_two(self):
        leaf = function(PATTERNS, "midboss5_flystep", "midboss5_pattern_update")
        self.assertIn("if(midboss.phase_frame == M5R_INITIAL_FLY_FRAME)", leaf)
        self.assertIn("M5R_LEFT_STEP_INDEX", leaf)
        self.assertIn("M5R_LAST_LEFT_STEP_INDEX", leaf)
        self.assertIn("midboss5_scratch.horizontal_step++", leaf)
        self.assertIn("midboss5_scratch.horizontal_step &= M5R_STEP_INDEX_MASK;", leaf)
        self.assertIn("midboss.pos.update_seg3();", leaf)
        self.assertIn("if(midboss.phase_frame >= M5R_DASH_FRAME_LIMIT)", leaf)
        self.assertEqual((value("M5R_DASH_FRAME_LIMIT"), value("M5R_DASH_SPEED_PX"), value("M5R_STEP_INDEX_MASK")), (32, 2, 3))
        directions = [-2 if step in (0, 3) else 2 for step in range(4)]
        self.assertEqual(directions, [-2, 2, 2, -2])
        self.assertEqual([(step + 1) & 3 for step in range(4)], [1, 2, 3, 0])

    def test_charge_uses_frame_minus_sixteen_and_animates_at_twenty_twenty_four_twenty_eight(self):
        leaf = function(PATTERNS, "midboss5_pattern_update", "midboss5_pattern_blue_spread")
        self.assertIn("if(midboss.phase_frame < M5R_PATTERN_START_FRAME)", leaf)
        self.assertIn("gather_add_only_3stack(midboss.phase_frame - M5R_CHARGE_FRAME, M5R_CHARGE_GATHER_FIRST_COLOR, M5R_CHARGE_GATHER_OTHER_COLOR);", leaf)
        self.assertIn("if(midboss.phase_frame == M5R_CHARGE_FRAME)", leaf)
        self.assertIn("snd_se_play(M5R_CHARGE_SOUND);", leaf)
        self.assertIn("bullet_template.angle = player_angle_from(", leaf)
        self.assertEqual((value("M5R_CHARGE_FRAME"), value("M5R_CHARGE_GATHER_FIRST_COLOR"), value("M5R_CHARGE_GATHER_OTHER_COLOR"), value("M5R_CHARGE_SOUND")), (16, 3, 2, 8))
        self.assertEqual([f for f in (20, 24, 28) if f in (value("M5R_SHOOT_SPRITE_FRAME_A"), value("M5R_SHOOT_SPRITE_FRAME_B"), value("M5R_SHOOT_SPRITE_FRAME_C"))], [20, 24, 28])
        self.assertEqual((value("M5R_PATTERN_START_FRAME"), value("M5R_SPRITE_ANIMATION_INTERVAL")), (32, 4))
        self.assertIn("if((midboss.phase_frame == M5R_SHOOT_SPRITE_FRAME_A) ||", leaf)

    def test_blue_spread_emits_seventeen_inclusive_thirteen_way_volleys(self):
        leaf = function(PATTERNS, "midboss5_pattern_blue_spread", "midboss5_pattern_green_rings")
        frames = [f for f in range(32, 97) if f % value("M5R_BLUE_FIRE_INTERVAL") == 0]
        self.assertEqual(frames, list(range(32, 97, 4)))
        self.assertEqual(len(frames), 17)
        self.assertEqual((value("M5R_BLUE_SPREAD_COUNT"), value("M5R_BLUE_SPREAD_STEP"), value("M5R_BLUE_SHOT_SPEED_PX")), (13, 7, 5.5))
        self.assertIn("MIDBOSS5_SPAWN_CLOUD_FORWARDS | MIDBOSS5_SPAWN_NO_DECELERATE", leaf)
        self.assertIn("MIDBOSS5_PAT_BULLET_V_BLUE", leaf)
        self.assertIn("midboss5_speed(M5R_BLUE_SHOT_SPEED_PX)", leaf)
        self.assertIn("midboss5_set_spread(M5R_BLUE_SPREAD_COUNT, M5R_BLUE_SPREAD_STEP);", leaf)
        self.assertIn("return (midboss.phase_frame >= M5R_BLUE_LAST_FRAME);", leaf)
        self.assertEqual(value("M5R_BLUE_LAST_FRAME"), 96)

    def test_green_rings_emit_seventeen_sixteen_bullet_rings_with_independent_rng(self):
        leaf = function(PATTERNS, "midboss5_pattern_green_rings", "midboss5_pattern_aimed_stacks")
        frames = [f for f in range(32, 97) if f % value("M5R_GREEN_FIRE_INTERVAL") == 0]
        self.assertEqual((len(frames), frames[0], frames[-1]), (17, 32, 96))
        self.assertEqual((value("M5R_GREEN_RING_COUNT"), value("M5R_GREEN_SPEED_PX")), (16, 2.0))
        self.assertIn("bullet_template.group = BG_RING;", leaf)
        self.assertIn("MIDBOSS5_PAT_BULLET_D_GREEN", leaf)
        self.assertEqual(leaf.count("randring2_next16_mod(to_sp(M5R_GREEN_POSITION_JITTER_PX))"), 2)
        self.assertIn("bullet_template.angle = randring2_next16();", leaf)
        self.assertIn("snd_se_play(3);", leaf)
        self.assertNotIn("bullet_template_tune();", leaf)
        self.assertEqual((value("M5R_GREEN_POSITION_JITTER_PX"), value("M5R_GREEN_POSITION_BIAS_PX")), (64, 32))
        self.assertEqual((-32, 32), (-value("M5R_GREEN_POSITION_BIAS_PX"), value("M5R_GREEN_POSITION_JITTER_PX") - value("M5R_GREEN_POSITION_BIAS_PX")))

    def test_aimed_pattern_fires_one_spread_stack_then_one_ring_stack_at_frame_thirty_two(self):
        leaf = function(PATTERNS, "midboss5_pattern_aimed_stacks")
        self.assertIn("if(midboss.phase_frame == M5R_AIMED_FIRE_FRAME)", leaf)
        self.assertIn("bullet_template.group = BG_SPREAD_STACK_AIMED;", leaf)
        self.assertIn("midboss5_set_spread_stack(M5R_AIMED_SPREAD_COUNT, M5R_AIMED_SPREAD_STEP, M5R_AIMED_STACK_COUNT, M5R_AIMED_STACK_STEP);", leaf)
        self.assertIn("bullet_template.group = BG_RING_STACK_AIMED;", leaf)
        self.assertIn("bullet_template.stack_speed_delta.v = midboss5_speed(M5R_AIMED_RING_STEP);", leaf)
        self.assertIn("bullet_template.spread = M5R_AIMED_RING_COUNT;", leaf)
        self.assertEqual((value("M5R_AIMED_FIRE_FRAME"), value("M5R_AIMED_SPREAD_COUNT"), value("M5R_AIMED_SPREAD_STEP"), value("M5R_AIMED_STACK_COUNT")), (32, 5, 10, 5))
        self.assertEqual((value("M5R_AIMED_STACK_STEP"), value("M5R_AIMED_SPEED_PX"), value("M5R_AIMED_RING_COUNT"), value("M5R_AIMED_RING_STEP")), (0.375, 2.0, 32, 0.25))
        self.assertEqual(leaf.count("bullets_add_regular();"), 2)
        self.assertIn("return (midboss.phase_frame >= M5R_AIMED_LAST_FRAME);", leaf)
        self.assertEqual(value("M5R_AIMED_LAST_FRAME"), 64)

    def test_pattern_table_is_three_near_callbacks_in_blue_green_aimed_order(self):
        self.assertIn("const midboss5_pattern_func_t near MIDBOSS5_PATTERNS[3]", PATTERN_TABLE)
        order = [
            "midboss5_pattern_blue_spread,",
            "midboss5_pattern_green_rings,",
            "midboss5_pattern_aimed_stacks",
        ]
        positions = [PATTERN_TABLE.index(item) for item in order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("sizeof(midboss5_pattern_func_t) == 2", HEADER)
        self.assertIn("sizeof(MIDBOSS5_PATTERNS) == 6", HEADER)
        self.assertIn("extern midboss5_pattern_func_t midboss5_pattern_func;", HEADER)

    def test_sixteen_executed_attacks_are_six_blue_five_green_five_aimed(self):
        executed, done, pending = stage5_sequence(value("MIDBOSS5_PATTERNS_MAX"))
        self.assertEqual(value("MIDBOSS5_PATTERNS_MAX"), 16)
        self.assertEqual(len(executed), 16)
        self.assertEqual((executed.count("blue"), executed.count("green"), executed.count("aimed")), (6, 5, 5))
        self.assertEqual((done, pending), (16, "green"))
        self.assertIn("midboss5_pattern_func = MIDBOSS5_PATTERNS[midboss5_patterns_done % M5R_PATTERN_ROTATION_COUNT];", UPDATE)
        self.assertIn("if(midboss5_patterns_done >= MIDBOSS5_PATTERNS_MAX)", UPDATE)

    def test_controller_entrance_initializes_blue_pattern_and_all_three_scratch_bytes(self):
        update = function(UPDATE, "midboss5_update")
        entrance = update[update.index("case MIDBOSS5_PHASE_ENTRANCE:"):update.index("case MIDBOSS5_PHASE_PATTERNS:")]
        self.assertIn("if(midboss.phase_frame >= M5R_ENTRANCE_FRAMES)", entrance)
        self.assertEqual(value("M5R_ENTRANCE_FRAMES"), 192)
        self.assertIn("midboss5_scratch.horizontal_step = 0;", entrance)
        self.assertIn("midboss5_pattern_phase = MIDBOSS5_MODE_ATTACK;", entrance)
        self.assertIn("midboss5_patterns_done = 0;", entrance)
        self.assertIn("midboss5_pattern_func = midboss5_pattern_blue_spread;", entrance)
        self.assertIn("midboss.pos.velocity.y.v = 0;", entrance)
        self.assertIn("midboss_hittest_shots_damage(to_sp(M5R_HIT_RADIUS_PX), to_sp(M5R_HIT_RADIUS_PX), M5R_HIT_ENTRY_SOUND);", entrance)
        self.assertEqual((value("M5R_HIT_RADIUS_PX"), value("M5R_HIT_ENTRY_SOUND")), (24, 10))

    def test_flystep_completion_advances_pattern_before_terminal_budget_check(self):
        update = function(UPDATE, "midboss5_update")
        phase = update[update.index("case MIDBOSS5_PHASE_PATTERNS:"):update.index("default:")]
        self.assertLess(phase.index("if(midboss5_flystep())"), phase.index("midboss5_patterns_done++;"))
        self.assertLess(phase.index("midboss5_patterns_done++;"), phase.index("midboss5_pattern_func = MIDBOSS5_PATTERNS"))
        self.assertLess(phase.index("midboss5_pattern_func = MIDBOSS5_PATTERNS"), phase.index("midboss5_pattern_phase++;"))
        self.assertLess(phase.index("midboss5_pattern_phase++;"), phase.index("if(midboss5_patterns_done >= MIDBOSS5_PATTERNS_MAX)"))
        self.assertIn("midboss.phase_frame = 0;", phase)
        self.assertIn("goto explode;", phase)

    def test_hp_defeat_rewards_but_sixteen_pattern_timeout_skips_hit_and_reward(self):
        update = function(UPDATE, "midboss5_update")
        phase = update[update.index("case MIDBOSS5_PHASE_PATTERNS:"):update.index("default:")]
        budget = phase[phase.index("if(midboss5_patterns_done >= MIDBOSS5_PATTERNS_MAX)"):phase.index("stage5_midboss_hittest_shots")]
        self.assertIn("goto explode;", budget)
        self.assertNotIn("bullet_zap.active = true;", budget)
        self.assertNotIn("midboss_score_bonus(", budget)
        self.assertNotIn("items_add(", budget)
        self.assertLess(phase.index("stage5_midboss_hittest_shots"), phase.index("if(midboss.hp > 0)"))
        self.assertLess(phase.index("if(midboss.hp > 0)"), phase.index("bullet_zap.active = true;"))
        self.assertIn("midboss_score_bonus(M5R_DEFEAT_SCORE_BONUS);", phase)
        self.assertIn("items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_1UP);", phase)
        self.assertEqual(value("M5R_DEFEAT_SCORE_BONUS"), 30)

    def test_scratch_offsets_and_explosion_tail_are_the_original_layout(self):
        self.assertIn("midboss5_patterns_at_13", SCRATCH)
        self.assertIn("midboss5_mode_at_14", SCRATCH)
        self.assertIn("midboss5_step_at_15", SCRATCH)
        self.assertIn("midboss5_scratch_is_16", SCRATCH)
        update = function(UPDATE, "midboss5_update")
        explode = update[update.index("explode:"):update.index("default:")]
        self.assertIn("midboss.phase = MIDBOSS5_PHASE_EXPLODE_BIG;", explode)
        self.assertIn("midboss.sprite = MIDBOSS5_SPRITE_EXPLODE;", explode)
        self.assertIn("sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(M5R_EXPLOSION_RADIUS_PX), M5R_EXPLOSION_SPARK_COUNT);", explode)
        self.assertIn("snd_se_play(M5R_EXPLOSION_SE);", explode)
        self.assertEqual((value("M5R_EXPLOSION_RADIUS_PX"), value("M5R_EXPLOSION_SPARK_COUNT"), value("M5R_EXPLOSION_SE")), (8, 48, 12))

    def test_default_defeat_returns_before_homing_target_publication(self):
        update = function(UPDATE, "midboss5_update")
        start = update.index("default:")
        default = update[start:update.index("return;", start) + len("return;")]
        self.assertIn("midboss_defeat_update();", default)
        self.assertIn("hud_hp_update_and_render(midboss.hp, MIDBOSS5_HP_TOTAL);", default)
        self.assertNotIn("homing_target.x", default)
        self.assertIn("homing_target.x = midboss.pos.cur.x;", update)


if __name__ == "__main__":
    unittest.main()
