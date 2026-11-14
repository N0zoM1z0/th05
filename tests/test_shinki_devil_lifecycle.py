"""Shinki Devil byte-10 latch, laser timing, shot budget and phase teardown."""
from math import ceil
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEVIL = (ROOT / "src/main/boss/shinki/devil.inl").read_text()
BALLISTICS = (ROOT / "src/main/boss/shinki/devil_ballistics.hpp").read_text()
SCRATCH = (ROOT / "src/main/boss/shinki/scratch.hpp").read_text()
HP = (ROOT / "src/main/boss/shinki/hp.inl").read_text()
SHINKI = (ROOT / "src/main/boss/shinki/shinki.cpp").read_text()
CONTEXT = (ROOT / "src/main/boss/shinki/update_context.cpp").read_text()
GENERIC = (ROOT / "src/main/boss/generic.cpp").read_text()
GAMEPLAY_LOOP = (ROOT / "src/main/runtime/gameplay_loop.cpp").read_text()
LASER_CONTROL = (ROOT / "src/main/bullet/laser_control.cpp").read_text()
LASER_UPDATE = (ROOT / "src/main/bullet/laser_update.cpp").read_text()
PLAYER_UPDATE = (ROOT / "src/main/player/update.cpp").read_text()
PLAYER_UPDATE_HPP = (ROOT / "src/main/player/update.hpp").read_text()
SHOT_COMMON = (ROOT / "src/main/player/common.cpp").read_text()
SHOT_COMMON_HPP = (ROOT / "src/main/player/common.hpp").read_text()
SHOT_TABLES = (ROOT / "src/main/player/shot_tables.cpp").read_text()
SHOT_COLLISION = (ROOT / "src/main/player/shot_collision.cpp").read_text()
SHOT_RUNTIME = (ROOT / "src/main/player/shot_runtime.hpp").read_text()
PLAYER_SOURCES = {
    "Reimu": (ROOT / "src/main/player/reimu.cpp").read_text(),
    "Marisa": (ROOT / "src/main/player/marisa.cpp").read_text(),
    "Mima": (ROOT / "src/main/player/mima.cpp").read_text(),
    "Yuuka": (ROOT / "src/main/player/yuuka.cpp").read_text(),
}


def macro_int(name, source=DEVIL):
    match = re.search(rf"#define {name}\s+(0[xX][0-9A-Fa-f]+|[0-9]+)", source)
    if not match:
        raise AssertionError(f"missing macro {name}")
    return int(match.group(1), 0)


def enum_int(name, source=HP):
    match = re.search(rf"{name}\s*=\s*(\d+)", source)
    if not match:
        raise AssertionError(f"missing enum/static value {name}")
    return int(match.group(1))


def local_const(name, source=DEVIL):
    match = re.search(rf"{name}\s*=\s*(0[xX][0-9A-Fa-f]+|[0-9]+)", source)
    if not match:
        raise AssertionError(f"missing local constant {name}")
    return int(match.group(1), 0)


def controller_phase(source):
    start = source.index("case SHINKI_PHASE_SYMMETRIC_SPREADS:")
    end = source.index("case SHINKI_PHASE_DEFEAT_TRANSITION:", start)
    return source[start:end]


def outer_low_frames(last_frame=2400):
    """Execute the original 4-frame prelude and 2-angle-unit turn clock."""
    outer = 0
    intro_done = False
    direction = "clockwise"
    lows = []
    for frame in range(192, last_frame + 1):
        if frame % 4:
            continue
        if outer == 0x40 and not intro_done:
            intro_done = True
        if not intro_done:
            outer = (outer + 4) & 0xFF
        elif direction == "clockwise":
            outer = (outer - 2) & 0xFF
            if outer == 0x30:
                direction = "counterclockwise"
        else:
            outer = (outer + 2) & 0xFF
            if outer == 0x40:
                direction = "clockwise"
        if intro_done and outer == 0x30:
            lows.append(frame)
    return lows


