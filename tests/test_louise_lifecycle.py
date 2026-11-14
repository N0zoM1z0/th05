"""Complete 582-byte Louise Boss phase controller and its two mode banks."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/louise/update.cpp").read_text()
HEADER = (ROOT / "src/main/boss/louise/update.hpp").read_text()
PHASES = (ROOT / "src/main/boss/louise/phase_choreography.hpp").read_text()
PATTERNS = (ROOT / "src/main/boss/louise/patterns.hpp").read_text()
SCRATCH = (ROOT / "src/main/boss/louise/scratch.hpp").read_text()


def number(name):
    for source in (UPDATE, HEADER, PHASES, PATTERNS, SCRATCH):
        for line in source.splitlines():
            needle = name + " = "
            if needle in line:
                raw = line.split(needle, 1)[1].split(";", 1)[0].strip().rstrip(",")
                return int(raw, 0)
    raise AssertionError(f"missing Louise constant {name}")


def phase(name, next_name):
    start = UPDATE.index(f"case {name}:")
    end = UPDATE.index(f"case {next_name}:", start + 1)
    return UPDATE[start:end]


def hp_ladder():
    return [number("LOUISE_HP_TOTAL"), number("LOUISE_HP_AFTER_SETUP"),
            number("LOUISE_HP_AFTER_BLUE_RED_WAVES"),
            number("LOUISE_HP_AFTER_MIRRORED_FANS"),
            number("LOUISE_HP_AFTER_LASER_RINGS")]


class LouiseLifecycleTests(unittest.TestCase):
    def test_eight_phase_switch_keys_and_hp_ladder_are_complete(self):
        expected = {
            "LOUISE_PHASE_SETUP": 0, "LOUISE_PHASE_READY": 1,
            "LOUISE_PHASE_BLUE_RED_SPREADS": 2, "LOUISE_PHASE_FIRE_TRANSITION_FIRST": 3,
            "LOUISE_PHASE_MIRRORED_FANS": 4, "LOUISE_PHASE_LASERS_AND_RINGS": 5,
            "LOUISE_PHASE_FIRE_TRANSITION_SECOND": 6, "LOUISE_PHASE_AIMED_PELLETS": 7,
        }
        self.assertEqual({name: number(name) for name in expected}, expected)
        self.assertEqual(hp_ladder(), [4400, 3000, 1900, 500, 0])
        self.assertIn("LOUISE_HP_AFTER_LASER_RINGS = 0", PHASES)

    def test_setup_and_ready_are_separate_invulnerable_128_and_64_frame_gates(self):
        self.assertEqual((number("LOUISE_FIRST_FRAME"), number("LOUISE_HP_FILL_FRAMES"), number("LOUISE_READY_FRAMES")), (1, 128, 64))
        setup = phase("LOUISE_PHASE_SETUP", "LOUISE_PHASE_READY")
        ready = phase("LOUISE_PHASE_READY", "LOUISE_PHASE_BLUE_RED_SPREADS")
        self.assertIn("if(boss.phase_frame == LOUISE_FIRST_FRAME)", setup)
        self.assertIn("boss.hp = LOUISE_HP_TOTAL;", setup)
        self.assertIn("boss.phase_end_hp = LOUISE_HP_AFTER_SETUP;", setup)
        self.assertIn("boss_hittest_shots_invincible();", setup)
        self.assertIn("if(boss.phase_frame >= LOUISE_HP_FILL_FRAMES)", setup)
        self.assertIn("if(boss.phase_frame >= LOUISE_READY_FRAMES)", ready)
        self.assertIn("boss.mode = LOUISE_MODE_BLUE_SPREADS;", ready)
        self.assertIn("louise_scratch.charge_speed = LOUISE_INITIAL_CHARGE_SPEED;", ready)
        self.assertIn("louise_scratch.blue_red_or_laser_direction = LOUISE_FIRST_PATTERN_BLUE;", ready)

    def test_first_wave_alternates_blue_red_by_pattern_parity_and_stops_at_twenty(self):
        self.assertEqual((number("LOUISE_BLUE_RED_PATTERN_LIMIT"), number("LOUISE_BLUE_RED_PATTERN_PARITY")), (20, 1))
        self.assertEqual((number("LOUISE_MODE_REPOSITION"), number("LOUISE_MODE_BLUE_SPREADS"), number("LOUISE_MODE_RED_STACKS")), (0, 1, 2))
        wave = phase("LOUISE_PHASE_BLUE_RED_SPREADS", "LOUISE_PHASE_FIRE_TRANSITION_FIRST")
        self.assertIn("louise_flystep(to_sp(1.0f), LOUISE_BLUE_RED_REPOSITION_FRAMES)", wave)
        self.assertIn("boss.mode = (boss.phase_state.patterns_seen & LOUISE_BLUE_RED_PATTERN_PARITY) + LOUISE_MODE_BLUE_SPREADS;", wave)
        self.assertIn("louise_pattern_blue_spreads();", wave)
        self.assertIn("louise_pattern_red_stacks();", wave)
        self.assertLess(wave.index("boss.phase_state.patterns_seen++"), wave.index("if(boss.phase_state.patterns_seen >= LOUISE_BLUE_RED_PATTERN_LIMIT)"))
        self.assertLess(wave.index("if(boss.phase_state.patterns_seen >= LOUISE_BLUE_RED_PATTERN_LIMIT)"), wave.index("LOUISE_HIT_BONUS_OR_BREAK();"))
        self.assertEqual(number("LOUISE_BLUE_RED_REPOSITION_FRAMES"), 96)

    def test_both_fire_transitions_are_strictly_64_frames_and_keep_shot_test_first(self):
        self.assertEqual(number("LOUISE_FIRE_TRANSITION_FRAMES"), 64)
        first = phase("LOUISE_PHASE_FIRE_TRANSITION_FIRST", "LOUISE_PHASE_MIRRORED_FANS")
        second = phase("LOUISE_PHASE_FIRE_TRANSITION_SECOND", "LOUISE_PHASE_AIMED_PELLETS")
        macro = UPDATE[UPDATE.index("#define LOUISE_FINISH_FIRE_TRANSITION()"):UPDATE.index("// Every regular attack phase")]
        self.assertIn("boss.phase_frame = LOUISE_PHASE_FRAME_RESET;", macro)
        self.assertIn("boss.phase++;", macro)
        self.assertIn("boss.sprite = LOUISE_SPRITE_FIRE;", macro)
        for block in (first, second):
            self.assertIn("boss_hittest_shots();", block)
            self.assertIn("LOUISE_FINISH_FIRE_TRANSITION();", block)
            self.assertLess(block.index("boss_hittest_shots();"), block.index("LOUISE_FINISH_FIRE_TRANSITION();"))

    def test_mirrored_fan_wave_has_twenty_cycles_and_moves_at_seven_eighths(self):
        self.assertEqual((number("LOUISE_MIRRORED_FAN_PATTERN_LIMIT"), number("LOUISE_MIRRORED_FAN_REPOSITION_FRAMES")), (20, 128))
        fans = phase("LOUISE_PHASE_MIRRORED_FANS", "LOUISE_PHASE_LASERS_AND_RINGS")
        self.assertIn("louise_pattern_mirrored_fans();", fans)
        self.assertIn("louise_flystep(to_sp(0.875f), LOUISE_MIRRORED_FAN_REPOSITION_FRAMES)", fans)
        self.assertIn("if(boss.phase_state.patterns_seen >= LOUISE_MIRRORED_FAN_PATTERN_LIMIT)", fans)
        self.assertIn("boss_phase_next(ET_SW_NE, LOUISE_HP_AFTER_MIRRORED_FANS);", fans)
        self.assertIn("louise_scratch.next_laser_ring_mode = LOUISE_LATER_PATTERN_SWEEP;", fans)
        self.assertIn("louise_scratch.charge_speed = LOUISE_LATER_CHARGE_SPEED;", fans)

    def test_laser_ring_wave_toggles_two_modes_and_ends_after_twenty_cycles(self):
        self.assertEqual((number("LOUISE_LASER_RING_PATTERN_LIMIT"), number("LOUISE_LASER_RING_REPOSITION_FRAMES")), (20, 48))
        wave = phase("LOUISE_PHASE_LASERS_AND_RINGS", "LOUISE_PHASE_FIRE_TRANSITION_SECOND")
        self.assertIn("boss.mode = louise_scratch.next_laser_ring_mode + LOUISE_MODE_SWEEPING_LASERS;", wave)
        self.assertIn("louise_scratch.next_laser_ring_mode = LOUISE_SECOND_PATTERN_TOGGLE - louise_scratch.next_laser_ring_mode;", wave)
        self.assertIn("louise_pattern_sweeping_lasers();", wave)
        self.assertIn("louise_pattern_turning_rings();", wave)
        self.assertLess(wave.index("boss.phase_state.patterns_seen++"), wave.index("if(boss.phase_state.patterns_seen >= LOUISE_LASER_RING_PATTERN_LIMIT)"))
        self.assertIn("boss_phase_next(ET_NW_SE, LOUISE_HP_AFTER_LASER_RINGS);", wave)
        self.assertEqual((number("LOUISE_INITIAL_CHARGE_SPEED"), number("LOUISE_LATER_CHARGE_SPEED")), (0x18, 0x14))

    def test_final_aimed_pellet_wave_has_ten_cycles_and_timeout_skips_hp_reward(self):
        self.assertEqual((number("LOUISE_AIMED_PELLET_PATTERN_LIMIT"), number("LOUISE_FINAL_REPOSITION_FRAMES")), (10, 128))
        final = UPDATE[UPDATE.index("case LOUISE_PHASE_AIMED_PELLETS:"):UPDATE.index("default:")]
        self.assertIn("louise_pattern_aimed_pellets();", final)
        self.assertIn("louise_flystep(to_sp(0.5f), LOUISE_FINAL_REPOSITION_FRAMES)", final)
        self.assertLess(final.index("if(boss.phase_state.patterns_seen >= LOUISE_AIMED_PELLET_PATTERN_LIMIT)"), final.index("if(!boss_hittest_shots())"))
        self.assertIn("boss.phase_state.defeat_bonus = false;", final)
        self.assertIn("boss.phase_state.defeat_bonus = true;", final)
        self.assertIn("explode_small:", final)
        self.assertIn("boss.phase = PHASE_BOSS_EXPLODE_SMALL;", final)

    def test_scratch_bytes_are_phase_reused_not_new_storage(self):
        self.assertIn("louise_scratch_is_16", SCRATCH)
        self.assertIn("louise_charge_speed_at_10", SCRATCH)
        self.assertIn("louise_pattern_choice_at_14", SCRATCH)
        self.assertIn("louise_direction_at_15", SCRATCH)
        self.assertIn("LOUISE_PHASE_FRAME_RESET = 0", PHASES)
        self.assertIn("LOUISE_PATTERN_COUNT_RESET = 0", PHASES)
        self.assertIn("boss.phase_state.patterns_seen = LOUISE_PATTERN_COUNT_RESET;", UPDATE)


if __name__ == "__main__":
    unittest.main()
