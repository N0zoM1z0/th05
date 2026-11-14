"""Cross-phase ownership of Yumeko's original 16-byte Boss scratch arena."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOSS = ROOT / "src/main/boss/yumeko"
SCRATCH = (BOSS / "final_ring_scratch.hpp").read_text()
SETUP = (ROOT / "src/main/stage/setup.cpp").read_text()
AIMED = (BOSS / "aimed_swords.inl").read_text()
LASER = (BOSS / "laser_swords.cpp").read_text()
LASER_TIMING = (BOSS / "laser_swords_timing.hpp").read_text()
SPREADS = (BOSS / "spreads.cpp").read_text()
SWEEP = (BOSS / "sweep.cpp").read_text()
PATTERNS = (BOSS / "patterns.cpp").read_text()
UPDATE = (BOSS / "update.cpp").read_text()


class YumekoScratchLifetimeTests(unittest.TestCase):
    def test_every_phase_view_is_the_same_sixteen_byte_boss_storage(self):
        self.assertIn("union YumekoBossScratch", SCRATCH)
        views = (
            ("YumekoStage5SetupScratch", "stage5_setup", "yumeko_stage5_view_at_zero"),
            ("YumekoAimedSwordsScratch", "aimed_swords", "yumeko_aimed_view_at_zero"),
            ("YumekoLaserSwordsScratch", "laser_swords", "yumeko_laser_view_at_zero"),
            ("YumekoSpreadScratch", "spreads", "yumeko_spread_view_at_zero"),
            ("YumekoSweepScratch", "sweep", "yumeko_sweep_view_at_zero"),
            ("YumekoFinalRingScratch", "final_ring", "yumeko_final_view_at_zero"),
            ("YumekoPatternScratch", "pattern", "yumeko_pattern_view_at_zero"),
        )
        for type_name, view, assertion in views:
            self.assertIn(f"{type_name} {view};", SCRATCH)
            self.assertIn(assertion, SCRATCH)
        for assertion in (
            "yumeko_stage5_scratch_is_16", "yumeko_aimed_scratch_is_16",
            "yumeko_laser_scratch_is_16", "yumeko_spread_scratch_is_16",
            "yumeko_sweep_scratch_is_16", "yumeko_final_scratch_is_16",
            "yumeko_pattern_scratch_is_16", "yumeko_boss_scratch_is_16",
        ):
            self.assertIn(assertion, SCRATCH)

    def test_stage_five_seeds_the_two_attack_intervals_before_yumeko_runs(self):
        start = SETUP.index("void pascal near stage5_setup(void)")
        end = SETUP.index("void pascal near stage6_setup(void)", start)
        stage5 = SETUP[start:end]
        self.assertIn("yumeko_boss_scratch.stage5_setup.sword_spawn_interval = select_for_rank(", stage5)
        self.assertIn("yumeko_boss_scratch.stage5_setup.laser_spawn_interval = select_for_rank(", stage5)
        self.assertNotRegex(stage5, r"boss_statebyte\s*\[\s*[01]\s*\]")

        for name, value in (
            ("STAGE5_RANK_BASE_EASY", 20),
            ("STAGE5_RANK_BASE_NORMAL", 10),
            ("STAGE5_RANK_BASE_HARD", 6),
            ("STAGE5_RANK_BASE_LUNATIC", 6),
            ("STAGE5_RANK_REPEAT_EASY", 48),
            ("STAGE5_RANK_REPEAT_NORMAL", 32),
            ("STAGE5_RANK_REPEAT_HARD", 24),
            ("STAGE5_RANK_REPEAT_LUNATIC", 24),
        ):
            self.assertRegex(SETUP, rf"{name}\s*=\s*{value}\s*;")

    def test_aimed_and_laser_attacks_consume_distinct_seeded_clocks(self):
        self.assertIn("#define yumeko_sword_interval yumeko_boss_scratch.aimed_swords.sword_spawn_interval", (BOSS / "aimed_swords.cpp").read_text())
        self.assertIn("(boss.phase_frame % yumeko_sword_interval) == 0", AIMED)
        self.assertIn("boss.hp - boss.phase_end_hp < 600", AIMED)
        self.assertIn("yumeko_sword_interval = select_for_rank(16, 8, 4, 4);", AIMED)
        self.assertIn("yumeko_volley_frames = select_for_rank(40, 48, 52, 52);", AIMED)

        self.assertIn("#define yumeko_laser_interval yumeko_boss_scratch.laser_swords.laser_spawn_interval", LASER)
        self.assertIn("(boss.phase_frame % yumeko_laser_interval) == 0", LASER)
        self.assertIn("YLS_NEAR_HP_GATE 500", LASER_TIMING)
        self.assertIn("YLS_LASER_EASY 34", LASER_TIMING)
        self.assertIn("YLS_LASER_NORMAL 28", LASER_TIMING)
        self.assertIn("YLS_LASER_HARD 20", LASER_TIMING)
        self.assertIn("YLS_LASER_LUNATIC 20", LASER_TIMING)
        self.assertIn("yumeko_laser_interval = select_for_rank(YLS_LASER_EASY, YLS_LASER_NORMAL, YLS_LASER_HARD, YLS_LASER_LUNATIC);", LASER)
        self.assertIn("yumeko_volley_frames = select_for_rank(YLS_VOLLEY_EASY, YLS_VOLLEY_NORMAL, YLS_VOLLEY_HARD, YLS_VOLLEY_LUNATIC);", LASER)

    def test_tail_bytes_are_named_by_their_sequential_attack_lifetimes(self):
        for field in (
            "aimed_swords_accelerated", "laser_swords_accelerated", "sweep_round",
            "paired_angle_b", "sweep_side", "final_ring_angle",
            "sword_pattern_angle_a", "fan_mirrored_side", "sweep_spacing",
            "final_ring_count",
        ):
            self.assertIn(field, SCRATCH)

        self.assertIn("#define yumeko_sweep_round yumeko_boss_scratch.sweep.pattern_byte13.sweep_round", SWEEP)
        self.assertIn("#define yumeko_sweep_side yumeko_boss_scratch.sweep.pattern_byte14.sweep_side", SWEEP)
        self.assertIn("#define yumeko_sweep_spacing yumeko_boss_scratch.sweep.pattern_byte15.sweep_spacing", SWEEP)
        self.assertIn("yumeko_boss_scratch.spreads.pattern_byte14.paired_angle_b", SPREADS)
        self.assertIn("#define yumeko_fan_mirrored yumeko_pattern_scratch.pattern_byte15.fan_mirrored_side", PATTERNS)
        self.assertIn("#define yumeko_pattern_scratch yumeko_boss_scratch.pattern", SCRATCH)
        self.assertIn("yumeko_final_scratch.pattern_byte14.final_ring_angle", UPDATE)
        self.assertIn("yumeko_final_scratch.pattern_byte15.final_ring_count", UPDATE)

    def test_yumeko_sources_no_longer_index_the_shared_scratch_array_directly(self):
        for path in BOSS.rglob("*"):
            if path.suffix not in {".cpp", ".hpp", ".h", ".inl"}:
                continue
            source = path.read_text()
            source = re.sub(r"//[^\n]*|/\*.*?\*/", "", source, flags=re.DOTALL)
            self.assertIsNone(
                re.search(r"boss_statebyte\s*\[", source),
                f"raw Boss scratch index remains in {path.relative_to(ROOT)}",
            )


if __name__ == "__main__":
    unittest.main()