def restore_latch_frame(trigger_frame, lows):
    """Model spawn, same-tick delay increment, grow and the first low-angle test."""
    delay = 0
    for frame in range(trigger_frame, trigger_frame + 200):
        if delay == 0:
            delay = 1  # the four fixed lasers are created in this callback
        if delay < 64:
            delay += 1
        elif delay == 64:
            delay += 1  # laser_manual_grow(), then 65
        elif frame in lows:
            return frame
    raise AssertionError("Devil byte-10 latch did not restore")


class ShinkiDevilLifecycleTests(unittest.TestCase):
    def test_laser_latch_is_the_phase_relative_byte_and_is_restored_before_exit(self):
        self.assertIn("unsigned char wave_relative_index;", SCRATCH)
        self.assertIn("unsigned char devil_lasers_active;", SCRATCH)
        self.assertIn("sizeof(ShinkiWaveOrDevilLaserLatch) == 1", SCRATCH)
        self.assertIn("offsetof(ShinkiPhaseScratch, wave_or_laser) == 10", SCRATCH)
        self.assertIn("offsetof(ShinkiDevilScratch, wave_or_laser) == 10", SCRATCH)
        self.assertIn("#define phase_relative shinki_scratch.wave_or_laser.wave_relative_index", SHINKI)
        self.assertRegex(DEVIL, r"#define\s+lasers_active\s+shinki_devil_scratch\.wave_or_laser\.devil_lasers_active")

        startup = DEVIL[DEVIL.index("if(phase_frame_minus_startup_delay == 0)"):]
        self.assertIn("lasers_active = false;", startup)
        latch = DEVIL[DEVIL.index("} else if(!lasers_active)"):DEVIL.index("} else if((boss.phase_frame % DEVIL_LASER_TURN_INTERVAL_FRAMES)")]
        self.assertIn("if(bullet_angle_outer == DEVIL_SPREAD_OUTER_LOW)", latch)
        self.assertIn("lasers_active++;", latch)

        for source in (SHINKI, CONTEXT):
            phase = controller_phase(source)
            attack_call = "wing_pattern();" if "wing_pattern();" in phase else "SHINKI_WING_FLIGHT_AND_ATTACK();"
            self.assertLess(phase.index(attack_call), phase.index("phase_done = boss_hittest_shots();"))
            self.assertLess(phase.index("phase_done = boss_hittest_shots();"), phase.index("if(phase_relative == SHINKI_FIRST_SHARED_WAVE)"))
            first = phase[phase.index("if(phase_relative == SHINKI_FIRST_SHARED_WAVE)"):phase.index("} else {")]
            self.assertIn("boss_phase_next(ET_SW_NE, HP_PHASE_10_END);", first)
            self.assertIn("shinki_wing_pattern = pattern_devil;", first)
            self.assertIn("phase_relative++;", first)

        self.assertEqual(enum_int("HP_PHASE_9_END"), 8600)
        self.assertEqual(enum_int("HP_PHASE_10_DEVIL_LASER"), 5600)
        self.assertEqual(enum_int("HP_PHASE_10_END"), 2800)
        phase_next = GENERIC[GENERIC.index("void pascal near boss_phase_next("):GENERIC.index("// Complete natural 414-byte defeat function")]
        self.assertLess(phase_next.index("boss.hp = boss.phase_end_hp;"), phase_next.index("boss.phase_end_hp = next_end_hp;"))

    def test_four_frame_bullet_clock_restores_byte_ten_within_127_updates(self):
        self.assertEqual(local_const("DEVIL_PATTERN_START_FRAME"), 192)
        self.assertEqual(local_const("DEVIL_SPREAD_INTERVAL_FRAMES"), 4)
        self.assertEqual(local_const("DEVIL_PRELUDE_OUTER_STEP"), 4)
        self.assertEqual(local_const("DEVIL_TURN_OUTER_STEP"), 2)
        self.assertEqual(local_const("DEVIL_SPREAD_OUTER_LOW"), 0x30)
        self.assertEqual(local_const("DEVIL_SPREAD_OUTER_HIGH"), 0x40)
        lows = outer_low_frames()
        self.assertEqual(lows[:4], [284, 348, 412, 476])
        self.assertEqual([b - a for a, b in zip(lows, lows[1:])], [64] * (len(lows) - 1))

        # The laser spawn callback increments delay 0->1 and then 1->2 in
        # its bottom-of-leaf delay branch. Grow occurs on T+63; the first
        # outer-low check is T+64, and a missed low recurs at most 64 later.
        self.assertEqual(restore_latch_frame(192, lows), 284)
        worst = max(
            (restore_latch_frame(trigger, lows) - trigger, trigger, restore_latch_frame(trigger, lows))
            for trigger in range(192, 1801)
        )
        self.assertEqual(worst, (127, 1757, 1884))
        self.assertEqual(local_const("DEVIL_FORCE_LASER_FRAME"), 1800)

        trigger = DEVIL[DEVIL.index("// Laser activation"):DEVIL.index("// Spread bullets")]
        self.assertIn("boss.hp <= HP_PHASE_10_DEVIL_LASER", trigger)
        self.assertIn("boss.phase_frame >= DEVIL_FORCE_LASER_FRAME", trigger)
        self.assertIn("laser_grow_delay++;", trigger)

    def test_real_fixed_lasers_become_collidable_before_the_phase_latch_restores(self):
        spawn_start = LASER_CONTROL.index("void pascal near laser_manual_fixed_spawn(int slot)")
        spawn_end = LASER_CONTROL.index("void pascal near laser_manual_grow", spawn_start)
        spawn = LASER_CONTROL[spawn_start:spawn_end]
        self.assertIn("laser.fixed_init(laser_template.coords.origin);", spawn)
        self.assertIn("laser.coords.width.nonshrink = 1;", spawn)
        self.assertIn("laser.grow_to_width = laser_template.coords.width.nonshrink;", spawn)

        grow_start = LASER_CONTROL.index("void pascal near laser_manual_grow(int slot)")
        grow_end = LASER_CONTROL.index("void pascal near laser_stop", grow_start)
        self.assertIn("LF_FIXED_WAIT_TO_GROW", LASER_CONTROL[grow_start:grow_end])
        self.assertIn("LF_FIXED_GROW", LASER_CONTROL[grow_start:grow_end])

        grow = LASER_UPDATE[LASER_UPDATE.index("case LF_FIXED_GROW:"):LASER_UPDATE.index("case LF_FIXED_ACTIVE:")]
        self.assertIn("if(laser->age & 1)", grow)
        self.assertIn("laser->coords.width.nonshrink += 2;", grow)
        self.assertIn("if(laser->coords.width.nonshrink >= laser->grow_to_width)", grow)
        self.assertNotIn("laser_hittest(*laser);", grow)
        active = LASER_UPDATE[LASER_UPDATE.index("case LF_FIXED_ACTIVE:"):LASER_UPDATE.index("case LF_FIXED_SHRINK:")]
        self.assertIn("laser_hittest(*laser);", active)

        # The trigger frame creates the laser after lasers_update. Its age is
        # 63 at the T+63 grow callback, then widths 3/5/7 are reached at
        # T+64/T+66/T+68; the first active hit-test is T+69.
        age, width = 63, 1
        active_frame = None
        for delta in range(1, 10):
            if age & 1:
                width += 2
            if width >= 6:
                active_frame = delta
                break
            age += 1
        self.assertEqual((active_frame, width), (5, 7))
        self.assertLess(69, 127)

    def test_all_player_levels_fit_inside_the_2800_hp_latch_safety_gap(self):
        # Exact raw damage emitted over one 18-frame shot cycle, levels 0..9.
        # The six shot_time values are 18/15/12/9/6/3; level 0/1 use shot_l0/l1.
        cycle_damage = {
            "Reimu": [30, 30, 38, 62, 87, 93, 93, 147, 153, 155],
            "Marisa": [30, 30, 56, 94, 126, 120, 148, 170, 148, 180],
            "Mima": [30, 30, 84, 102, 138, 159, 159, 207, 207, 228],
            "Yuuka": [30, 30, 39, 72, 87, 111, 132, 156, 177, 201],
        }
        max_damage_by_level = {
            "Reimu": [10, 10, 10, 9, 9, 9, 9, 9, 9, 9],
            "Marisa": [10, 10, 16, 13, 12, 11, 11, 11, 10, 9],
            "Mima": [10, 10, 8, 7, 7, 7, 7, 7, 7, 7],
            "Yuuka": [10, 10, 9, 8, 7, 7, 7, 7, 7, 7],
        }
        max_single_damage = {name: max(values) for name, values in max_damage_by_level.items()}
        multipliers = {
            "Reimu": (5, 4), "Marisa": (4, 5),
            "Mima": (4, 5), "Yuuka": (5, 4),
        }
        expected = {"Reimu": 2270, "Marisa": 1652, "Mima": 1818, "Yuuka": 2570}

        self.assertEqual(enum_int("HP_PHASE_10_DEVIL_LASER"), 5600)
        self.assertEqual(enum_int("HP_PHASE_10_END"), 2800)
        self.assertEqual(enum_int("PLAYER_UPDATE_SHOT_CYCLE", PLAYER_UPDATE_HPP), 18)
        self.assertIn("if(shot_time != 0)", PLAYER_UPDATE)
        self.assertIn("playchar_shot_func();", PLAYER_UPDATE)
        self.assertIn("shot_time--;", PLAYER_UPDATE)
        self.assertEqual(SHOT_COMMON.count("case "), 6)
        for value in (18, 15, 12, 9, 6, 3):
            self.assertIn(f"case {value}:", SHOT_COMMON)
        self.assertIn("SHOT_RUNTIME_COUNT = 64", SHOT_RUNTIME)
        self.assertIn("extern shot_alive_t shots_alive[SHOT_RUNTIME_COUNT];", SHOT_RUNTIME)

        # The initialized function table covers every character at all ten
        # levels. The per-level damage ledger models each source loop's six
        # shot_time masks, ShotAddIterator count and damage-setting branches.
        match = re.search(r"SHOT_FUNCS\[.*?=\s*\{(.*?)\n\};", SHOT_TABLES, re.S)
        self.assertIsNotNone(match)
        rows = [re.findall(r"shot_[a-z0-9_]+", row) for row in re.findall(r"\{([^{}]+)\}", match.group(1))]
        self.assertEqual(rows, [
            ["shot_l0", "shot_l1"] + [f"shot_reimu_l{i}" for i in range(2, 10)],
            ["shot_l0", "shot_l1"] + [f"shot_marisa_l{i}" for i in range(2, 10)],
            ["shot_l0", "shot_l1"] + [f"shot_mima_l{i}" for i in range(2, 10)],
            ["shot_l0", "shot_l1"] + [f"shot_yuuka_l{i}" for i in range(2, 10)],
        ])
        self.assertIn("shot->damage = 10;", SHOT_COMMON)
        damage_tokens = {
            "Reimu": r"(?:shot->damage\s*=\s*|set_option_sprite_and_damage\(|set_homing\(shot,\s*|reimu_forward\(shot,\s*sai,\s*)(\d+)",
            "Marisa": r"(?:shot->damage\s*=\s*|set_option_sprite_and_damage\(|marisa_stars\(shot,\s*)(\d+)",
            "Mima": r"(?:shot->damage\s*=\s*|set_option_sprite_and_damage\()(\d+)",
            "Yuuka": r"(?:shot->damage\s*=\s*|set_option_sprite_and_damage\()(\d+)",
        }
        self.assertEqual({
            name: max(map(int, re.findall(damage_tokens[name], source + SHOT_COMMON)))
            for name, source in PLAYER_SOURCES.items()
        }, max_single_damage)
        self.assertEqual({name: max(values) for name, values in cycle_damage.items()},
            {"Reimu": 155, "Marisa": 180, "Mima": 228, "Yuuka": 201})

        # 128 frames contain at most ceil(128/18)=8 complete shot cycles.
        # The 64 live shots at the 5600-HP crossing and all future volleys are
        # both charged at their full source damage, before the Stage 6 factor.
        cycles_in_window = ceil(128 / 18)
        self.assertEqual(cycles_in_window, 8)
        actual = {}
        mixed_bomb_bounds = {}
        for character, totals in cycle_damage.items():
            self.assertEqual(len(totals), 10)
            self.assertEqual(len(max_damage_by_level[character]), 10)
            numerator, denominator = multipliers[character]
            fixed_level = [
                ceil((64 * damage + cycles_in_window * cycle) * numerator / denominator)
                for damage, cycle in zip(max_damage_by_level[character], totals)
            ]
            actual[character] = max(fixed_level)
            mixed_bomb_bounds[character] = max(
                bomb_frames + ceil((64 * damage + ceil((128 - bomb_frames) / 18) * cycle) * numerator / denominator)
                for damage, cycle in zip(max_damage_by_level[character], totals)
                for bomb_frames in range(128)
            )
        self.assertEqual(actual, expected)
        self.assertEqual(actual, {"Reimu": 2270, "Marisa": 1652, "Mima": 1818, "Yuuka": 2570})
        self.assertLess(max(actual.values()), 2800)
        self.assertEqual(2800 - max(actual.values()), 230)
        self.assertEqual(mixed_bomb_bounds, {"Reimu": 2271, "Marisa": 1653, "Mima": 1819, "Yuuka": 2571})
        self.assertEqual(2800 - max(mixed_bomb_bounds.values()), 229)

        # shots_hittest divides by hit ordinal and clamps each share to one;
        # no hit can contribute more than its shot's full damage.
        self.assertIn("alive->shot->damage) / hits", SHOT_COLLISION)
        self.assertIn("if(!_AX) _AX = 1;", SHOT_COLLISION)
        self.assertIn("if(stage_id == 6)", SHOT_COLLISION)
        self.assertIn("damage *= 5;", SHOT_COLLISION)
        self.assertIn("damage = damage / 4;", SHOT_COLLISION)
        self.assertIn("damage *= 4;", SHOT_COLLISION)
        self.assertIn("damage /= 5;", SHOT_COLLISION)

    def test_bombs_cannot_skip_the_alias_restore_and_phase_exit_owns_cleanup(self):
        for source in (SHINKI, CONTEXT):
            phase = controller_phase(source)
            bomb = phase[phase.index("if(bombing)"):phase.index("if(!phase_done)")]
            self.assertIn("boss.hp += (boss.damage_this_frame - SHINKI_BOMB_DAMAGE_PER_FRAME);", bomb)
            self.assertIn("phase_done = false;", bomb)
            self.assertLess(bomb.index("phase_done = false;"), phase.index("if(!phase_done)"))
            self.assertLess(phase.index("boss_phase_next(ET_HORIZONTAL, HP_PHASE_12_END);"), phase.index("laser_stop(SHINKI_DEVIL_LASER_SLOT_A);"))
            for slot in ("A", "B", "C", "D"):
                self.assertIn(f"laser_stop(SHINKI_DEVIL_LASER_SLOT_{slot});", phase)

        self.assertLess(GAMEPLAY_LOOP.index("player_update();"), GAMEPLAY_LOOP.index("lasers_update();"))
        self.assertLess(GAMEPLAY_LOOP.index("lasers_update();"), GAMEPLAY_LOOP.index("boss_update();"))
        stop_start = LASER_CONTROL.index("void pascal near laser_stop(int slot)")
        stop_end = LASER_CONTROL.index("\n}", stop_start) + 2
        stop = LASER_CONTROL[stop_start:stop_end]
        self.assertIn("LF_FIXED_ACTIVE", stop)
        self.assertIn("LF_FIXED_SHRINK", stop)
        self.assertIn("LF_FREE", stop)
        self.assertIn("LF_SHOOTOUT_DECAY", stop)
        self.assertNotIn("laser_stop(", DEVIL)

    def test_ranked_b6ball_and_fast_interval_switches_keep_their_order(self):
        starts = {
            "EASY": macro_int("DEVIL_BALL_START_EASY", BALLISTICS),
            "NORMAL": macro_int("DEVIL_BALL_START_NORMAL", BALLISTICS),
            "HARD": macro_int("DEVIL_BALL_START_HARD", BALLISTICS),
            "LUNATIC": macro_int("DEVIL_BALL_START_LUNATIC", BALLISTICS),
        }
        first = {rank: ((256 + interval - 1) // interval) * interval for rank, interval in starts.items()}
        self.assertEqual(first, {"EASY": 256, "NORMAL": 280, "HARD": 256, "LUNATIC": 280})
        self.assertEqual(
            [macro_int(f"DEVIL_BALL_FAST_{rank}", BALLISTICS) for rank in ("EASY", "NORMAL", "HARD", "LUNATIC")],
            [52, 20, 16, 12],
        )
        self.assertEqual(local_const("DEVIL_FAST_STAGE_FRAME"), 2500)
        self.assertEqual(local_const("DEVIL_LASER_TURN_INTERVAL_FRAMES"), 8)

        spread_start = DEVIL.index("// Spread bullets")
        spread_end = DEVIL.index("// Lasers", spread_start)
        spread = DEVIL[spread_start:spread_end]
        laser_start = DEVIL.index("// Lasers")
        laser = DEVIL[laser_start:]
        self.assertLess(DEVIL.index("// Aimed 32x32 balls"), DEVIL.index("if((boss.hp <= HP_PHASE_10_DEVIL_FAST)"))
        self.assertLess(laser.index("if((boss.hp <= HP_PHASE_10_DEVIL_FAST)"), laser.index("b6ball_interval = select_for_rank("))
        self.assertLess(2500, 2504)
        self.assertEqual(2504 % 8, 0)
        self.assertEqual(2500 % 8, 4)
        self.assertIn("if((laser_grow_delay++) == DEVIL_FAST_DELAY_SENTINEL)", laser)
        self.assertEqual(local_const("DEVIL_FAST_DELAY_SENTINEL"), 65)

    def test_fast_stage_delay_sentinel_is_a_nonwrapping_16bit_counter(self):
        state = (ROOT / "src/main/boss/shinki/devil_float_state.h").read_text()
        self.assertIn("extern int near shinki_devil_laser_grow_delay;", state)
        self.assertIn("shinki_devil_laser_delay_is_2[(sizeof(int) == 2)", state)
        self.assertEqual(local_const("DEVIL_LASER_GROW_FRAMES"), 64)
        self.assertEqual(local_const("DEVIL_FAST_DELAY_SENTINEL"), 65)
        wing_rules = (ROOT / "src/main/boss/shinki/wing_attack_rules.hpp").read_text()
        timeout_frames = macro_int("SHW_WING_PHASE_TIMEOUT_FRAMES", wing_rules)
        self.assertEqual(timeout_frames, 3000)
        max_turns = (timeout_frames + local_const("DEVIL_LASER_TURN_INTERVAL_FRAMES") - 1) // local_const("DEVIL_LASER_TURN_INTERVAL_FRAMES")
        self.assertEqual(max_turns, 375)
        # Turbo C++ target int is signed 16-bit; even a full timeout after the
        # fast gate cannot wrap the post-grow counter back to its sentinel.
        self.assertLess(65 + max_turns, 0x7FFF)
        laser_code = DEVIL[DEVIL.index("// Lasers"):]
        self.assertIn("laser_grow_delay++", laser_code)
        self.assertIn("Growth leaves this 16-bit delay at 65", laser_code)


if __name__ == "__main__":
    unittest.main()
