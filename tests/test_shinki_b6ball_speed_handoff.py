"""Ranked B6-ball template speed provenance across Shinki's late phases."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "src/main/boss/shinki/shinki.cpp").read_text()
CONTEXT = (ROOT / "src/main/boss/shinki/update_context.cpp").read_text()
DEVIL = (ROOT / "src/main/boss/shinki/devil.inl").read_text()
BALLISTICS = (ROOT / "src/main/boss/shinki/devil_ballistics.hpp").read_text()
WING_RULES = (ROOT / "src/main/boss/shinki/wing_attack_rules.hpp").read_text()
TIMING = (ROOT / "src/main/boss/shinki/final_spiral_timing.hpp").read_text()
BALL_ADD = SOURCE[SOURCE.index("void near b6balls_add(void)"):SOURCE.index("#include \"src/main/boss/shinki/balls_update_body.inl\"")]
HP = (ROOT / "src/main/boss/shinki/hp.inl").read_text()
GENERIC = (ROOT / "src/main/boss/generic.cpp").read_text()


def rank_values(prefix):
    names = ("EASY", "NORMAL", "HARD", "LUNATIC")
    return {
        rank: int(re.search(rf"#define {prefix}_{rank}\s+(\d+)", BALLISTICS if prefix.startswith("DEVIL") else WING_RULES).group(1))
        for rank in names
    }


def first_multiple_after(start, interval):
    return ((start + interval - 1) // interval) * interval


def without_comments(source):
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    return re.sub(r"//[^\n]*", "", source)


class ShinkiB6BallSpeedHandoffTests(unittest.TestCase):
    def test_ranked_phase_nine_writer_precedes_the_devil_writer(self):
        intervals = rank_values("SHW_AIMED_INTERVAL")
        expected = {"EASY": 192, "NORMAL": 160, "HARD": 140, "LUNATIC": 144}
        self.assertEqual(
            {rank: first_multiple_after(130, interval) for rank, interval in intervals.items()},
            expected,
        )
        self.assertIn("#define SHW_AIMED_FIRST_ATTACK_FRAME 128", WING_RULES)
        self.assertIn("#define SHW_AIMED_INIT_FRAME 129", WING_RULES)
        aimed_start = SOURCE.index("void near pattern_aimed_b6balls_and_symmetric_spreads(void)")
        aimed_end = SOURCE.index("#include \"src/main/boss/shinki/devil.inl\"", aimed_start)
        aimed = SOURCE[aimed_start:aimed_end]
        self.assertIn("b6ball_template.speed.v = sara_to_sp8(SHW_AIMED_BALL_SPEED_PX);", aimed)
        self.assertIn("#define SHW_AIMED_BALL_SPEED_PX 4.0f", WING_RULES)

    def test_purple_transition_can_remain_the_final_speed_source(self):
        # Phase 8's purple transition writes sixteen random speeds at frame
        # 192. The last value remains in the shared template after the loop.
        for text in (
            "#define SHW_PURPLE_SPAWN_FRAME 192",
            "#define SHW_PURPLE_SPAWN_COUNT 16",
            "#define SHW_PURPLE_SPAWN_SPEED_MIN 2.0f",
            "#define SHW_PURPLE_SPAWN_SPEED_MAX 6.0f",
        ):
            self.assertIn(text, WING_RULES)
        purple_start = SOURCE.index("bool near pattern_wings_to_purple(void)")
        purple_end = SOURCE.index("void near pattern_aimed_b6balls_and_symmetric_spreads(void)", purple_start)
        purple = SOURCE[purple_start:purple_end]
        self.assertIn("for(int i = 0; i < SHW_PURPLE_SPAWN_COUNT; i++)", purple)
        self.assertIn("b6ball_template.speed.v = sara_rand_speed(SHW_PURPLE_SPAWN_SPEED_MIN, SHW_PURPLE_SPAWN_SPEED_MAX);", purple)
        self.assertLess(purple.index("b6ball_template.speed.v = sara_rand_speed("), purple.index("b6balls_add();"))
        self.assertIn("return (boss.phase_frame == SHW_PURPLE_FINISH_FRAME);", purple)

        # The purple phase observes the hit test but ignores its result; it
        # always reaches the frame-200 handoff after the frame-192 seed.
        purple_phase_start = CONTEXT.index("case SHINKI_PHASE_PURPLE_TRANSITION:")
        purple_phase_end = CONTEXT.index("case SHINKI_PHASE_SYMMETRIC_SPREADS:", purple_phase_start)
        purple_phase = CONTEXT[purple_phase_start:purple_phase_end]
        self.assertIn("boss_hittest_shots();", purple_phase)
        self.assertIn("if(pattern_wings_to_purple())", purple_phase)
        self.assertNotIn("if(!boss_hittest_shots())", purple_phase)

        # Phase 9 calls the aimed callback before its HP test. Its first speed
        # write is rank-specific and may be skipped by an earlier HP exit.
        phase_start = CONTEXT.index("case SHINKI_PHASE_SYMMETRIC_SPREADS:")
        phase_end = CONTEXT.index("case SHINKI_PHASE_DEFEAT_TRANSITION:", phase_start)
        phase = CONTEXT[phase_start:phase_end]
        self.assertLess(phase.index("SHINKI_WING_FLIGHT_AND_ATTACK();"), phase.index("phase_done = boss_hittest_shots();"))
        self.assertIn("wing_pattern();", CONTEXT[:CONTEXT.index("case SHINKI_PHASE_SYMMETRIC_SPREADS:")])
        self.assertNotIn("SHW_AIMED_FIRST_ATTACK_FRAME", phase)
        intervals = rank_values("SHW_AIMED_INTERVAL")
        phase9_first = {
            rank: first_multiple_after(130, interval)
            for rank, interval in intervals.items()
        }
        self.assertEqual(phase9_first, {"EASY": 192, "NORMAL": 160, "HARD": 140, "LUNATIC": 144})

        # If HP exits before that first spawn, the purple random speed remains;
        # the same-frame exit occurs after the callback and therefore sees 4.0.
        def phase9_carry(exit_frame, first_spawn):
            return "purple-random-2.0-to-under-6.0" if exit_frame < first_spawn else 4.0

        for rank, first in phase9_first.items():
            self.assertEqual(phase9_carry(first - 1, first), "purple-random-2.0-to-under-6.0", rank)
            self.assertEqual(phase9_carry(first, first), 4.0, rank)

    def test_devil_first_aimed_ball_is_rank_gated_after_its_angle_prelude(self):
        intervals = rank_values("DEVIL_BALL_START")
        expected = {"EASY": 256, "NORMAL": 280, "HARD": 256, "LUNATIC": 280}
        self.assertEqual(
            {rank: first_multiple_after(256, interval) for rank, interval in intervals.items()},
            expected,
        )
        self.assertIn("DEVIL_PATTERN_START_FRAME = 192", DEVIL)
        self.assertIn("DEVIL_PRELUDE_OUTER_STEP = 0x04", DEVIL)
        self.assertIn("DEVIL_SPREAD_OUTER_HIGH = 0x40", DEVIL)
        self.assertIn("#define SHINKI_DEVIL_AIMED_BALL_SPEED_PX 3.75f", BALLISTICS)

        start = DEVIL.index("// Spread bullets")
        end = DEVIL.index("// Lasers", start)
        spread = DEVIL[start:end]
        self.assertIn("if((bullet_angle_outer == DEVIL_SPREAD_OUTER_HIGH) && (bullet_intro_done == 0))", spread)
        self.assertIn("if(bullet_intro_done && ((boss.phase_frame % b6ball_interval) == 0))", spread)
        self.assertIn("b6ball_template.speed.v = sara_to_sp8(SHINKI_DEVIL_AIMED_BALL_SPEED_PX);", spread)

    def test_phase_ten_can_take_the_hp_exit_before_the_ranked_speed_write(self):
        # The late-wing controller runs the Devil callback, then tests HP; no
        # minimum frame is required before boss_phase_next can enter phase 11.
        phase_start = SOURCE.index("case SHINKI_PHASE_SYMMETRIC_SPREADS:")
        phase_end = SOURCE.index("case SHINKI_PHASE_DEFEAT_TRANSITION:", phase_start)
        phase = SOURCE[phase_start:phase_end]
        self.assertLess(phase.index("wing_pattern();"), phase.index("phase_done = boss_hittest_shots();"))
        self.assertIn("boss_phase_next(ET_HORIZONTAL, HP_PHASE_12_END);", phase)
        self.assertIn("boss_phase_next(ET_SW_NE, HP_PHASE_10_END);", phase)
        self.assertIn("HP_PHASE_10_END = 2800", HP)
        self.assertIn("HP_PHASE_10_DEVIL_LASER = 5600", HP)
        # The strict 3000-frame timeout is the only frame-count gate; the HP
        # path is reachable before the rank-specific 256/280 first spawn.
        self.assertIn("if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES)", phase)
        self.assertNotRegex(phase, r"if\s*\(\s*boss\.phase_frame\s*<\s*(?:256|280)\s*\)")
        self.assertNotIn("b6ball_template.speed", phase)

    def test_final_spiral_consumes_the_carried_speed_without_reinitializing_it(self):
        for source in (SOURCE, CONTEXT):
            start = source.index("void near pattern_circles_and_alternating_spirals(void)")
            end = source.index("void near shinki_move_float(void)", start)
            final = source[start:end]
            executable = without_comments(final)
            self.assertNotIn("b6ball_template.speed", executable)
            self.assertIn("SHINKI_SPIRAL_ARM_FRAME", final)
            if "SHINKI_SPIRAL_FIRE_OFFSET_B6BALL();" in final:
                self.assertEqual(final.count("SHINKI_SPIRAL_FIRE_OFFSET_B6BALL();"), 2)
                macro_start = source.index("#define SHINKI_SPIRAL_FIRE_OFFSET_B6BALL()")
                macro_end = source.index("// The red and pellet rings", macro_start)
                self.assertIn("b6balls_add();", source[macro_start:macro_end])
            else:
                self.assertEqual(executable.count("b6balls_add();"), 2)
        self.assertIn("subpixel_t speed = playperf_speedtune(b6ball_template.speed);", BALL_ADD)
        self.assertIn("vector2_near(p->pos.velocity, b6ball_template.angle, speed);", BALL_ADD)
        self.assertNotRegex(BALL_ADD, r"b6ball_template\.speed\s*=")

        # The final value is the last writer reached across the three phases:
        # purple's random [2,6) speed, phase nine's 4.0, then Devil's 3.75.
        def carried_speed(phase9_exit, phase9_first, devil_exit, devil_first):
            speed = "purple-random-2.0-to-under-6.0"
            if phase9_exit >= phase9_first:
                speed = 4.0
            if devil_exit >= devil_first:
                speed = 3.75
            return speed

        phase9_first = {"EASY": 192, "NORMAL": 160, "HARD": 140, "LUNATIC": 144}
        devil_first = {"EASY": 256, "NORMAL": 280, "HARD": 256, "LUNATIC": 280}
        for rank in ("EASY", "NORMAL", "HARD", "LUNATIC"):
            self.assertEqual(
                carried_speed(phase9_first[rank] - 1, phase9_first[rank], devil_first[rank] - 1, devil_first[rank]),
                "purple-random-2.0-to-under-6.0",
            )
            self.assertEqual(
                carried_speed(phase9_first[rank], phase9_first[rank], devil_first[rank] - 1, devil_first[rank]),
                4.0,
            )
            self.assertEqual(
                carried_speed(phase9_first[rank], phase9_first[rank], devil_first[rank], devil_first[rank]),
                3.75,
            )


if __name__ == "__main__":
    unittest.main()
