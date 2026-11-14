"""Sara's full 1,824-byte Boss update: phase, pattern and laser clocks."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SARA = (ROOT / "src/main/boss/sara/sara.cpp").read_text()
SARA_HPP = (ROOT / "src/main/boss/sara/sara.hpp").read_text()
WAVE_SETTINGS = (ROOT / "src/main/boss/sara/combat_wave_settings.hpp").read_text()
PROJECTILE_RULES = (ROOT / "src/main/boss/sara/projectile_rules.hpp").read_text()
PATTERN_TABLES = (ROOT / "src/main/boss/sara/pattern_tables.cpp").read_text()
BACKGROUND = (ROOT / "src/main/boss/background.hpp").read_text()
GENERIC = (ROOT / "src/main/boss/generic.cpp").read_text()
GAMEPLAY_LOOP = (ROOT / "src/main/runtime/gameplay_loop.cpp").read_text()


def number(name, source):
    match = re.search(rf"\b{name}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)", source)
    if not match:
        raise AssertionError(f"missing numeric constant {name}")
    return int(match.group(1), 0)


def macro_int(name, source):
    match = re.search(rf"^#define {name}\s+(0[xX][0-9A-Fa-f]+|[0-9]+)$", source, re.M)
    if not match:
        raise AssertionError(f"missing macro {name}")
    return int(match.group(1), 0)


def sara_phase(name):
    next_name = {
        "PHASE_HP_FILL": "PHASE_BOSS_ENTRANCE_BB",
        "PHASE_BOSS_ENTRANCE_BB": "SARA_PHASE_BLUE_RED_WAVES",
        "SARA_PHASE_BLUE_RED_WAVES": "SARA_PHASE_SPINNING_RINGS",
        "SARA_PHASE_SPINNING_RINGS": "SARA_PHASE_LASER_CORRIDOR",
        "SARA_PHASE_LASER_CORRIDOR": "default",
    }[name]
    start = SARA.index(f"case {name}:")
    end = SARA.index(f"case {next_name}:", start + 1) if next_name != "default" else SARA.index("default:", start + 1)
    return SARA[start:end]


def corridor_turns():
    left = (-number("SARA_LASER_CORRIDOR_CENTER_ANGLE", PROJECTILE_RULES)
            - number("SARA_LASER_OFFSET_ANGLE", PROJECTILE_RULES)) & 0xFF
    right = (-number("SARA_LASER_CORRIDOR_CENTER_ANGLE", PROJECTILE_RULES)
             + number("SARA_LASER_OFFSET_ANGLE", PROJECTILE_RULES)) & 0xFF
    interval = number("SARA_LASER_INITIAL_TURN_INTERVAL", PROJECTILE_RULES)
    slowdown = [
        number("SARA_LASER_SLOWDOWN_ANGLE_A", PROJECTILE_RULES),
        number("SARA_LASER_SLOWDOWN_ANGLE_B", PROJECTILE_RULES),
        number("SARA_LASER_SLOWDOWN_ANGLE_C", PROJECTILE_RULES),
        number("SARA_LASER_SLOWDOWN_ANGLE_D", PROJECTILE_RULES),
    ]
    frames = []
    thresholds = []
    for frame in range(number("SARA_LASER_CREATE_FRAME", PROJECTILE_RULES) + 1,
                        number("SARA_LASER_CORRIDOR_TIMEOUT", SARA) + 1):
        if frame % interval and interval != 1:
            continue
        terminal = (number("SARA_LASER_CORRIDOR_CENTER_ANGLE", PROJECTILE_RULES) +
                    number("SARA_LASER_CORRIDOR_ANGLE_WIDTH", PROJECTILE_RULES) // 2)
        if left <= terminal:
            continue
        right = (right + 1) & 0xFF
        left = (left - 1) & 0xFF
        frames.append(frame)
        if left in slowdown:
            thresholds.append((frame, left, interval + 1))
            interval += 1
    return frames, thresholds, right, left, interval


class SaraBossLifecycleTests(unittest.TestCase):
    def test_hp_fill_gather_window_and_transition_are_inclusive(self):
        hp_fill = number("HUD_HP_FILL_FRAMES", SARA_HPP)
        extra = macro_int("SAR_HP_GATHER_EXTRA_DELAY", WAVE_SETTINGS)
        span = macro_int("SAR_HP_GATHER_SPAN", WAVE_SETTINGS)
        start = hp_fill + extra
        end = start + span
        self.assertEqual((hp_fill, start, end), (128, 224, 256))
        gather_frames = [frame for frame in range(start, end + 1)
                         if frame & macro_int("SAR_HP_GATHER_TICK_MASK", WAVE_SETTINGS) == 0]
        self.assertEqual(gather_frames, [224, 232, 240, 248, 256])

        fill = sara_phase("PHASE_HP_FILL")
        self.assertIn("if(boss.phase_frame == SAR_HP_FILL_FIRST_FRAME)", fill)
        self.assertLess(fill.index("gather_template.col = COL_GATHER_1;"),
                        fill.index("gather_add_only();"))
        self.assertLess(fill.index("gather_add_only();"),
                        fill.index("gather_template.col = COL_GATHER_2;"))
        self.assertIn("if(boss.phase_frame >= KEYFRAME_GATHER_SPAWN_END)", fill)
        self.assertIn("boss.phase_frame = 0;", fill)
        self.assertIn("bg_render_bombing_func = sara_bg_render;", fill)

    def test_entrance_initializes_the_two_mobile_wave_protocol(self):
        frames_per_cel = number("ENTRANCE_BB_TRANSITION_FRAMES_PER_CEL", SARA_HPP)
        self.assertIn("#define TILES_BB_CELS (2048 / 128)", BACKGROUND)
        cels = 2048 // 128
        self.assertEqual(frames_per_cel * cels, 32)
        entrance = sara_phase("PHASE_BOSS_ENTRANCE_BB")
        self.assertIn("if(boss.phase_frame >= (", entrance)
        self.assertIn("boss.phase_state.patterns_seen = 0;", entrance)
        self.assertIn("state->phase_2.previous_pattern_mode = SARA_MODE_NO_PREVIOUS_PATTERN;", entrance)
        self.assertIn("state->phase_2.fly_delay = SARA_WAVE_2_FLY_DELAY_INITIAL;", entrance)
        self.assertIn("boss.mode = SARA_MODE_REPOSITION;", entrance)

    def test_mobile_wave_limits_count_the_terminal_reposition_not_an_extra_pattern(self):
        selector_start = SARA.index("#define phase_2_3_wait_fly_and_select_pattern(")
        selector_end = SARA.index("// A successful hit during either mobile wave", selector_start)
        selector = SARA[selector_start:selector_end]
        self.assertLess(selector.index("boss.phase_state.patterns_seen++;"),
                        selector.index("if(boss.phase_state.patterns_seen >= patterns_max)"))
        self.assertLess(selector.index("if(boss.phase_state.patterns_seen >= patterns_max)"),
                        selector.index("boss.mode = randring2_next8_mod_ge_lt"))
        self.assertIn("do {", selector)
        self.assertIn("} while(boss.mode == previous_pattern_mode);", selector)

        phase2_limit = number("SARA_WAVE_2_PATTERN_LIMIT", SARA)
        phase3_limit = number("SARA_WAVE_3_PATTERN_LIMIT", SARA)
        self.assertEqual((phase2_limit, phase3_limit), (32, 24))
        executed = lambda limit: sum(1 for seen in range(1, limit) if seen < limit)
        self.assertEqual((executed(phase2_limit), executed(phase3_limit)), (31, 23))
        callbacks = re.findall(r"^\s+pattern_[a-z0-9_]+,?$", PATTERN_TABLES, re.M)
        self.assertEqual(len(callbacks), 8)

        phase2 = sara_phase("SARA_PHASE_BLUE_RED_WAVES")
        phase3 = sara_phase("SARA_PHASE_SPINNING_RINGS")
        for phase, label in ((phase2, "phase_2_timed_out:"),
                             (phase3, "phase_3_timed_out:")):
            self.assertLess(phase.index("SARA_WAVE_HIT_SCORE_OR_BREAK();"), phase.index(label))
            self.assertIn("boss_phase_next(", phase[phase.index(label):])
        self.assertIn("goto timeout_label;", selector)

    def test_phase_two_fly_delay_is_a_guarded_staircase_that_ends_at_four(self):
        delay = number("SARA_WAVE_2_FLY_DELAY_INITIAL", SARA)
        guard = number("SARA_WAVE_2_FLY_DELAY_GUARD", SARA)
        step = number("SARA_WAVE_2_FLY_DELAY_STEP", SARA)
        values = [delay]
        while delay > guard:
            delay -= step
            values.append(delay)
        self.assertEqual((guard, step, values), (12, 12, [64, 52, 40, 28, 16, 4]))
        phase2 = sara_phase("SARA_PHASE_BLUE_RED_WAVES")
        self.assertIn("(boss.phase_frame == 0) && (state->phase_2.fly_delay > SARA_WAVE_2_FLY_DELAY_GUARD)", phase2)
        self.assertIn("state->phase_2.fly_delay -= SARA_WAVE_2_FLY_DELAY_STEP;", phase2)

    def test_phase_three_pattern_duration_overshoots_its_guard_to_two_hundred(self):
        duration = number("SARA_WAVE_3_PATTERN_FRAMES_INITIAL", SARA)
        guard = number("SARA_WAVE_3_PATTERN_FRAMES_GUARD", SARA)
        step = number("SARA_WAVE_3_PATTERN_FRAMES_STEP", SARA)
        values = [duration]
        while duration < guard:
            duration += step
            values.append(duration)
        self.assertEqual((guard, step, values), (180, 24, [80, 104, 128, 152, 176, 200]))
        phase3_leaf = SARA[SARA.index("static void near phase_3_with_pattern"):
                           SARA.index("void near pattern_pellet_arcs_at_expanding_random_angles")]
        self.assertIn("boss.phase_frame >= state->phase_3.pattern_frames", phase3_leaf)
        phase3 = sara_phase("SARA_PHASE_SPINNING_RINGS")
        self.assertIn("state->phase_3.pattern_frames < SARA_WAVE_3_PATTERN_FRAMES_GUARD", phase3)
        self.assertIn("state->phase_3.pattern_frames += SARA_WAVE_3_PATTERN_FRAMES_STEP;", phase3)

    def test_previous_pattern_byte_is_carried_across_the_phase_two_three_boundary(self):
        self.assertIn("sara_previous_pattern_mode_2_at_10", SARA)
        self.assertIn("sara_previous_pattern_mode_3_at_10", SARA)
        phase2_timeout = sara_phase("SARA_PHASE_BLUE_RED_WAVES")
        phase3_timeout = sara_phase("SARA_PHASE_SPINNING_RINGS")
        self.assertIn("state->phase_3.pattern_frames = SARA_WAVE_3_PATTERN_FRAMES_INITIAL;", phase2_timeout)
        self.assertNotIn("state->phase_3.previous_pattern_mode =", phase2_timeout)
        self.assertIn("state->phase_3.previous_pattern_mode", phase3_timeout)
        self.assertIn("previous_pattern_mode = boss.mode;", SARA)
        self.assertEqual(number("SARA_MODE_NO_PREVIOUS_PATTERN", SARA), 0xFF)

    def test_corridor_creates_two_mirrored_lasers_then_grows_on_frame_sixty_four(self):
        create = number("SARA_LASER_CREATE_FRAME", PROJECTILE_RULES)
        grow = number("SARA_LASER_GROW_FRAME", PROJECTILE_RULES)
        center = number("SARA_LASER_CORRIDOR_CENTER_ANGLE", PROJECTILE_RULES)
        offset = number("SARA_LASER_OFFSET_ANGLE", PROJECTILE_RULES)
        self.assertEqual((create, grow), (32, 64))
        self.assertEqual(((-center + offset) & 0xFF, (-center - offset) & 0xFF), (0xE0, 0xA0))
        self.assertEqual((number("X_RIGHT", SARA_HPP), number("X_LEFT", SARA_HPP)), (0, 1))
        self.assertEqual(number("SARA_LASER_WIDTH", PROJECTILE_RULES), 8)
        self.assertEqual(number("SARA_LASER_COLOR", PROJECTILE_RULES), 8)

        corridor_start = SARA.index("void near pattern_dense_spreads_and_random_balls_within_laser_walls")
        corridor_end = SARA.index("extern const pattern_loop_func_t SARA_PATTERNS_PHASE_2_3", corridor_start)
        corridor = SARA[corridor_start:corridor_end]
        self.assertIn("if(boss.phase_frame == SARA_LASER_CREATE_FRAME)", corridor)
        self.assertLess(corridor.index("SARA_CORRIDOR_FIXED_LASER(X_RIGHT"),
                        corridor.index("SARA_CORRIDOR_FIXED_LASER(X_LEFT"))
        self.assertIn("return;", corridor[corridor.index("if(boss.phase_frame == SARA_LASER_CREATE_FRAME)"):])
        self.assertIn("if(boss.phase_frame == SARA_LASER_GROW_FRAME)", corridor)
        self.assertIn("laser_manual_grow(X_RIGHT);", corridor)
        self.assertIn("laser_manual_grow(X_LEFT);", corridor)

    def test_corridor_angle_sweep_slows_at_four_exact_frames_and_stops_at_frame_180(self):
        frames, thresholds, right, left, interval = corridor_turns()
        self.assertEqual(thresholds, [
            (64, 0x80, 2), (128, 0x60, 3), (150, 0x58, 4), (180, 0x50, 5),
        ])
        # 0x50 is only the final slowdown threshold. Rotation continues six
        # more 5-frame turns until the independent terminal angle 0x4A.
        self.assertEqual((len(frames), frames[0], frames[-1]), (86, 33, 210))
        self.assertEqual((right, left, interval), (0x36, 0x4A, 5))
        self.assertIn("lasers[X_RIGHT].coords.angle += 0x01;", SARA)
        self.assertIn("lasers[X_LEFT].coords.angle -= 0x01;", SARA)
        self.assertIn("lasers[X_LEFT].coords.angle > SARA_LASER_ROTATION_TERMINAL_ANGLE", SARA)

    def test_corridor_ball_count_uses_boss_clock_but_spread_volley_uses_stage_clock(self):
        initial = number("SARA_LASER_INITIAL_BALL_COUNT", PROJECTILE_RULES)
        step = number("SARA_LASER_RANDOM_COUNT_STEP_FRAMES", PROJECTILE_RULES)
        limit = number("SARA_LASER_RANDOM_COUNT_LIMIT", PROJECTILE_RULES)
        counts = [initial]
        for frame in range(step, 1000, step):
            if counts[-1] < limit:
                counts.append(counts[-1] + 1)
        self.assertEqual(counts, [1, 2, 3, 4, 5, 6, 7, 8])

        corridor_start = SARA.index("void near pattern_dense_spreads_and_random_balls_within_laser_walls")
        corridor_end = SARA.index("extern const pattern_loop_func_t SARA_PATTERNS_PHASE_2_3", corridor_start)
        corridor = SARA[corridor_start:corridor_end]
        fire_tick = macro_int("SAR_CORRIDOR_FIRE_TICK", WAVE_SETTINGS)
        self.assertEqual(fire_tick, 0)
        self.assertIn("if(stage_frame_mod16 == SAR_CORRIDOR_FIRE_TICK)", corridor)
        self.assertLess(corridor.index("if(stage_frame_mod16 == SAR_CORRIDOR_FIRE_TICK)"),
                        corridor.index("SARA_LASER_RANDOM_COUNT_STEP_FRAMES"))
        self.assertIn("state->phase_4.random_ball_count++", corridor)
        self.assertIn("state->phase_4.spread_angle += 0x0E;", corridor)
        self.assertNotIn("boss.phase_frame % 16", corridor)

    def test_corridor_laser_growth_uses_post_update_age_and_hits_on_frame_seventy_three(self):
        age = 0
        width = 1
        state = "waiting"
        first_hit = None
        for frame in range(33, 100):
            if state == "growing":
                if age & 1:
                    width += 2
                if width >= number("SARA_LASER_WIDTH", PROJECTILE_RULES):
                    state = "active"
            elif state == "active":
                first_hit = frame
                break
            age += 1
            # Boss callback calls laser_manual_grow after this frame's
            # lasers_update; the age increment above therefore happens first.
            if frame == number("SARA_LASER_GROW_FRAME", PROJECTILE_RULES):
                state = "growing"
        self.assertEqual((first_hit, width, state), (73, 9, "active"))
        self.assertLess(GAMEPLAY_LOOP.index("lasers_update();"), GAMEPLAY_LOOP.index("boss_update();"))

    def test_corridor_timeout_runs_pattern_but_skips_hp_test_and_stops_both_lasers(self):
        timeout = number("SARA_LASER_CORRIDOR_TIMEOUT", SARA)
        self.assertEqual(timeout, 1300)
        phase4 = sara_phase("SARA_PHASE_LASER_CORRIDOR")
        self.assertLess(phase4.index("pattern_dense_spreads_and_random_balls_within_laser_walls();"),
                        phase4.index("if(boss.phase_frame >= SARA_LASER_CORRIDOR_TIMEOUT)"))
        timeout_branch = phase4[phase4.index("if(boss.phase_frame >= SARA_LASER_CORRIDOR_TIMEOUT)"):]
        else_branch = timeout_branch[timeout_branch.index("} else {"):]
        self.assertIn("boss.phase_state.defeat_bonus = false;", timeout_branch)
        self.assertIn("if(!boss_hittest_shots())", else_branch)
        self.assertIn("boss.phase_state.defeat_bonus = true;", else_branch)
        self.assertLess(timeout_branch.index("boss.phase_state.defeat_bonus = false;"),
                        timeout_branch.index("laser_stop(SARA_LASER_STOP_RIGHT);"))
        self.assertIn("laser_stop(SARA_LASER_STOP_RIGHT);", timeout_branch)
        self.assertIn("laser_stop(SARA_LASER_STOP_LEFT);", timeout_branch)
        self.assertIn("boss.phase = PHASE_BOSS_EXPLODE_SMALL;", timeout_branch)
        self.assertIn("boss.phase_frame = 0;", timeout_branch)
        self.assertLess(GAMEPLAY_LOOP.index("lasers_update();"), GAMEPLAY_LOOP.index("boss_update();"))


if __name__ == "__main__":
    unittest.main()
