"""Full 939-byte Alice controller: wave ladder, puppets, beams and final spread."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/alice/update_context.cpp").read_text()
HEADER = (ROOT / "src/main/boss/alice/update.hpp").read_text()
BEAM_RULES = (ROOT / "src/main/boss/alice/beam_weapon_rules.hpp").read_text()
BEAM_PHASE = (ROOT / "src/main/boss/alice/beam_phase.hpp").read_text()
PUPPETS = (ROOT / "src/main/boss/alice/puppet_choreography.hpp").read_text()
SCRATCH = (ROOT / "src/main/boss/alice/scratch.hpp").read_text()


def number(name):
    for source in (UPDATE, HEADER, BEAM_RULES, BEAM_PHASE, PUPPETS, SCRATCH):
        for line in source.splitlines():
            stripped = line.strip()
            needle = name + " = "
            if needle in stripped:
                raw = stripped.split(needle, 1)[1].split(";", 1)[0].strip().rstrip(",")
                return int(raw, 0)
    raise AssertionError(f"missing Alice constant {name}")


def phase(name, next_name):
    start = UPDATE.index(f"case {name}:")
    end = UPDATE.index(f"case {next_name}:", start + 1)
    return UPDATE[start:end]


def phase_until(name, end_token):
    start = UPDATE.index(f"case {name}:")
    end = UPDATE.index(end_token, start + 1)
    return UPDATE[start:end]


def hp_ladder():
    current_end = number("ALICE_WAVE_ONE_END_HP")
    current_hp = number("ALICE_HP_TOTAL")
    rows = []
    for wave in range(4):
        current_hp = current_end
        rows.append(current_hp)
        if wave < 3:
            current_end -= number("ALICE_WAVE_HP_DECREMENT")
        else:
            current_end = number("ALICE_FINAL_WAVE_END_HP")
    return rows, current_end


class AliceLifecycleTests(unittest.TestCase):
    def test_full_phase_enum_is_the_original_fifteen_phase_sequence(self):
        expected = {
            "ALICE_PHASE_SETUP": 0, "ALICE_PHASE_READY": 1,
            "ALICE_PHASE_PUPPET_ENTRANCE": 2, "ALICE_PHASE_PATTERN_WAVE_1": 3,
            "ALICE_PHASE_BEAM_APPROACH_1": 4, "ALICE_PHASE_BEAM_ATTACK_1": 5,
            "ALICE_PHASE_PATTERN_WAVE_2": 6, "ALICE_PHASE_BEAM_APPROACH_2": 7,
            "ALICE_PHASE_BEAM_ATTACK_2": 8, "ALICE_PHASE_PATTERN_WAVE_3": 9,
            "ALICE_PHASE_BEAM_APPROACH_3": 10, "ALICE_PHASE_BEAM_ATTACK_3": 11,
            "ALICE_PHASE_PATTERN_WAVE_4": 12, "ALICE_PHASE_RING_APPROACH": 13,
            "ALICE_PHASE_FINAL_SPREAD": 14,
        }
        self.assertEqual({name: number(name) for name in expected}, expected)
        self.assertIn("ALICE_PHASE_EXPLODE_SMALL = 253", HEADER)
        self.assertIn("ALICE_PHASE_EXPLODE_BIG = 254", HEADER)

    def test_setup_ready_and_puppet_entrance_have_distinct_strict_clocks(self):
        self.assertEqual((number("ALICE_SETUP_ENTRY_FRAME"), number("ALICE_SETUP_EXIT_FRAME"), number("ALICE_READY_EXIT_FRAME"), number("ALICE_PUPPET_APPEAR_FRAME")), (1, 128, 64, 128))
        setup = phase("ALICE_PHASE_SETUP", "ALICE_PHASE_READY")
        ready = phase("ALICE_PHASE_READY", "ALICE_PHASE_PUPPET_ENTRANCE")
        entrance = phase("ALICE_PHASE_PUPPET_ENTRANCE", "ALICE_PHASE_PATTERN_WAVE_1")
        self.assertIn("if(boss.phase_frame == ALICE_SETUP_ENTRY_FRAME)", setup)
        self.assertIn("boss_hittest_shots_invincible();", setup)
        self.assertIn("if(boss.phase_frame >= ALICE_SETUP_EXIT_FRAME)", setup)
        self.assertIn("if(boss.phase_frame >= ALICE_READY_EXIT_FRAME)", ready)
        self.assertIn("alice_scratch.ready_phase_store_only = ALICE_READY_PHASE_STORE_VALUE;", ready)
        self.assertIn("if(boss.phase_frame == ALICE_PUPPET_APPEAR_FRAME)", entrance)
        self.assertIn("else if(boss.phase_frame > ALICE_PUPPET_APPEAR_FRAME)", entrance)
        self.assertIn("if(alice_puppet0.radius.radius_motion == ALICE_PUPPET_ENTRANCE_DONE)", entrance)
        self.assertEqual((number("ALICE_PUPPET_ENTRANCE_RADIUS_PX"), number("ALICE_PUPPET_HP")), (256, 500))

    def test_regular_wave_hp_thresholds_are_a_ladder_not_a_running_subtraction(self):
        rows, final = hp_ladder()
        self.assertEqual(number("ALICE_HP_TOTAL"), 9600)
        self.assertEqual(rows, [7400, 5200, 3000, 800])
        self.assertEqual(final, 0)
        wave = phase("ALICE_PHASE_PATTERN_WAVE_1", "ALICE_PHASE_BEAM_APPROACH_1")
        self.assertLess(wave.index("boss.hp = boss.phase_end_hp;"), wave.index("boss.phase_end_hp -= ALICE_WAVE_HP_DECREMENT;"))
        self.assertIn("if(boss.phase < ALICE_PHASE_PATTERN_WAVE_4)", wave)
        self.assertIn("boss.phase_end_hp = ALICE_FINAL_WAVE_END_HP;", wave)
        self.assertEqual(number("ALICE_WAVE_HP_DECREMENT"), 2200)

    def test_each_regular_wave_has_twenty_four_patterns_and_three_random_variants(self):
        self.assertEqual((number("ALICE_REGULAR_WAVE_PATTERN_LIMIT"), number("ALICE_REGULAR_WAVE_VARIANTS"), number("ALICE_RANDOM_FLYSTEP_LEAD_FRAMES")), (24, 3, 8))
        wave = phase("ALICE_PHASE_PATTERN_WAVE_1", "ALICE_PHASE_BEAM_APPROACH_1")
        self.assertIn("boss.phase_state.patterns_seen++", wave)
        self.assertLess(wave.index("boss.phase_state.patterns_seen++"), wave.index("if(boss.phase_state.patterns_seen >= ALICE_REGULAR_WAVE_PATTERN_LIMIT)"))
        self.assertLess(wave.index("if(boss.phase_state.patterns_seen >= ALICE_REGULAR_WAVE_PATTERN_LIMIT)"), wave.index("alice_pattern_current ="))
        self.assertIn("boss_flystep_random(boss.phase_frame - ALICE_RANDOM_FLYSTEP_LEAD_FRAMES)", wave)
        self.assertIn("alice_pattern_table[alice_scratch.attack_wave][randring2_next16_mod(ALICE_REGULAR_WAVE_VARIANTS)]", wave)
        self.assertEqual(number("ALICE_REGULAR_WAVE_BONUS"), 7)

    def test_wave_completion_orders_reward_clear_explosion_phase_and_hp_handoff(self):
        wave = phase("ALICE_PHASE_PATTERN_WAVE_1", "ALICE_PHASE_BEAM_APPROACH_1")
        positions = [
            wave.index("if(!boss_hittest_shots())"), wave.index("boss_score_bonus(ALICE_REGULAR_WAVE_BONUS);"),
            wave.index("boss_items_drop();"), wave.index("phase_complete:"), wave.index("alice_scratch.attack_wave++;"),
            wave.index("ALICE_ENSURE_CLEAR_WINDOW();"), wave.index("boss_explode_small(ET_NW_SE);"),
            wave.index("ALICE_NEXT_PHASE_AND_RESET_CLOCK();"), wave.index("boss.hp = boss.phase_end_hp;"),
            wave.index("boss.phase_end_hp -= ALICE_WAVE_HP_DECREMENT;"),
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(number("ALICE_BULLET_CLEAR_MIN_FRAMES"), 20)
        self.assertIn("static const int ALICE_PHASE_FRAME_RESET = 0;", UPDATE)
        self.assertIn("static const int ALICE_PATTERN_COUNT_RESET = 0;", UPDATE)

    def test_three_beam_approaches_hold_puppets_then_attack_with_strict_600_timeout(self):
        self.assertEqual((number("ALICE_BEAM_ATTACK_TIMEOUT"), number("ALICE_BEAM_WAVE_BONUS")), (600, 5))
        approach = phase("ALICE_PHASE_BEAM_APPROACH_1", "ALICE_PHASE_BEAM_ATTACK_1")
        attack = phase_until("ALICE_PHASE_BEAM_ATTACK_1", "case ALICE_PHASE_RING_APPROACH:")
        self.assertIn("ALICE_BEAM_PUPPETS_HOLD();", approach)
        self.assertIn("boss_flystep_towards(to_sp(ALICE_BOSS_APPROACH_X_PX)", approach)
        self.assertIn("ALICE_BEAM_PUPPETS_HOLD();", attack)
        self.assertIn("alice_puppet_beam_pattern();", attack)
        self.assertIn("boss_hittest_shots();", attack)
        self.assertLess(attack.index("if(boss.phase_frame < ALICE_BEAM_ATTACK_TIMEOUT)"), attack.index("boss_score_bonus(ALICE_BEAM_WAVE_BONUS);"))
        self.assertLess(attack.index("boss_score_bonus(ALICE_BEAM_WAVE_BONUS);"), attack.index("alice_scratch.beam_phase = ALICE_BEAM_INACTIVE;"))
        self.assertIn("alice_puppet_pattern0 = alice_puppet_spread;", attack)
        self.assertIn("alice_puppet0.phase_frame = alice_puppet1.phase_frame = ALICE_PUPPET_FRAME_RESET;", attack)
        self.assertEqual([frame for frame in (599, 600, 601) if frame < number("ALICE_BEAM_ATTACK_TIMEOUT")], [599])

    def test_beam_phase_byte_is_a_four_state_shared_lifecycle_not_a_counter(self):
        self.assertEqual({"ALICE_BEAM_INACTIVE": 0, "ALICE_BEAM_CHARGE_CIRCLES": 1, "ALICE_BEAM_CONTRACTING": 2, "ALICE_BEAM_SPRITES": 3}, {name: number(name) for name in ("ALICE_BEAM_INACTIVE", "ALICE_BEAM_CHARGE_CIRCLES", "ALICE_BEAM_CONTRACTING", "ALICE_BEAM_SPRITES")})
        self.assertEqual((number("ALICE_BEAM_CHARGE_START"), number("ALICE_BEAM_CONTRACT_START"), number("ALICE_BEAM_SPRITES_START"), number("ALICE_BEAM_FIRE_START")), (16, 32, 64, 80))
        self.assertIn("alice_beam_phase_at_9", SCRATCH)
        self.assertIn("alice_scratch.beam_phase = ALICE_BEAM_INACTIVE;", UPDATE)

    def test_ring_approach_uses_shared_movement_labels_and_resets_before_phase_increment(self):
        ring = phase("ALICE_PHASE_RING_APPROACH", "ALICE_PHASE_FINAL_SPREAD")
        self.assertIn("ALICE_RING_PUPPETS_ANCHOR();", ring)
        self.assertIn("alice_puppet_pattern0 = alice_puppet_pattern1 = alice_puppet_rings;", ring)
        self.assertLess(ring.index("movement_complete:"), ring.index("boss.phase_frame = ALICE_PHASE_FRAME_RESET;"))
        self.assertLess(ring.index("boss.phase_frame = ALICE_PHASE_FRAME_RESET;"), ring.index("boss.phase++;"))
        self.assertLess(ring.index("movement_hittest:"), ring.index("boss_hittest_shots();"))

    def test_final_spread_leaf_runs_before_strict_timeout_and_only_hp_hit_sets_bonus(self):
        self.assertEqual(number("ALICE_FINAL_SPREAD_TIMEOUT"), 1000)
        final = phase_until("ALICE_PHASE_FINAL_SPREAD", "default:")
        self.assertIn("alice_pattern_final_spread();", final)
        self.assertLess(final.index("alice_pattern_final_spread();"), final.index("if(boss.phase_frame < ALICE_FINAL_SPREAD_TIMEOUT)"))
        self.assertLess(final.index("if(boss.phase_frame < ALICE_FINAL_SPREAD_TIMEOUT)"), final.index("boss.phase_state.defeat_bonus = true;"))
        self.assertIn("boss.phase = ALICE_PHASE_EXPLODE_SMALL;", final)
        self.assertIn("alice_puppet0.flag = ALICE_PUPPET_DEFEAT_ANIMATION;", final)
        self.assertIn("alice_puppet1.flag = ALICE_PUPPET_DEFEAT_ANIMATION;", final)
        self.assertEqual([frame for frame in (999, 1000, 1001) if frame < number("ALICE_FINAL_SPREAD_TIMEOUT")], [999])

    def test_phase_sentinels_are_named_without_reusing_other_physical_roles(self):
        expected = {"ALICE_PHASE_FRAME_RESET": 0, "ALICE_PATTERN_COUNT_RESET": 0,
                    "ALICE_FIRST_ATTACK_WAVE": 0, "ALICE_FINAL_WAVE_END_HP": 0,
                    "ALICE_PUPPET_ENTRANCE_DONE": 0, "ALICE_BEAM_FRAME_RESET": 0,
                    "ALICE_PUPPET_FRAME_RESET": 0}
        self.assertEqual({name: number(name) for name in expected}, expected)
        self.assertIn("alice_scratch.ready_phase_store_only", UPDATE)
        self.assertIn("alice_scratch.attack_wave = ALICE_FIRST_ATTACK_WAVE;", UPDATE)
        self.assertIn("alice_scratch.beam_phase = ALICE_BEAM_INACTIVE;", UPDATE)
        self.assertIn("unsigned char charge_angle;", SCRATCH)


if __name__ == "__main__":
    unittest.main()
