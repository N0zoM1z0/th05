// Complete Mima bomb phase/tone/scroll lifecycle.
#ifndef TH05_MIMA_BOMB_COMBINED
#pragma option -zCMIMA_BOMB_TEXT -zPmain_01
#endif
#include "src/main/hud/overlay.hpp"
extern unsigned char bomb_frame;
extern bool bombing;
extern bool scroll_active;
extern vram_y_t scroll_line;
extern unsigned char stage_id;
extern bool items_pull_to_player;
extern unsigned int PaletteTone;
extern bool palette_changed;
extern nearfunc_t_near bg_render_bombing;
extern nearfunc_t_near bg_render_bombing_func;
#pragma codeseg _TEXT
extern "C" void pascal far graph_scrollup(vram_y_t line);
#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int effect);
#pragma codeseg MIMA_BOMB_TEXT main_01
extern "C" void pascal near nullfunc_near(void);
void near mima_bomb_draw(void);
void near bomb_dream_decay(void);

#include "src/main/player/bomb_body/mima_control.inl"
