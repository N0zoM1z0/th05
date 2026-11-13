"""EX-Alice's 223-byte final fan, inclusive timeout and HP-scaled orbit."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEAF = (ROOT / "src/main/boss/exalice/final_patterns.cpp").read_text()
UPDATE = (ROOT / "src/main/boss/exalice/update.cpp").read_text()
FULL = (ROOT / "src/main/boss/exalice/full_context.cpp").read_text()
RULES = (ROOT / "src/main/boss/exalice/final_attack_rules.hpp").read_text()
PHASES = (ROOT / "src/main/boss/exalice/update_phases.hpp").read_text()
GENERIC = (ROOT / "src/main/boss/generic.hpp").read_text()


def value(name):
    return int(re.search(rf"#define {name}\s+(0[xX][0-9A-Fa-f]+|[0-9]+)", RULES).group(1), 0)


def enum_value(name):
    return int(re.search(rf"{name}\s*=\s*(\d+)", PHASES).group(1))


def final_case(source):
    start = source.index("case EXALICE_PHASE_FINAL_FAN:")
    end = source.index("default:", start)
    return source[start:end]


class ExAliceFinalFanTests(unittest.TestCase):
    def test_two_frame_volley_schedule_includes_frame_5000(self):
        start = value("EXF_FAN_FIRE_START")
        cadence = value("EXF_FAN_FIRE_CADENCE")
        timeout = enum_value("EXALICE_FINAL_FAN_TIMEOUT_FRAME")
        frames = list(range(start, timeout + 1, cadence))
        self.assertEqual((start, cadence, timeout), (128, 2, 5000))
        self.assertEqual(len(frames), 2437)
        self.assertEqual((frames[0], frames[-1]), (128, 5000))
        self.assertEqual(2 * len(frames), 4874)
        self.assertEqual(5000 % cadence, 0)
        self.assertNotEqual(5001 % cadence, 0)

        leaf = LEAF[LEAF.index("void near exalice_pattern_final_fan(void)"):]
        self.assertIn("if(boss.phase_frame >= EXF_FAN_FIRE_START)", leaf)
        self.assertIn("if((boss.phase_frame % EXF_FAN_FIRE_CADENCE) == 0)", leaf)
        self.assertIn("EXF_FAN_CHARGE_FRAME 64", RULES)
        self.assertIn("EXF_FAN_FIRE_START 128", RULES)

    def test_opposite_bullets_rotate_by_seven_degrees_per_volley(self):
        opposite = value("EXF_FAN_OPPOSITE_ANGLE")
        step = value("EXF_FAN_ROTATION_STEP")
        volleys = 2437
        self.assertEqual((opposite, step), (0x80, 0x87))
        self.assertEqual((opposite + step) & 0xFF, 7)
        first_angle = 0x35  # arbitrary seeded byte; the real seed is random
        last_first = (first_angle + (volleys - 1) * 7) & 0xFF
        last_second = (last_first + opposite) & 0xFF
        after_last = (last_first + opposite + step) & 0xFF
        self.assertEqual((last_first - first_angle) & 0xFF, 0x9C)
        self.assertEqual((last_second - first_angle) & 0xFF, 0x1C)
        self.assertEqual((after_last - first_angle) & 0xFF, 0xA3)

        # The Boss orbit clock advances by two on every frame, not only on
        # volley frames. It runs on the terminal frame 5001 as well.
        orbit_angle_at_5000 = (2 * (5000 - 128)) & 0xFF
        orbit_angle_at_5001 = (orbit_angle_at_5000 + 2) & 0xFF
        orbit_angle_after_5001 = (orbit_angle_at_5001 + 2) & 0xFF
        self.assertEqual((orbit_angle_at_5000, orbit_angle_at_5001, orbit_angle_after_5001), (16, 18, 20))

        leaf = LEAF[LEAF.index("void near exalice_pattern_final_fan(void)"):]
        self.assertIn("bullets_add_regular();", leaf)
        self.assertLess(leaf.index("bullet_template.angle += EXF_FAN_OPPOSITE_ANGLE;"), leaf.index("bullets_add_regular();", leaf.index("bullet_template.angle += EXF_FAN_OPPOSITE_ANGLE;")))
        self.assertIn("bullet_template.angle += EXF_FAN_ROTATION_STEP;", leaf)

    def test_hp_loss_scales_bullet_speed_and_orbit_radius(self):
        hp_total = 3400
        min_speed_px = 2.5
        speed_scale_subpixels = value("EXF_FAN_HP_SPEED_SCALE")
        radius_scale_px = value("EXF_FAN_RADIUS_SCALE_PX")

        def bullet_speed_subpixels(hp):
            return ((hp_total - hp) * speed_scale_subpixels // hp_total) + round(min_speed_px * 16)

        def orbit_radius_subpixels(hp):
            return ((hp_total - hp) * radius_scale_px * 16) // hp_total

        self.assertEqual((speed_scale_subpixels, radius_scale_px), (64, 64))
        self.assertEqual((bullet_speed_subpixels(3400), bullet_speed_subpixels(1700), bullet_speed_subpixels(0)), (40, 72, 104))
        self.assertEqual((orbit_radius_subpixels(3400), orbit_radius_subpixels(1700), orbit_radius_subpixels(0)), (0, 512, 1024))

        leaf = LEAF[LEAF.index("void near exalice_pattern_final_fan(void)"):]
        self.assertIn("static_cast<unsigned long>(EXALICE_HP_WAVE4_REGULAR_END - boss.hp)", leaf)
        self.assertIn("EXF_FAN_HP_SPEED_SCALE", leaf)
        self.assertIn("EXF_FAN_RADIUS_SCALE_PX", leaf)
        self.assertIn("boss.pos.cur.x.v = polar(to_sp(EXF_FAN_CENTER_X_PX)", leaf)
        position = leaf.index("boss.pos.cur.x.v = polar")
        radius_write = leaf.index("boss.pos.velocity.x.v =", position)
        self.assertLess(position, radius_write)
        self.assertIn("final_fan_angle += EXF_FAN_ANGLE_STEP;", leaf)

    def test_frame_5000_still_checks_hp_but_5001_skips_and_explodes(self):
        for source in (UPDATE, FULL):
            case = final_case(source)
            self.assertLess(case.index("exalice_pattern_final_fan();"), case.index("if(boss.phase_frame <= EXALICE_FINAL_FAN_TIMEOUT_FRAME)"))
            self.assertLess(case.index("if(boss.phase_frame <= EXALICE_FINAL_FAN_TIMEOUT_FRAME)"), case.index("boss.phase_state.defeat_bonus = true;"))
            self.assertLess(case.index("boss.phase_state.defeat_bonus = true;"), case.index("boss_explode_small(ET_VERTICAL);"))
            self.assertIn("bullet_zap_drop_point_items = false;", case)
            self.assertIn("boss_custombullets_render = nullfunc_near;", case)

        self.assertTrue(5000 <= enum_value("EXALICE_FINAL_FAN_TIMEOUT_FRAME"))
        self.assertFalse(5001 <= enum_value("EXALICE_FINAL_FAN_TIMEOUT_FRAME"))
        # Final phase entry clears the byte-21 patterns_seen/defeat_bonus alias.
        self.assertIn("boss.phase_state.patterns_seen = EXALICE_NEW_PHASE_PATTERN_COUNT;", (ROOT / "src/main/boss/exalice/phase.cpp").read_text())
        self.assertIn("bullet_zap.active = boss.phase_state.defeat_bonus;", GENERIC)
        self.assertIn("if(boss.phase_state.defeat_bonus) { boss_score_bonus(bonus_units); }", GENERIC)

    def test_terminal_leaf_motion_and_shared_tail_run_before_generic_defeat(self):
        leaf = LEAF[LEAF.index("void near exalice_pattern_final_fan(void)"):]
        self.assertLess(leaf.index("if(boss.phase_frame >= EXF_FAN_FIRE_START)"), leaf.index("boss.pos.cur.x.v = polar"))
        self.assertLess(leaf.index("boss.pos.cur.x.v = polar"), leaf.index("final_fan_angle += EXF_FAN_ANGLE_STEP;"))
        case = final_case(UPDATE)
        self.assertLess(case.index("boss_explode_small(ET_VERTICAL);"), case.index("bullet_zap_drop_point_items = false;"))
        tail = UPDATE[UPDATE.index("cheetos_update();"):]
        self.assertIn("firewaves_update();", tail)
        self.assertIn("hud_hp_update_and_render(boss.hp, EXALICE_HP_INITIAL);", tail)
        self.assertIn("boss_defeat_update(EXALICE_FINAL_DEFEAT_BONUS);", UPDATE)


if __name__ == "__main__":
    unittest.main()
