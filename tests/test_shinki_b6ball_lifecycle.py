"""Executable model of the 220-byte B6-ball cloud/active/decay/free leaf."""
from dataclasses import dataclass
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "src/main/boss/shinki/balls_update_body.inl").read_text()
GENERATOR = (ROOT / "src/main/boss/shinki/shinki.cpp").read_text()
HEADER = (ROOT / "src/main/boss/shinki/shinki.hpp").read_text()
RULES = (ROOT / "src/main/boss/shinki/ball_lifecycle.hpp").read_text()


def value(name):
    match = re.search(rf"\b{name}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)", HEADER)
    if match:
        return int(match.group(1), 0)
    match = re.search(rf"#define\s+{name}\s+(0[xX][0-9A-Fa-f]+|[0-9]+(?:\.\d+)?f?)", HEADER + "\n" + RULES)
    if match:
        return float(match.group(1).rstrip("f")) if "." in match.group(1) else int(match.group(1), 0)
    raise AssertionError(f"missing B6-ball constant {name}")


FREE = value("B6BF_FREE")
CLOUD = value("B6BF_CLOUD")
ALIVE = value("B6BF_ALIVE")
DECAY = value("B6BF_DECAY")
BALL_COUNT = value("B6BALL_COUNT")
BALL_W = value("B6BALL_W")
BALL_H = value("B6BALL_H")
DECAY_FIRST = value("PAT_DECAY_B6BALL")
DECAY_LAST = value("PAT_DECAY_B6BALL_last")
BIRTH_RADIUS = int(value("SHINKI_B6_BIRTH_CLOUD_RADIUS_PX"))
CLOUD_SHRINK = int(value("SHINKI_B6_CLOUD_SHRINK_PX"))
HALF_DIVISOR = value("SHINKI_B6_HITBOX_HALF_DIVISOR")
VELOCITY_DIVISOR = value("SHINKI_B6_DECAY_VELOCITY_DIVISOR")
DECAY_INTERVAL = value("SHINKI_B6_DECAY_ANIMATION_INTERVAL")


def trunc_div(value, divisor):
    """C/C++ signed integer division truncates toward zero."""
    return int(value / divisor)


@dataclass
class Ball:
    flag: int = FREE
    radius: int = 0
    age: int = 0
    x: int = 0
    y: int = 0
    vx: int = 0
    vy: int = 0
    sprite: int = 200
    decay_frame: int = 0


def update(ball, *, clear=False, zap=False, in_bounds=True, collision=False):
    """Model the actual source branch order; returns whether player was hit."""
    player_hit = False
    if ball.flag != FREE:
        if ball.flag == CLOUD:
            ball.radius -= CLOUD_SHRINK
            if ball.radius < BALL_W // HALF_DIVISOR:
                ball.flag += 1
            else:
                return player_hit
        if clear or zap:
            ball.flag = DECAY
        ball.age = (ball.age + 1) & 0xFFFF
        ball.x += ball.vx
        ball.y += ball.vy
        if not in_bounds:
            ball.flag = FREE
        elif ball.flag != DECAY:
            if collision:
                player_hit = True
                ball.flag = DECAY
                return player_hit
        elif ball.sprite < DECAY_FIRST:
            ball.sprite = DECAY_FIRST
            ball.vx = trunc_div(ball.vx, VELOCITY_DIVISOR)
            ball.vy = trunc_div(ball.vy, VELOCITY_DIVISOR)
            ball.decay_frame = 0
        else:
            ball.decay_frame += 1
            if (ball.decay_frame % DECAY_INTERVAL) == 0:
                ball.sprite += 1
                if ball.sprite >= (DECAY_LAST + 1):
                    ball.flag = FREE
    return player_hit


