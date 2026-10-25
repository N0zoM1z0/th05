// Reimu's complete backdrop, star animation and deferred palette ramp callback.
#pragma option -zCREIMU_DRAW_TEXT -zPmain_01
#include "src/main/player/bomb_draw.hpp"
#pragma codeseg REIMU_DRAW_TEXT main_01

void near reimu_bomb_draw(void)
{
    cdg_put_noalpha_8(80, 16, 0);
    reimu_bomb_backdrop_render();
    reimu_stars_update_and_render();
    circles_color = 9;
    if(bomb_frame <= 64) {
        PaletteTone = 196 - ((bomb_frame - 32) * 3);
        palette_changed = true;
        return;
    }
    if(bomb_frame <= 112 && stage_frame_mod4 == 0) {
        snd_se_play(9);
    }
}
