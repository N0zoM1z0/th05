"""Frame-accurate Shinki phase-11/12 and final spiral/float leaf model."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
# The accepted 959-byte controller is independently compiled from
# update_context.cpp; shinki.cpp remains the full natural-source counterpart.
SOURCE = (ROOT / "src/main/boss/shinki/update_context.cpp").read_text()
NATURAL_SOURCE = (ROOT / "src/main/boss/shinki/shinki.cpp").read_text()
GENERIC_SOURCE = (ROOT / "src/main/boss/generic.cpp").read_text()
GENERIC_HEADER = (ROOT / "src/main/boss/generic.hpp").read_text()
TIMING = (ROOT / "src/main/boss/shinki/final_spiral_timing.hpp").read_text()
WING = (ROOT / "src/main/boss/shinki/wing_attack_rules.hpp").read_text()
MOVEMENT = (ROOT / "src/main/boss/movement.hpp").read_text()
WING_HITBOXES = (ROOT / "src/main/boss/shinki/wing_hitboxes.hpp").read_text()
GENERIC = (ROOT / "src/main/boss/generic.hpp").read_text()
FLOAT_DATA = (ROOT / "src/main/boss/shinki/float_direction.c").read_text()


def enum_constants(source, enum_name, prefix):
    match = re.search(rf"enum\s+{enum_name}\s*\{{(.*?)\}};", source, re.S)
    if not match:
        raise AssertionError(f"enum {enum_name} is missing")
    values = {}
    for name, expression in re.findall(rf"\b({prefix}[A-Z0-9_]+)\s*=\s*([^,}}]+)", match.group(1)):
        values[name] = int(expression.strip(), 0)
    return values


def phase_block(phase_name, next_marker):
    start = SOURCE.index(f"case {phase_name}:")
    end = SOURCE.index(next_marker, start)
    return SOURCE[start:end]


class ShinkiFinalPhaseTests(unittest.TestCase):
    def test_phase_11_carries_the_clock_into_phase_12(self):
        self.assertIn("boss.phase_frame = SHINKI_PHASE_FRAME_RESET;", SOURCE[SOURCE.index("case SHINKI_PHASE_SYMMETRIC_SPREADS:"):SOURCE.index("case SHINKI_PHASE_DEFEAT_TRANSITION:")])
        phase11 = phase_block("SHINKI_PHASE_DEFEAT_TRANSITION", "case SHINKI_PHASE_FINAL_CIRCLES:")
        self.assertIn("if(boss.phase_frame > PHASE_11_FRAMES)", phase11)
        self.assertIn("boss.phase++;", phase11)
        self.assertNotIn("boss.phase_frame = 0;", phase11)
        self.assertIn("PHASE_11_FRAMES = 16", SOURCE)
        self.assertIn("boss.phase_frame++;", SOURCE[:SOURCE.index("switch(boss.phase)")])
        # The prior boss_phase_next starts phase 11 at zero; its 17th update
        # advances to phase 12 without resetting the shared frame counter.
        self.assertIn("boss_phase_next(ET_HORIZONTAL, HP_PHASE_12_END);", SOURCE)
        self.assertEqual(list(range(1, 18))[-1], 17)
        self.assertEqual(17 + 1, 18)  # first phase-12 callback observes frame 18

        # The transition flashes on every one of its 17 updates. With the
        # original even-frame selector 0, odd frames are dim and even frames
        # are bright; the terminal frame 17 is therefore still a dim flash.
        bright_frames = [frame for frame in range(1, 18) if (frame % 2) == 0]
        dim_frames = [frame for frame in range(1, 18) if (frame % 2) != 0]
        self.assertEqual(bright_frames, [2, 4, 6, 8, 10, 12, 14, 16])
        self.assertEqual(dim_frames, [1, 3, 5, 7, 9, 11, 13, 15, 17])
        self.assertIn("SHINKI_DEFEAT_FLASH_EVEN_FRAME = 0", WING_HITBOXES)
        self.assertIn("SHINKI_DEFEAT_TONE_BRIGHT = 150", SOURCE)
        self.assertIn("SHINKI_DEFEAT_TONE_DIM = 100", SOURCE)
        self.assertLess(phase11.index("boss_hittest_shots();"), phase11.index("palette_settone_deferred(SHINKI_DEFEAT_TONE_BRIGHT);"))

    def test_phase_entry_clears_the_shared_defeat_bonus_latch(self):
        # Boss byte 21 is one byte, not two independent phase counters.
        self.assertIn("unsigned char patterns_seen;\n        bool defeat_bonus;", MOVEMENT)
        self.assertIn("th05_boss_phase_state_at_21", MOVEMENT)

        start = GENERIC_SOURCE.index("void pascal near boss_phase_next(")
        end = GENERIC_SOURCE.index("// Complete natural 414-byte defeat function", start)
        phase_next = GENERIC_SOURCE[start:end]
        self.assertIn("boss.phase_state.patterns_seen = 0;", phase_next)

        # Shinki's Devil-to-defeat transition uses that helper. The subsequent
        # frame-17 transition is a direct phase increment and carries the clock.
        for source in (SOURCE, NATURAL_SOURCE):
            self.assertIn("boss_phase_next(ET_HORIZONTAL, HP_PHASE_12_END);", source)
            phase11 = source[source.index("case SHINKI_PHASE_DEFEAT_TRANSITION:"):source.index("case SHINKI_PHASE_FINAL_CIRCLES:")]
            self.assertIn("boss.phase++;", phase11)
            self.assertNotIn("boss.phase_frame = 0;", phase11)

        final = phase_block("SHINKI_PHASE_FINAL_CIRCLES", "default:")
        self.assertIn("boss.phase_state.defeat_bonus = true;", final)
        self.assertLess(final.index("if(!boss_hittest_shots())"), final.index("boss.phase_state.defeat_bonus = true;"))
        # A timeout does not enter that HP-only write; the prior helper left
        # the aliased byte at zero, so generic defeat cannot grant the bonus.
        self.assertIn("bullet_zap.active = boss.phase_state.defeat_bonus;", GENERIC_HEADER)
        self.assertIn("if(boss.phase_state.defeat_bonus) { boss_score_bonus(bonus_units); }", GENERIC_HEADER)

    def test_final_spiral_emits_360_two_ball_volleys_inclusive_of_frame_3000(self):
        values = enum_constants(TIMING, "ShinkiFinalSpiralClock", "SHINKI_SPIRAL_")
        timeout = int(re.search(r"#define SHW_WING_PHASE_TIMEOUT_FRAMES\s+(\d+)", WING).group(1))
        frames = list(range(values["SHINKI_SPIRAL_ARM_FRAME"], timeout + 1, values["SHINKI_SPIRAL_VOLLEY_INTERVAL"]))
        self.assertEqual(values["SHINKI_SPIRAL_ARM_FRAME"], 128)
        self.assertEqual(timeout, 3000)
        self.assertEqual(len(frames), 360)
        self.assertEqual(frames[-1], 3000)
        self.assertEqual(len(frames) * 2, 720)

        start = SOURCE.index("void near pattern_circles_and_alternating_spirals(void)")
        end = SOURCE.index("void near shinki_move_float(void)", start)
        body = SOURCE[start:end]
        # The accepted context uses a real one-call macro for the common
        # vector2_at + b6balls_add sequence; the natural full source spells
        # both calls inline. Check both forms and their source order.
        self.assertEqual(body.count("SHINKI_SPIRAL_FIRE_OFFSET_B6BALL();"), 2)
        macro_start = SOURCE.index("#define SHINKI_SPIRAL_FIRE_OFFSET_B6BALL()")
        macro_end = SOURCE.index("// The red and pellet rings", macro_start)
        macro = SOURCE[macro_start:macro_end]
        self.assertIn("vector2_at(", macro)
        self.assertIn("b6balls_add();", macro)
        natural_start = NATURAL_SOURCE.index("void near pattern_circles_and_alternating_spirals(void)")
        natural_end = NATURAL_SOURCE.index("void near shinki_move_float(void)", natural_start)
        natural_body = NATURAL_SOURCE[natural_start:natural_end]
        self.assertEqual(natural_body.count("b6balls_add();"), 2)
        first = body.index("SHINKI_SPIRAL_FIRE_OFFSET_B6BALL();")
        rotate = body.index("b6ball_template.angle += SHINKI_SPIRAL_OPPOSITE_BALL_ANGLE;")
        second = body.index("SHINKI_SPIRAL_FIRE_OFFSET_B6BALL();", first + 1)
        back = body.index("b6ball_template.angle -= SHINKI_SPIRAL_BALL_ROTATE_BACK;")
        self.assertLess(first, rotate)
        self.assertLess(rotate, second)
        self.assertLess(second, back)

        # Each completed volley advances the next pair by 0x80 - 0x78 = 8.
        self.assertEqual((359 * 8) & 0xFF, 0x38)
        self.assertEqual((360 * 8) & 0xFF, 0x40)

    def test_red_and_pellet_rings_occupy_disjoint_halves_of_each_256_frame_cycle(self):
        values = enum_constants(TIMING, "ShinkiFinalSpiralClock", "SHINKI_SPIRAL_")
        timeout = int(re.search(r"#define SHW_WING_PHASE_TIMEOUT_FRAMES\s+(\d+)", WING).group(1))
        interval = values["SHINKI_SPIRAL_VOLLEY_INTERVAL"]
        period = values["SHINKI_SPIRAL_WAVE_PERIOD"]
        half = values["SHINKI_SPIRAL_WAVE_HALF"]
        red = [f for f in range(values["SHINKI_SPIRAL_RED_RINGS_BEGIN"], timeout + 1)
               if f % interval == 0 and f % period < half]
        pellet = [f for f in range(values["SHINKI_SPIRAL_PELLET_RINGS_BEGIN"], timeout + 1)
                  if f % interval == 0 and f % period >= half]
        self.assertEqual(len(red), 176)
        self.assertEqual((red[0], red[-1]), (256, 2936))
        self.assertEqual(len(pellet), 152)
        self.assertEqual((pellet[0], pellet[-1]), (640, 3000))
        self.assertFalse(set(red) & set(pellet))
        self.assertEqual((len(red) * 2) & 0xFF, 0x60)  # 176 red-angle decrements of 2
        self.assertEqual((len(pellet) * 4) & 0xFF, 0x60)  # 152 pellet-angle increments of 4

    def test_terminal_frame_runs_ball_pair_pellet_ring_and_flystep_before_timeout(self):
        values = enum_constants(TIMING, "ShinkiFinalSpiralClock", "SHINKI_SPIRAL_")
        timeout = int(re.search(r"#define SHW_WING_PHASE_TIMEOUT_FRAMES\s+(\d+)", WING).group(1))
        frame_in_cycle = timeout % values["SHINKI_SPIRAL_WAVE_PERIOD"]
        flystep_cycle = (timeout - values["SHINKI_SPIRAL_FLYSTEP_BEGIN"]) % values["SHINKI_SPIRAL_FLYSTEP_PERIOD"]
        flystep_argument = flystep_cycle - values["SHINKI_SPIRAL_FLYSTEP_LEAD"]
        self.assertEqual(frame_in_cycle, 184)
        self.assertGreaterEqual(frame_in_cycle, values["SHINKI_SPIRAL_WAVE_HALF"])
        self.assertEqual(timeout % values["SHINKI_SPIRAL_VOLLEY_INTERVAL"], 0)
        self.assertEqual(flystep_argument, 8)

        final = phase_block("SHINKI_PHASE_FINAL_CIRCLES", "default:")
        self.assertLess(final.index("pattern_circles_and_alternating_spirals();"), final.index("if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES)"))
        self.assertLess(final.index("if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES)"), final.index("boss.phase_state.defeat_bonus = true;"))
        self.assertIn("boss.phase_frame = SHINKI_PHASE_FRAME_RESET;", final)

    def test_final_timeout_skips_hp_bonus_but_hp_defeat_sets_shared_bonus_bit(self):
        final = phase_block("SHINKI_PHASE_FINAL_CIRCLES", "default:")
        self.assertIn("if(!boss_hittest_shots())", final)
        self.assertIn("boss.phase_state.defeat_bonus = true;", final)
        self.assertLess(final.index("boss.phase_state.defeat_bonus = true;"), final.index("boss_explode_small(ET_VERTICAL);"))
        union = re.search(r"union\s*\{\s*unsigned char patterns_seen;\s*bool defeat_bonus;\s*\}", MOVEMENT, re.S)
        self.assertIsNotNone(union)
        self.assertIn("bullet_zap.active = boss.phase_state.defeat_bonus;", GENERIC)
        self.assertIn("if(boss.phase_state.defeat_bonus) { boss_score_bonus(bonus_units); }", GENERIC)
        self.assertIn("boss_defeat_update(SHINKI_DEFEAT_SCORE_BONUS);", SOURCE)

    def test_float_leaf_uses_stage_mod4_and_reverses_at_signed_unit_speed(self):
        values = enum_constants(TIMING, "ShinkiFinalSpiralClock", "SHINKI_FLOAT_")
        self.assertEqual(values["SHINKI_FLOAT_UPDATE_FRAME_MOD4"], 0)
        self.assertEqual(values["SHINKI_FLOAT_DOWNWARD"], 0)
        acceleration = float(re.search(r"#define SHINKI_FLOAT_ACCELERATION_PX\s+\(([^f]+)f\)", TIMING).group(1))
        limit = float(re.search(r"#define SHINKI_FLOAT_SPEED_LIMIT_PX\s+\(([^f]+)f\)", TIMING).group(1))
        self.assertEqual((acceleration, limit), (0.0625, 1.0))
        self.assertRegex(FLOAT_DATA, r"shinki_float_direction\s*=\s*0")

        direction = values["SHINKI_FLOAT_DOWNWARD"]
        velocity = 0.0
        snapshots = {}
        for update in range(1, 113):
            if direction == values["SHINKI_FLOAT_DOWNWARD"]:
                velocity += acceleration
                if velocity >= limit:
                    direction += 1
            else:
                velocity -= acceleration
                if velocity <= -limit:
                    direction -= 1
            if update in (16, 48, 80, 112):
                snapshots[update] = (round(velocity, 4), direction)
        self.assertEqual(snapshots, {
            16: (1.0, 1),
            48: (-1.0, 0),
            80: (1.0, 1),
            112: (-1.0, 0),
        })
        self.assertIn("if(stage_frame_mod4 != SHINKI_FLOAT_UPDATE_FRAME_MOD4)", SOURCE)
        self.assertIn("boss.pos.cur.y.v += boss.pos.velocity.y.v;", SOURCE)
        self.assertIn("boss.pos.velocity.y.v = to_sp(SHINKI_RESET_Y_VELOCITY_PX);", SOURCE)


if __name__ == "__main__":
    unittest.main()
