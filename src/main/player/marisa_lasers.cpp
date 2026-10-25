// Eight transient Marisa bomb beams, with layered PC-98 filled shapes.
#pragma option -zCMARISA_LASERS_TEXT -zPmain_01
#include <dos.h>
#include "src/main/player/bombanim.hpp"
#include "src/main/player/player.hpp"

extern unsigned int PaletteTone;
extern bool palette_changed;
#pragma codeseg _TEXT
extern "C" {
    void pascal far palette_show(void);
    void pascal far grcg_boxfill(int left, int top, int right, int bottom);
    void pascal far grcg_circlefill(int x, int y, unsigned int radius);
}
#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int effect);
#pragma codeseg MAIN_BOMB_SPARKS main_03
void far bomb_sparks_add_at_player(void);
#pragma codeseg MARISA_LASERS_TEXT main_01
void near grcg_setmode_rmw(void);
void near grcg_setcolor_direct_raw(void);
#include "src/main/player/bomb_body/marisa_lasers.inl"
