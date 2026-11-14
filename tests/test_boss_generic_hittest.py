"""Generic Boss/Midboss hit-test leaves retain their original code shape."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "src/main/boss/generic.cpp").read_text()
HEADER = (ROOT / "src/main/boss/generic.hpp").read_text()


class BossGenericHittestTests(unittest.TestCase):
    def test_boss_uses_the_shared_inline_hitbox_helper(self):
        start = SOURCE.index("int pascal near boss_hittest_shots_damage(")
        end = SOURCE.index("// Probably only here", start)
        body = SOURCE[start:end]
        self.assertIn("shots_hittest_against_boss = true;", body)
        self.assertIn("int ret = shots_hittest(boss.pos.cur, radius_x, radius_y);", body)
        self.assertIn("shots_hittest_against_boss = false;", body)
        self.assertIn("inline int shots_hittest(const PlayfieldPoint &center,", HEADER)

    def test_midboss_retains_scalar_hitbox_stores_for_the_352_byte_unit(self):
        start = SOURCE.index("int pascal near midboss_hittest_shots_damage(")
        end = SOURCE.index("bool near boss_hittest_shots(void)", start)
        body = SOURCE[start:end]
        stores = [
            "shots_hittest_against_boss = true;",
            "shot_hitbox_radius.x.v = radius_x;",
            "shot_hitbox_radius.y.v = radius_y;",
            "shot_hitbox_center.x.v = midboss.pos.cur.x.v;",
            "shot_hitbox_center.y.v = midboss.pos.cur.y.v;",
            "int ret = shots_hittest();",
            "shots_hittest_against_boss = false;",
        ]
        positions = [body.index(store) for store in stores]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("shots_hittest(midboss.pos.cur, radius_x, radius_y)", body)
        self.assertIn("inline center/radius helper emits 4 fewer", body)


if __name__ == "__main__":
    unittest.main()
