// Natural maintained TH04 src/main/hud/hud.cpp HP drawer, genuine TH05 APIs.
#pragma option -G -zCHUD_HP_DRAW_TEXT -zPmain_01
#include "src/main/hud/hp_draw.hpp"

void pascal far hud_hp_put(int bar_value)
{
    const hud_bar9_t blank = gHUD_HP_BLANK;
    const hud_colors5_t colors = HUD_HP_COLORS;
    if(bar_value != 0) {
        gaiji_putsa(61, 8, reinterpret_cast<const char far *>(gsENEMY),
            HUD_HP_DRAW_YELLOW);
        hud_bar_put(9, bar_value, colors.v[bar_value / 32]);
    } else {
        gaiji_putsa(61, 8, reinterpret_cast<const char far *>(&blank.v[5]),
            HUD_HP_DRAW_WHITE);
        gaiji_putsa(56, 9, reinterpret_cast<const char far *>(blank.v),
            HUD_HP_DRAW_WHITE);
    }
}
