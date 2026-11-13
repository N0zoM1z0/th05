"""The original Yumeko Stage 5 -> Shinki Stage 6 laser-width handoff."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
YUMEKO_UPDATE = (ROOT / "src/main/boss/yumeko/update.cpp").read_text()
YUMEKO_LASER = (ROOT / "src/main/boss/yumeko/laser_swords.cpp").read_text()
YUMEKO_LASER_TIMING = (ROOT / "src/main/boss/yumeko/laser_swords_timing.hpp").read_text()
STAGE_SETUP = (ROOT / "src/main/stage/setup.cpp").read_text()
LASER_CONTROL = (ROOT / "src/main/bullet/laser_control.cpp").read_text()
LASER_UPDATE = (ROOT / "src/main/bullet/laser_update.cpp").read_text()
GAMEPLAY_LOOP = (ROOT / "src/main/runtime/gameplay_loop.cpp").read_text()
SHINKI_UPDATE = (ROOT / "src/main/boss/shinki/update_context.cpp").read_text()
WING = (ROOT / "src/main/boss/shinki/wing_preparation.cpp").read_text()
WING_RULES = (ROOT / "src/main/boss/shinki/wing_preparation_rules.hpp").read_text()


def phase_block(source, name, next_marker):
    start = source.index(f"case {name}:")
    end = source.index(next_marker, start)
    return source[start:end]


def grow_window(target_width, initial_age):
    """Model one laser after manual_grow; gameplay loop updates laser first."""
    width = 1
    age = initial_age
    state = "grow"
    wing_frame = 1  # the release callback already advanced frame 0 to 1
    active_hit_updates = 0
    for _ in range(8):
        # lasers_update(): the GROW case does not fall through to hit-test
        if state == "grow":
            if age & 1:
                width += 2
            if width >= target_width:
                state = "active"
        elif state == "active":
            active_hit_updates += 1
        age += 1

        # boss_update(): frame 8 stops the now-active laser after this tick's
        # lasers_update(), so the current tick's hit-test still counts.
        if wing_frame >= 8:
            state = "stopped"
            break
        wing_frame += 1
    return active_hit_updates, width, state


class ShinkiYumekoLaserHandoffTests(unittest.TestCase):
    def test_yumeko_phase_seven_sets_width_six_before_the_stage_handoff(self):
        approach = phase_block(YUMEKO_UPDATE, "YUMEKO_PHASE_APPROACH_SECOND", "case YUMEKO_PHASE_STATIONARY_FIRST:")
        self.assertIn("yumeko_pattern = yumeko_pattern_laser_swords;", approach)
        stationary = phase_block(YUMEKO_UPDATE, "YUMEKO_PHASE_STATIONARY_SECOND", "case YUMEKO_PHASE_SWORD_SWEEP:")
        self.assertIn("yumeko_pattern();", stationary)
        self.assertIn("YUMEKO_ADVANCE_PHASE_CLOCK();", YUMEKO_UPDATE)

        self.assertIn("#define YLS_LASER_WIDTH 6", YUMEKO_LASER_TIMING)
        charge = YUMEKO_LASER[YUMEKO_LASER.index("if(boss.phase_frame < YLS_CHARGE_FRAMES)"):]
        self.assertIn("if(boss.phase_frame == YLS_CHARGE_SOUND_FRAME)", charge)
        self.assertIn("laser_template.coords.width.nonshrink = YLS_LASER_WIDTH;", charge)
        self.assertIn("YLS_CHARGE_SOUND_FRAME 16", YUMEKO_LASER_TIMING)
        self.assertEqual(int(re.search(r"#define YLS_LASER_WIDTH\s+(\d+)", YUMEKO_LASER_TIMING).group(1)), 6)

        # No later Yumeko phase or final-ring leaf overwrites the width.
        later = YUMEKO_UPDATE[YUMEKO_UPDATE.index("case YUMEKO_PHASE_SWORD_SWEEP:"):]
        self.assertNotIn("laser_template.coords.width", later)
        self.assertEqual(YUMEKO_LASER.count("laser_template.coords.width.nonshrink = YLS_LASER_WIDTH;"), 1)

    def test_stage_six_boss_reset_preserves_the_laser_template(self):
        stage5 = STAGE_SETUP[STAGE_SETUP.index("void pascal near stage5_setup"):STAGE_SETUP.index("void pascal near stage6_setup")]
        stage6 = STAGE_SETUP[STAGE_SETUP.index("void pascal near stage6_setup"):STAGE_SETUP.index("void pascal near stagex_setup")]
        reset_start = STAGE_SETUP.index("void near boss_reset(void)")
        reset_end = STAGE_SETUP.index("void pascal near bb_boss_load", reset_start)
        reset = STAGE_SETUP[reset_start:reset_end]
        self.assertIn("boss_update_func = yumeko_update;", stage5)
        self.assertIn("boss_reset();", stage5)
        self.assertIn("boss_update_func = shinki_update;", stage6)
        self.assertIn("boss_reset();", stage6)
        self.assertNotIn("laser_template", stage6)
        self.assertNotIn("laser_template", reset)

        # The Shinki controller updates only the per-frame origin, not width.
        self.assertIn("laser_template.coords.origin = boss.pos.cur;", SHINKI_UPDATE)
        self.assertNotIn("laser_template.coords.width", SHINKI_UPDATE)

    def test_manual_fixed_spawn_copies_inherited_width_and_starts_at_one(self):
        start = LASER_CONTROL.index("void pascal near laser_manual_fixed_spawn(int slot)")
        end = LASER_CONTROL.index("void pascal near laser_manual_grow", start)
        spawn = LASER_CONTROL[start:end]
        self.assertIn("laser.fixed_init(laser_template.coords.origin);", spawn)
        self.assertIn("laser.coords.width.nonshrink = 1;", spawn)
        self.assertIn("laser.grow_to_width = laser_template.coords.width.nonshrink;", spawn)

        self.assertIn("#define SWPREP_LASER_COUNT 6", WING_RULES)
        self.assertIn("#define SWPREP_WING_VISIBLE_FRAMES 8", WING_RULES)
        self.assertEqual(WING.count("laser_manual_fixed_spawn("), 6)
        self.assertEqual(WING.count("laser_manual_grow(i);"), 1)
        self.assertIn("if(wing_frame >= SWPREP_WING_VISIBLE_FRAMES)", WING)
        self.assertNotIn("laser_template.coords.width", WING)

    def test_width_six_leaves_two_or_three_hit_updates_but_width_eight_does_not(self):
        # Source loop order is critical: lasers update before the boss callback.
        self.assertLess(GAMEPLAY_LOOP.index("lasers_update();"), GAMEPLAY_LOOP.index("boss_update();"))
        grow = LASER_UPDATE[LASER_UPDATE.index("case LF_FIXED_GROW:"):LASER_UPDATE.index("case LF_FIXED_ACTIVE:")]
        self.assertIn("if(laser->age & 1)", grow)
        self.assertIn("laser->coords.width.nonshrink += 2;", grow)
        self.assertIn("if(laser->coords.width.nonshrink >= laser->grow_to_width)", grow)

        for age_parity in (0, 1):
            hits_six, final_six, state_six = grow_window(6, age_parity)
            hits_eight, final_eight, state_eight = grow_window(8, age_parity)
            self.assertGreaterEqual(hits_six, 2)
            self.assertLessEqual(hits_eight, 1)
            self.assertEqual(state_six, "stopped")
            self.assertEqual(state_eight, "stopped")
            self.assertGreaterEqual(final_six, 6)
            self.assertGreaterEqual(final_eight, 8)


if __name__ == "__main__":
    unittest.main()
