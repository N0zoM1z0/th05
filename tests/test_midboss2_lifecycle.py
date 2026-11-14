"""Stage-two midboss orbit, attack payloads and three-phase handoff."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = (ROOT / "src/main/midboss/stage2_patterns.cpp").read_text()
UPDATE = (ROOT / "src/main/midboss/stage2.cpp").read_text()
STAGE2_HPP = (ROOT / "src/main/midboss/stage2.hpp").read_text()
SCRATCH = (ROOT / "src/main/midboss/stage2_scratch.hpp").read_text()


def number(name):
    for source in (PATTERNS, UPDATE, STAGE2_HPP, SCRATCH):
        needle = name + " = "
        for line in source.splitlines():
            if needle in line:
                value = line.split(needle, 1)[1].split(";", 1)[0].strip()
                return int(value, 0)
    raise AssertionError(f"missing Stage 2 constant {name}")


def function(source, name, next_name=None):
    start = source.index(f"void near {name}(void)")
    if next_name is None:
        return source[start:]
    end = source.index(f"void near {next_name}(void)", start + 1)
    return source[start:end]


def signed8(value):
    value &= 0xFF
    return value if value < 0x80 else value - 0x100


class Midboss2LifecycleTests(unittest.TestCase):
    def test_orbit_center_drift_uses_signed_byte_and_strict_128_256_bounds(self):
        leaf = function(PATTERNS, "midboss2_move", "midboss2_pattern")
        self.assertIn("static_cast<signed char>(midboss2_orbit_speed)", leaf)
        self.assertIn("if(midboss2_orbit_center.x.v < to_sp(MIDBOSS2_ORBIT_CENTER_LEFT_PX))", leaf)
        self.assertIn("else if(midboss2_orbit_center.x.v > to_sp(MIDBOSS2_ORBIT_CENTER_RIGHT_PX))", leaf)
        self.assertEqual((number("MIDBOSS2_ORBIT_CENTER_LEFT_PX"), number("MIDBOSS2_ORBIT_CENTER_RIGHT_PX"), number("MIDBOSS2_ORBIT_DRIFT_STEP")), (128, 256, 2))
        center_x = 192 * 16
        drift = 0x20
        trajectory = []
        for frame in range(1, 50):
            center_x += signed8(drift)
            if center_x < 128 * 16:
                drift = (drift + 2) & 0xFF
            elif center_x > 256 * 16:
                drift = (drift - 2) & 0xFF
            trajectory.append((center_x, signed8(drift)))
        self.assertEqual(trajectory[31], (256 * 16, 32))
        self.assertEqual(trajectory[32], (258 * 16, 30))
        self.assertEqual(trajectory[47], (273 * 16, 0))
        self.assertEqual(trajectory[48], (273 * 16, -2))
        self.assertEqual(signed8(0xFE), -2)
        self.assertEqual(signed8(0x80), -128)

    def test_orbit_radius_overshoots_64_then_contracts_to_one_pixel(self):
        leaf = function(PATTERNS, "midboss2_move", "midboss2_pattern")
        self.assertEqual((number("MIDBOSS2_ORBIT_RADIUS_STEP_PX"), number("MIDBOSS2_ORBIT_RADIUS_LIMIT_PX")), (1, 64))
        self.assertIn("if(midboss2_orbit_contracting == MIDBOSS2_ORBIT_EXPANDING)", leaf)
        self.assertIn("if(midboss.pos.velocity.x.v > to_sp(MIDBOSS2_ORBIT_RADIUS_LIMIT_PX))", leaf)
        self.assertIn("if(midboss.pos.velocity.x.v <= to_sp(MIDBOSS2_ORBIT_RADIUS_STEP_PX))", leaf)
        radius = 0
        direction = 0
        values = []
        for frame in range(1, 130):
            if direction == 0:
                radius += 16
                if radius > 64 * 16:
                    direction = 1
            else:
                radius -= 16
                if radius <= 1 * 16:
                    direction = 0
            values.append((radius, direction))
        self.assertEqual(values[63], (64 * 16, 0))
        self.assertEqual(values[64], (65 * 16, 1))
        self.assertEqual(values[128], (1 * 16, 0))

    def test_orbit_position_uses_old_center_radius_and_angle_before_state_advances(self):
        leaf = function(PATTERNS, "midboss2_move", "midboss2_pattern")
        order = [
            "midboss.pos.prev = midboss.pos.cur;",
            "vector2_at(midboss.pos.cur, midboss2_orbit_center.x.v,",
            "midboss2_orbit_center.x.v += static_cast<signed char>(midboss2_orbit_speed);",
            "if(midboss2_orbit_contracting == MIDBOSS2_ORBIT_EXPANDING)",
            "midboss.angle -= MIDBOSS2_ORBIT_ANGLE_STEP;",
        ]
        positions = [leaf.index(token) for token in order]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(number("MIDBOSS2_ORBIT_ANGLE_STEP"), 2)

    def test_regular_pattern_fires_two_payloads_only_on_global_sixteen_frame_ticks(self):
        leaf = function(PATTERNS, "midboss2_pattern", "midboss2_pattern_final")
        self.assertIn("if(stage_frame_mod16 == 0)", leaf)
        self.assertIn("bullet_template.spawn_type = MIDBOSS2_NO_DECEL_SPAWN;", leaf)
        self.assertIn("bullet_template.patnum = MIDBOSS2_RED_BALL_PATNUM;", leaf)
        self.assertIn("bullet_template.group = BG_STACK;", leaf)
        self.assertIn("MIDBOSS2_PATTERN_STACK_COUNT | (MIDBOSS2_PATTERN_STACK_DELTA << 8)", leaf)
        self.assertIn("bullet_template.spawn_type = MIDBOSS2_CLOUD_NO_DECEL_SPAWN;", leaf)
        self.assertIn("bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;", leaf)
        self.assertEqual((number("MIDBOSS2_NO_DECEL_SPAWN"), number("MIDBOSS2_CLOUD_NO_DECEL_SPAWN")), (0x10, 0x12))
        self.assertEqual((number("MIDBOSS2_RED_BALL_PATNUM"), number("MIDBOSS2_PATTERN_STACK_COUNT"), number("MIDBOSS2_PATTERN_STACK_DELTA"), number("MIDBOSS2_PATTERN_SPEED_SP")), (48, 3, 8, 24))
        self.assertEqual([frame for frame in range(1, 65) if frame % 16 == 0], [16, 32, 48, 64])
        self.assertEqual(24 / 16, 1.5)
        self.assertEqual(leaf.count("bullet_template_tune();"), 2)
        self.assertEqual(leaf.count("bullets_add_regular();"), 2)

    def test_random_cloud_spread_steps_at_800_and_600_hp_are_ordered(self):
        leaf = function(PATTERNS, "midboss2_pattern", "midboss2_pattern_final")
        self.assertEqual((number("MIDBOSS2_CLOUD_SPREAD_BASE"), number("MIDBOSS2_CLOUD_SPREAD_MID"), number("MIDBOSS2_CLOUD_SPREAD_LOW")), (3, 4, 6))
        self.assertEqual((number("MIDBOSS2_CLOUD_HP_MID"), number("MIDBOSS2_CLOUD_HP_LOW")), (800, 600))
        self.assertLess(leaf.index("if(midboss.hp <= MIDBOSS2_CLOUD_HP_LOW)"), leaf.index("else if(midboss.hp <= MIDBOSS2_CLOUD_HP_MID)"))
        spread = lambda hp: 6 if hp <= 600 else 4 if hp <= 800 else 3
        self.assertEqual([spread(hp) for hp in (1000, 801, 800, 601, 600, 0)], [3, 3, 4, 4, 6, 6])

    def test_final_pattern_uses_four_frame_blue_stack_with_delta_fifteen(self):
        leaf = function(PATTERNS, "midboss2_pattern_final")
        self.assertIn("if(stage_frame_mod4 == 0)", leaf)
        self.assertIn("bullet_template.spawn_type = MIDBOSS2_NO_DECEL_SPAWN;", leaf)
        self.assertIn("bullet_template.patnum = MIDBOSS2_BLUE_BALL_PATNUM;", leaf)
        self.assertIn("MIDBOSS2_FINAL_STACK_COUNT | (MIDBOSS2_FINAL_STACK_DELTA << 8)", leaf)
        self.assertEqual((number("MIDBOSS2_BLUE_BALL_PATNUM"), number("MIDBOSS2_FINAL_STACK_COUNT"), number("MIDBOSS2_FINAL_STACK_DELTA")), (44, 3, 15))
        self.assertEqual([frame for frame in range(1, 17) if frame % 4 == 0], [4, 8, 12, 16])

    def test_entrance_resets_the_signed_orbit_state_and_center_after_256_frames(self):
        update = UPDATE[UPDATE.index("case MIDBOSS2_PHASE_ENTRANCE:"):UPDATE.index("case MIDBOSS2_PHASE_ORBIT_ATTACK:")]
        self.assertEqual(number("MIDBOSS2_ENTRANCE_END_FRAME"), 256)
        self.assertIn("midboss.pos.update_seg3();", update)
        self.assertIn("midboss_hittest_shots_damage(to_sp(MIDBOSS2_HIT_RADIUS_PX), to_sp(MIDBOSS2_HIT_RADIUS_PX), MIDBOSS2_INVINCIBLE_HIT_SOUND);", update)
        self.assertIn("midboss2_scratch.orbit_contracting = MIDBOSS2_ORBIT_EXPANDING;", update)
        self.assertIn("midboss2_scratch.orbit_center_drift = MIDBOSS2_ORBIT_DRIFT_INITIAL;", update)
        self.assertIn("midboss2_orbit_center.x.v = to_sp(192);", update)
        self.assertIn("midboss.pos.velocity.x.v = 0;", update)
        self.assertEqual((number("MIDBOSS2_HIT_RADIUS_PX"), number("MIDBOSS2_INVINCIBLE_HIT_SOUND")), (24, 10))

    def test_orbit_hp_exit_and_timeout_share_transition_but_only_hp_exit_rewards(self):
        orbit = UPDATE[UPDATE.index("case MIDBOSS2_PHASE_ORBIT_ATTACK:"):UPDATE.index("case MIDBOSS2_PHASE_FINAL_ATTACK:")]
        self.assertIn("midboss2_pattern();", orbit)
        self.assertIn("midboss2_move();", orbit)
        self.assertIn("stage2_midboss_hittest_shots(to_sp(24), to_sp(24));", orbit)
        self.assertEqual((number("MIDBOSS2_ORBIT_TIMEOUT_FRAMES"), number("MIDBOSS2_ORBIT_HP_THRESHOLD")), (1000, 400))
        self.assertLess(orbit.index("if(midboss.phase_frame < MIDBOSS2_ORBIT_TIMEOUT_FRAMES)"), orbit.index("if(midboss.hp > MIDBOSS2_ORBIT_HP_THRESHOLD)"))
        self.assertIn("midboss_score_bonus(MIDBOSS2_ORBIT_SCORE_BONUS);", orbit)
        self.assertIn("if(bullet_clear_time < MIDBOSS2_BULLET_CLEAR_MIN)", orbit)
        self.assertIn("bullet_clear_time = MIDBOSS2_BULLET_CLEAR_MIN;", orbit)
        self.assertEqual((number("MIDBOSS2_ORBIT_SCORE_BONUS"), number("MIDBOSS2_BULLET_CLEAR_MIN")), (5, 20))
        hp_reward = lambda frame, hp: frame < 1000 and hp <= 400
        self.assertEqual([hp_reward(frame, hp) for frame, hp in ((999, 400), (999, 401), (1000, 0), (1000, 401))], [True, False, False, False])
        self.assertIn("midboss.sprite = MIDBOSS2_SPRITE_DAMAGED;", orbit)
        self.assertIn("sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(MIDBOSS2_ORBIT_SPARK_RADIUS_PX), MIDBOSS2_ORBIT_SPARK_COUNT);", orbit)
        self.assertIn("vector2_between_plus(midboss.pos.cur.x.v, midboss.pos.cur.y.v,", orbit)

    def test_final_attack_rewards_only_hp_defeat_before_800_frame_timeout(self):
        final = UPDATE[UPDATE.index("case MIDBOSS2_PHASE_FINAL_ATTACK:"):UPDATE.index("default:")]
        self.assertIn("midboss2_pattern_final();", final)
        self.assertIn("midboss.pos.update_seg3();", final)
        self.assertIn("stage2_midboss_hittest_shots(to_sp(24), to_sp(24));", final)
        self.assertEqual((number("MIDBOSS2_FINAL_TIMEOUT_FRAMES"), number("MIDBOSS2_FINAL_SCORE_BONUS")), (800, 15))
        self.assertLess(final.index("if(midboss.phase_frame < MIDBOSS2_FINAL_TIMEOUT_FRAMES)"), final.index("if(midboss.hp > 0)"))
        self.assertIn("bullet_zap.active = true;", final)
        self.assertIn("items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_BOMB);", final)
        self.assertIn("midboss.phase = MIDBOSS2_PHASE_EXPLODE_BIG;", final)
        self.assertIn("sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(MIDBOSS2_FINAL_SPARK_RADIUS_PX), MIDBOSS2_FINAL_SPARK_COUNT);", final)
        self.assertEqual((number("MIDBOSS2_FINAL_SPARK_RADIUS_PX"), number("MIDBOSS2_FINAL_SPARK_COUNT"), number("MIDBOSS2_FINAL_TRANSITION_SOUND")), (8, 48, 12))
        hp_reward = lambda frame, hp: frame < 800 and hp <= 0
        self.assertEqual([hp_reward(frame, hp) for frame, hp in ((799, 0), (799, 1), (800, 0), (800, 1))], [True, False, False, False])

    def test_defeat_default_returns_before_homing_target_publication(self):
        default_start = UPDATE.index("default:")
        default = UPDATE[default_start:UPDATE.index("return;", default_start) + len("return;")]
        self.assertIn("midboss_defeat_update();", default)
        self.assertIn("hud_hp_update_and_render(midboss.hp, MIDBOSS2_HP_TOTAL);", default)
        self.assertIn("return;", default)
        self.assertNotIn("homing_target.x", default)
        self.assertIn("homing_target.x = midboss.pos.cur.x;", UPDATE)


if __name__ == "__main__":
    unittest.main()
