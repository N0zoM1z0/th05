// Default rectangle that boss_flystep_random() keeps the boss inside.
#pragma option -zCBOSS_DEFAULT_CLAMP_TEXT -zPmain_01
#include "src/main/boss/movement.hpp"
#pragma codeseg BOSS_DEFAULT_CLAMP_TEXT main_01

// Playfield pixels. EX-Alice later overwrites this object with her own,
// narrower arena of [64,320]x[48,96].
enum BossDefaultClampPixels {
    BOSS_DEFAULT_LEFT_PX = 32,
    BOSS_DEFAULT_RIGHT_PX = 352,
    BOSS_DEFAULT_TOP_PX = 24,
    BOSS_DEFAULT_BOTTOM_PX = 128,
    BOSS_SUBPIXEL_SHIFT = 4
};

LRTB<Subpixel, Subpixel> near boss_flystep_random_clamp = {
    { BOSS_DEFAULT_LEFT_PX << BOSS_SUBPIXEL_SHIFT },
    { BOSS_DEFAULT_RIGHT_PX << BOSS_SUBPIXEL_SHIFT },
    { BOSS_DEFAULT_TOP_PX << BOSS_SUBPIXEL_SHIFT },
    { BOSS_DEFAULT_BOTTOM_PX << BOSS_SUBPIXEL_SHIFT }
};

typedef char boss_default_clamp_is_eight[
    (sizeof(boss_flystep_random_clamp) == 8) ? 1 : -1];
