// Bomb animation state and the drawing routines the bombs use.
#ifndef TH05_CHARACTER_BOMB_DRAW_HPP
#define TH05_CHARACTER_BOMB_DRAW_HPP
#include "src/main/player/bombanim.hpp"

extern unsigned int PaletteTone;
extern bool palette_changed;
extern unsigned char circles_color;
extern unsigned char stage_frame_mod4;

// Implemented elsewhere in main_01.
void near reimu_bomb_backdrop_render(void);
void near yuuka_bomb_backdrop_render(void);
void near yuuka_heart_update_and_render(void);

#pragma codeseg _TEXT
extern "C" void pascal far palette_show(void);
#pragma codeseg SHARED
extern "C" {
    void pascal far cdg_put_noalpha_8(int left, int top, int slot);
    void pascal far snd_se_play(int effect);
}
#endif
