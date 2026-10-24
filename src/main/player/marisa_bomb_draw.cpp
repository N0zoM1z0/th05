// Complete Marisa bomb backdrop, entrance tone and beam dispatch.
#pragma option -zCMARISA_DRAW_TEXT -zPmain_01
#include "src/main/player/bombanim.hpp"
extern unsigned int PaletteTone;
extern bool palette_changed;
extern unsigned char shot_time;
static const unsigned char SHOT_BLOCKED_FOR_THIS_FRAME = 0xFF;
#pragma codeseg SHARED
extern "C" void pascal far cdg_put_noalpha_8(int left, int top, int slot);
#pragma codeseg MARISA_DRAW_TEXT main_01
void near marisa_bomb_backdrop_render(void);
void near marisa_lasers_update_and_render(void);

void near marisa_bomb_draw(void)
{
    cdg_put_noalpha_8(112, 16, 0);
    marisa_bomb_backdrop_render();
    if(bomb_frame < 16) {
        PaletteTone = 196 - (bomb_frame * 6);
        palette_changed = true;
    } else {
        marisa_lasers_update_and_render();
        shot_time = SHOT_BLOCKED_FOR_THIS_FRAME;
    }
}
