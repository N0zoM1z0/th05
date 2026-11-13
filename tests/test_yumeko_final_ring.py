"""Frame-accurate Yumeko final-ring and major-controller handoff model."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE = (ROOT / "src/main/boss/yumeko/update.cpp").read_text()
TIMING = (ROOT / "src/main/boss/yumeko/phase_timing.hpp").read_text()
SCRATCH = (ROOT / "src/main/boss/yumeko/final_ring_scratch.hpp").read_text()
MOVEMENT = (ROOT / "src/main/boss/movement.hpp").read_text()
GENERIC = (ROOT / "src/main/boss/generic.hpp").read_text()


def enum_values(source, enum_name):
    match = re.search(rf"enum\s+{enum_name}\s*\{{(.*?)\}};", source, re.S)
    if not match:
        raise AssertionError(f"enum {enum_name} is missing")
    values = {}
    for name, expression in re.findall(r"\b([A-Z][A-Z0-9_]+)\s*=\s*([^,]+)", match.group(1)):
        expression = expression.strip()
        if re.fullmatch(r"(?:0[xX][0-9A-Fa-f]+|[0-9]+)", expression):
            values[name] = int(expression, 0)
    return values


def phase_block(name, next_marker):
    start = UPDATE.index(f"case {name}:")
    end = UPDATE.index(next_marker, start)
    return UPDATE[start:end]


class YumekoFinalRingTests(unittest.TestCase):
    def test_final_ring_fires_74_volleys_including_the_timeout_frame(self):
        values = enum_values(TIMING, "YumekoPhaseClocks")
        first = values["YUMEKO_FINAL_RING_FIRST_VOLLEY_FRAME"]
        timeout = values["YUMEKO_FINAL_RING_TIMEOUT_FRAMES"]
        interval = values["YUMEKO_FINAL_RING_INTERVAL_FRAMES"]
        frames = list(range(first, timeout + 1, interval))
        self.assertEqual((first, timeout, interval), (32, 1200, 16))
        self.assertEqual(len(frames), 74)
        self.assertEqual((frames[0], frames[-1]), (32, 1200))
        count_expression = re.search(
            r"YUMEKO_FINAL_RING_VOLLEY_COUNT\s*=\s*([^,]+)", TIMING, re.S
        ).group(1)
        self.assertEqual(
            re.sub(r"\s+", "", count_expression),
            "((YUMEKO_FINAL_RING_TIMEOUT_FRAMES-YUMEKO_FINAL_RING_FIRST_VOLLEY_FRAME)/YUMEKO_FINAL_RING_INTERVAL_FRAMES)+1",
        )
        self.assertEqual(len(frames), 74)

        helper_start = UPDATE.index("void near yumeko_pattern_final_ring(void)")
        helper_end = UPDATE.index("// The stationary sword/laser waves", helper_start)
        helper = UPDATE[helper_start:helper_end]
        self.assertIn("if(boss.phase_frame < YUMEKO_FINAL_RING_FIRST_VOLLEY_FRAME)", helper)
        self.assertIn("if((boss.phase_frame % YUMEKO_FINAL_RING_INTERVAL_FRAMES) == 0)", helper)

        final = phase_block("YUMEKO_PHASE_FINAL_RING", "default:")
        self.assertLess(final.index("yumeko_pattern_final_ring();"), final.index("if(boss.phase_frame < YUMEKO_FINAL_RING_TIMEOUT_FRAMES)"))
        self.assertLess(final.index("if(boss.phase_frame < YUMEKO_FINAL_RING_TIMEOUT_FRAMES)"), final.index("boss.phase_state.defeat_bonus = true;"))

    def test_alternating_turns_reflect_every_other_angle_without_changing_the_counter(self):
        values = enum_values(TIMING, "YumekoPhaseClocks")
        effects = enum_values(TIMING, "YumekoFightEffects")
        count = (
            (values["YUMEKO_FINAL_RING_TIMEOUT_FRAMES"] - values["YUMEKO_FINAL_RING_FIRST_VOLLEY_FRAME"])
            // values["YUMEKO_FINAL_RING_INTERVAL_FRAMES"] + 1
        )
        reflect = values["YUMEKO_FINAL_RING_REFLECT_ANGLE"]
        turn = values["YUMEKO_FINAL_RING_TURN_ANGLE"]
        angle = 0
        emitted = []
        for ring_count in range(count):
            odd = bool(ring_count & 1)
            emitted.append((reflect - angle if odd else angle, turn if odd else -turn))
            angle = (angle + 1) & 0xFF

        self.assertEqual(count, 74)
        self.assertEqual(emitted[:2], [(0, -0x40), (0x7F, 0x40)])
        self.assertEqual(emitted[-1], (0x37, 0x40))
        self.assertEqual(sum(turn_by < 0 for _, turn_by in emitted), 37)
        self.assertEqual(sum(turn_by > 0 for _, turn_by in emitted), 37)
        self.assertEqual(angle, 74)
        self.assertEqual(effects["YUMEKO_FINAL_RING_BULLET_COUNT"], 18)

        helper_start = UPDATE.index("void near yumeko_pattern_final_ring(void)")
        helper_end = UPDATE.index("// The stationary sword/laser waves", helper_start)
        helper = UPDATE[helper_start:helper_end]
        self.assertIn("bullet_special.turns_max = YSW_FINAL_TURNS_MAX;", helper)
        self.assertIn("bullet_template_special_angle.turn_by = YUMEKO_FINAL_RING_TURN_ANGLE;", helper)
        self.assertIn("bullet_template.angle = YUMEKO_FINAL_RING_REFLECT_ANGLE - bullet_template.angle;", helper)
        self.assertIn("bullet_template_special_angle.turn_by = -YUMEKO_FINAL_RING_TURN_ANGLE;", helper)
        self.assertLess(helper.index("bullets_add_special_fixedspeed();"), helper.index("yumeko_final_angle++;"))
        self.assertLess(helper.index("yumeko_final_angle++;"), helper.index("yumeko_final_rings++;"))

    def test_final_approach_clears_the_shared_defeat_bonus_byte(self):
        self.assertIn("unsigned char patterns_seen;\n        bool defeat_bonus;", MOVEMENT)
        self.assertIn("th05_boss_phase_state_at_21", MOVEMENT)
        self.assertIn("unsigned char final_ring_count;", SCRATCH)
        self.assertIn("yumeko_final_rings_at_15", SCRATCH)

        approach = phase_block("YUMEKO_PHASE_FINAL_APPROACH", "case YUMEKO_PHASE_FINAL_RING:")
        self.assertIn("YUMEKO_ADVANCE_PHASE_CLOCK();", approach)
        self.assertIn("boss.phase_state.patterns_seen = 0;", approach)

        final = phase_block("YUMEKO_PHASE_FINAL_RING", "default:")
        self.assertIn("boss.phase_state.defeat_bonus = true;", final)
        self.assertIn("if(!boss_hittest_shots())", final)
        self.assertIn("boss_explode_small(ET_VERTICAL);", final)
        self.assertIn("boss_custombullets_render = nullfunc_near;", final)
        self.assertIn("bullet_zap.active = boss.phase_state.defeat_bonus;", GENERIC)

        # At frame 1199 an HP hit can set the reward bit; frame 1200 bypasses
        # the hit test entirely, so the final-approach zero survives.
        def reward_after_final_tick(frame, hp_hit):
            reward = 0  # final approach reset the byte-21 alias
            if frame < 1200 and hp_hit:
                reward = 1
            return reward

        self.assertEqual(reward_after_final_tick(1199, True), 1)
        self.assertEqual(reward_after_final_tick(1200, True), 0)
        self.assertEqual(reward_after_final_tick(1200, False), 0)

    def test_final_explosion_entry_runs_the_shared_tail_once_but_defeat_phase_returns_early(self):
        final = phase_block("YUMEKO_PHASE_FINAL_RING", "default:")
        self.assertLess(final.index("boss_explode_small(ET_VERTICAL);"), final.index("boss.phase_frame = 0;"))
        self.assertLess(final.index("boss.phase_frame = 0;"), final.index("boss.phase = PHASE_BOSS_EXPLODE_SMALL;"))
        self.assertLess(final.index("boss.phase = PHASE_BOSS_EXPLODE_SMALL;"), final.index("boss_custombullets_render = nullfunc_near;"))
        default = UPDATE[UPDATE.index("default:", UPDATE.index("case YUMEKO_PHASE_FINAL_RING:")):]
        self.assertIn("boss_defeat_update(YUMEKO_DEFEAT_BONUS);", default)
        self.assertIn("return;", default)
        self.assertGreater(UPDATE.index("swords_update();"), UPDATE.index("switch(boss.phase)"))
        self.assertIn("hud_hp_update_and_render(boss.hp, YUMEKO_HP_TOTAL);", UPDATE)
        self.assertIn("YUMEKO_DEFEAT_BONUS = 65", TIMING)


if __name__ == "__main__":
    unittest.main()