class ShinkiB6BallLifecycleTests(unittest.TestCase):
    def test_original_pool_has_sixty_three_slots_after_the_template(self):
        self.assertEqual((BALL_COUNT, BALL_W, BALL_H), (63, 32, 32))
        self.assertIn("#define b6balls (reinterpret_cast<b6ball_t *>(&custom_entities[1]))", HEADER)
        self.assertIn("shinki_slots_fit_exactly", HEADER)
        self.assertIn("(1 + B6BALL_COUNT) * sizeof(b6ball_t)", HEADER)
        self.assertIn("for((p = b6balls, i = 1); i < (1 + B6BALL_COUNT); (i++, p++))", GENERATOR)

    def test_birth_cloud_shrinks_two_pixels_and_uses_strict_sixteen_pixel_exit(self):
        self.assertEqual((BIRTH_RADIUS, CLOUD_SHRINK, BALL_W // HALF_DIVISOR), (48, 2, 16))
        ball = Ball(flag=CLOUD, radius=BIRTH_RADIUS, age=77)
        for frame in range(1, 17):
            update(ball)
            self.assertEqual(ball.flag, CLOUD, f"cloud changed early at frame {frame}")
            self.assertEqual(ball.radius, 48 - frame * 2)
            self.assertEqual(ball.age, 77)
        self.assertEqual(ball.radius, 16)
        update(ball)
        self.assertEqual((ball.flag, ball.radius), (ALIVE, 14))
        self.assertEqual(ball.age, 78)

    def test_cloud_is_not_cleared_or_moved_until_its_radius_crosses_the_hitbox(self):
        ball = Ball(flag=CLOUD, radius=18, age=12, x=20, y=30, vx=3, vy=-2)
        update(ball, clear=True, zap=True, collision=True)
        self.assertEqual((ball.flag, ball.radius, ball.age, ball.x, ball.y), (CLOUD, 16, 12, 20, 30))
        update(ball, clear=True)
        self.assertEqual((ball.flag, ball.radius, ball.age, ball.x, ball.y), (DECAY, 14, 13, 23, 28))

    def test_active_collision_sets_decay_and_defers_decay_initialization_one_tick(self):
        ball = Ball(flag=ALIVE, radius=14, age=4, vx=5, vy=-5, sprite=200)
        self.assertTrue(update(ball, collision=True))
        self.assertEqual((ball.flag, ball.age, ball.sprite, ball.vx, ball.vy, ball.decay_frame), (DECAY, 5, 200, 5, -5, 0))
        self.assertFalse(update(ball))
        self.assertEqual((ball.flag, ball.age, ball.sprite, ball.vx, ball.vy, ball.decay_frame), (DECAY, 6, 204, 2, -2, 0))

    def test_bullet_clear_and_bullet_zap_enter_decay_before_position_and_hit_test(self):
        for kwargs in ({"clear": True}, {"zap": True}):
            ball = Ball(flag=ALIVE, age=9, vx=2, vy=1, sprite=200)
            self.assertFalse(update(ball, collision=True, **kwargs))
            self.assertEqual((ball.flag, ball.age, ball.x, ball.y, ball.sprite), (DECAY, 10, 2, 1, 204))

    def test_bounds_check_precedes_collision_and_decay_setup(self):
        ball = Ball(flag=ALIVE, age=3, vx=100, vy=0, sprite=200)
        self.assertFalse(update(ball, in_bounds=False, collision=True))
        self.assertEqual((ball.flag, ball.age, ball.sprite, ball.decay_frame), (FREE, 4, 200, 0))
        self.assertIn("if(!playfield_encloses(_AX, _DX, B6BALL_W, B6BALL_H))", SOURCE)
        self.assertLess(SOURCE.index("if(!playfield_encloses("), SOURCE.index("} else if(p->flag != B6BF_DECAY)"))

    def test_decay_halves_signed_velocity_with_truncation_toward_zero(self):
        self.assertEqual(VELOCITY_DIVISOR, 2)
        ball = Ball(flag=DECAY, age=1, vx=-5, vy=5, sprite=200)
        update(ball)
        self.assertEqual((ball.sprite, ball.vx, ball.vy, ball.decay_frame), (204, -2, 2, 0))
        ball = Ball(flag=DECAY, age=1, vx=-3, vy=3, sprite=200)
        update(ball)
        self.assertEqual((ball.vx, ball.vy), (-1, 1))

    def test_decay_animation_advances_only_every_four_frames_through_204_to_207(self):
        self.assertEqual((DECAY_FIRST, DECAY_LAST, DECAY_INTERVAL), (204, 207, 4))
        ball = Ball(flag=DECAY, sprite=DECAY_FIRST)
        expected = [204, 204, 204, 205, 205, 205, 205, 206,
                    206, 206, 206, 207, 207, 207, 207, 208]
        observed = []
        for frame in range(1, 17):
            update(ball)
            observed.append(ball.sprite)
            if frame < 16:
                self.assertEqual(ball.flag, DECAY)
        self.assertEqual(observed, expected)
        self.assertEqual(ball.flag, FREE)
        self.assertEqual(ball.sprite, 208)

    def test_age_is_incremented_for_active_decay_but_never_reset_on_spawn(self):
        self.assertIn("p->age++;", SOURCE)
        self.assertNotRegex(GENERATOR[GENERATOR.index("void near b6balls_add(void)"):GENERATOR.index("#include \"src/main/boss/shinki/balls_update_body.inl\"")], r"\bage\s*=")
        self.assertNotIn("p->age =", SOURCE)
        cloud = Ball(flag=CLOUD, radius=18, age=0xFFFF)
        update(cloud)
        self.assertEqual(cloud.age, 0xFFFF)
        update(cloud)
        self.assertEqual(cloud.age, 0)

    def test_update_order_keeps_clear_before_age_motion_bounds_and_collision(self):
        positions = [
            SOURCE.index("if(p->flag == B6BF_CLOUD)"),
            SOURCE.index("if(bullet_clear_time || bullet_zap.active)"),
            SOURCE.index("p->age++;"),
            SOURCE.index("p->pos.update_seg3();"),
            SOURCE.index("if(!playfield_encloses("),
            SOURCE.index("} else if(p->flag != B6BF_DECAY)"),
            SOURCE.index("if(overlap_wh_inplace_fast("),
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(SOURCE.count("optimization_barrier();"), 2)

    def test_spawn_uses_first_free_slot_and_preserves_unused_age_storage(self):
        start = GENERATOR.index("void near b6balls_add(void)")
        end = GENERATOR.index("#include \"src/main/boss/shinki/balls_update_body.inl\"", start)
        body = GENERATOR[start:end]
        self.assertIn("subpixel_t speed = playperf_speedtune(b6ball_template.speed);", body)
        self.assertIn("if(p->flag != B6BF_FREE)", body)
        self.assertIn("p->flag = B6BF_CLOUD;", body)
        self.assertIn("p->pos.cur = b6ball_template.origin;", body)
        self.assertIn("vector2_near(p->pos.velocity, b6ball_template.angle, speed);", body)
        self.assertIn("p->patnum_tiny = b6ball_template.patnum_tiny;", body)
        self.assertIn("p->cloud_radius.v = to_sp(SHINKI_B6_BIRTH_CLOUD_RADIUS_PX);", body)
        self.assertIn("return;", body)
        self.assertNotIn("p->age", body)
        self.assertIn("Original comment: unused and broken; never reset.", HEADER)


if __name__ == "__main__":
    unittest.main()
