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

#include "src/main/player/bomb_body/marisa_draw.inl"
