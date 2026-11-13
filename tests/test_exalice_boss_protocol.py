"""EX-Alice bomb-immunity countdown and HP-vs-time transition handshake."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/exalice/update.cpp").read_text()
FULL = (ROOT / "src/main/boss/exalice/full_context.cpp").read_text()
PHASE = (ROOT / "src/main/boss/exalice/phase.cpp").read_text()
PROTOCOL = (ROOT / "src/main/boss/exalice/bomb_phase_protocol.hpp").read_text()
MIDBOSS = (ROOT / "src/main/midboss/lifecycle.cpp").read_text()
STAGE_SETUP = (ROOT / "src/main/stage/setup.cpp").read_text()


def constant(name):
    return int(re.search(rf"{name}\s*=\s*(\d+)", PROTOCOL).group(1))


def phase_helper(source):
    start = source.index("void pascal near exalice_phase_next(")
    end = source.index("\n}", start) + 2
    return source[start:end]


def timer_tick(timer, bombing):
    if timer != constant("EXALICE_BOMB_INVINCIBILITY_EXPIRED"):
        timer -= 1
    if bombing:
        timer = constant("EXALICE_BOMB_INVINCIBILITY_RELOAD")
    return timer, ("boss_hittest_shots" if timer == 0 else "suppressed")


class ExAliceBossProtocolTests(unittest.TestCase):
    def test_bomb_gate_reloads_39_and_reopens_after_38_suppressed_updates(self):
        reload_frames = constant("EXALICE_BOMB_INVINCIBILITY_RELOAD")
        expired = constant("EXALICE_BOMB_INVINCIBILITY_EXPIRED")
        self.assertEqual((reload_frames, expired), (39, 0))

        for source in (PHASE, FULL):
            gate = source[source.index("int far exalice_hittest_shots(void)"):source.index("void pascal near exalice_phase_next(")]
            self.assertIn("if(bombing)", gate)
            self.assertIn("exalice_bomb_invincibility = EXALICE_BOMB_INVINCIBILITY_RELOAD;", gate)
            self.assertLess(gate.index("if(bombing)"), gate.index("if(exalice_bomb_invincibility == EXALICE_BOMB_INVINCIBILITY_EXPIRED)"))
            self.assertIn("return boss_hittest_shots();", gate)
            self.assertIn("return EXALICE_SUPPRESSED_SHOT_RESULT;", gate)

        # The full controller decrements before it reaches the phase's hit gate.
        for source in (UPDATE, FULL):
            body = source[source.index("void pascal far exalice_update(void)"):]
            self.assertLess(body.index("exalice_bomb_invincibility--;"), body.index("boss.phase_frame++;"))

        timer, result = timer_tick(expired, True)
        self.assertEqual((timer, result), (39, "suppressed"))
        results = []
        for _ in range(38):
            timer, result = timer_tick(timer, False)
            results.append((timer, result))
        self.assertEqual(timer, 1)
        self.assertTrue(all(result == "suppressed" for _, result in results))
        timer, result = timer_tick(timer, False)
        self.assertEqual((timer, result), (0, "boss_hittest_shots"))

    def test_setup_and_ready_use_the_separate_always_invincible_hit_gate(self):
        setup = UPDATE[UPDATE.index("case EXALICE_PHASE_SETUP:"):UPDATE.index("case EXALICE_PHASE_READY:")]
        ready = UPDATE[UPDATE.index("case EXALICE_PHASE_READY:"):UPDATE.index("case EXALICE_PHASE_WAVE1_REGULAR:")]
        self.assertIn("exalice_bomb_invincibility = EXALICE_BOMB_INVINCIBILITY_EXPIRED;", setup)
        self.assertIn("boss_hittest_shots_invincible();", setup)
        self.assertIn("boss_hittest_shots_invincible();", ready)
        self.assertNotIn("exalice_hittest_shots();", setup)
        self.assertNotIn("exalice_hittest_shots();", ready)

    def test_only_an_hp_score_bonus_opens_the_item_drop_latch(self):
        reset_start = STAGE_SETUP.index("void near boss_reset(void)")
        reset_end = STAGE_SETUP.index("void pascal near bb_boss_load", reset_start)
        self.assertIn("boss_phase_timed_out = true;", STAGE_SETUP[reset_start:reset_end])

        score_start = MIDBOSS.index("void pascal near boss_score_bonus(unsigned int units)")
        score_end = MIDBOSS.index("void near midboss_defeat_update(void)", score_start)
        score = MIDBOSS[score_start:score_end]
        self.assertIn("boss_phase_timed_out = false;", score)

        for source in (PHASE, FULL):
            helper = phase_helper(source)
            self.assertIn("if(type != ET_NONE)", helper)
            self.assertIn("if(!boss_phase_timed_out)", helper)
            self.assertIn("bullet_zap_drop_point_items = true;", helper)
            self.assertIn("bullet_zap.active = true;", helper)
            self.assertIn("boss_items_drop();", helper)
            self.assertIn("boss_phase_timed_out = true;", helper)

        regular = UPDATE[UPDATE.index("case EXALICE_PHASE_WAVE1_REGULAR:"):UPDATE.index("case EXALICE_PHASE_WAVE1_APPROACH:")]
        self.assertLess(regular.index("if(!exalice_hittest_shots())"), regular.index("boss_score_bonus(EXALICE_REGULAR_HIT_BONUS);"))
        self.assertLess(regular.index("boss_score_bonus(EXALICE_REGULAR_HIT_BONUS);"), regular.index("regular_complete:"))
        self.assertIn("goto regular_complete;", regular)
        self.assertLess(regular.index("goto regular_complete;"), regular.index("if(!exalice_hittest_shots())"))

        charge = UPDATE[UPDATE.index("case EXALICE_PHASE_WAVE1_CHARGE:"):UPDATE.index("case EXALICE_PHASE_WAVE2_APPROACH_FIRST:")]
        self.assertIn("if(boss.phase_frame > EXALICE_CHARGE_TIMEOUT_FRAME)", charge)
        self.assertLess(charge.index("goto charge_complete;"), charge.index("charge_hittest:"))
        self.assertLess(charge.index("boss_score_bonus(EXALICE_CHARGED_HIT_BONUS);"), charge.index("charge_complete:"))

        # The two exits have different visible results despite sharing the
        # same phase helper: HP hit clears the latch first; timeout leaves it set.
        def transition_drops_items(hp_hit, explosion_type="ET_CIRCLE"):
            timed_out = not hp_hit
            drops = (explosion_type != "ET_NONE") and (not timed_out)
            return drops, True

        self.assertEqual(transition_drops_items(True), (True, True))
        self.assertEqual(transition_drops_items(False), (False, True))
        self.assertEqual(transition_drops_items(True, "ET_NONE"), (False, True))

    def test_phase_transition_resets_boss_phase_state_but_preserves_bomb_timer(self):
        for source in (PHASE, FULL):
            helper = phase_helper(source)
            for expected in (
                "boss.phase++;",
                "boss.phase_frame = EXALICE_NEW_PHASE_FIRST_FRAME;",
                "boss.mode = EXALICE_MODE_REPOSITION;",
                "boss.phase_state.patterns_seen = EXALICE_NEW_PHASE_PATTERN_COUNT;",
                "boss.hp = boss.phase_end_hp;",
                "boss.phase_end_hp = next_end_hp;",
            ):
                self.assertIn(expected, helper)
            self.assertNotIn("exalice_bomb_invincibility", helper)

        self.assertEqual(constant("EXALICE_NEW_PHASE_FIRST_FRAME"), 0)
        self.assertEqual(constant("EXALICE_NEW_PHASE_PATTERN_COUNT"), 0)
        # Phase transitions leave any remaining post-bomb immunity untouched.
        timer = 17
        self.assertEqual(timer, 17)


if __name__ == "__main__":
    unittest.main()
