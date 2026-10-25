// Yuuka's complete backdrop, heart animation and immediate flashing callback.
#pragma option -zCYUUKA_DRAW_TEXT -zPmain_01
#include "src/main/player/bomb_draw.hpp"
#pragma codeseg YUUKA_DRAW_TEXT main_01

void near yuuka_bomb_draw(void)
{
    cdg_put_noalpha_8(96, 16, 0);
    yuuka_bomb_backdrop_render();
    yuuka_heart_update_and_render();
    circles_color = 9;
    if(bomb_frame <= 64) {
        PaletteTone = 196 - ((bomb_frame - 32) * 3);
        palette_changed = true;
        return;
    }
    if(bomb_frame % 4 == 0) {
        snd_se_play(9);
        PaletteTone = 150;
    } else if(bomb_frame % 4 == 2) {
        PaletteTone = 100;
    } else {
        return;
    }
    palette_show();
}
