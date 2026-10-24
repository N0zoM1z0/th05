// Complete Marisa bomb phase/tone/scroll lifecycle.
#pragma option -zCMARISA_BOMB_TEXT -zPmain_01
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
#pragma codeseg MARISA_BOMB_TEXT main_01
extern "C" void pascal near nullfunc_near(void);
void near marisa_bomb_draw(void);
void near bomb_dream_decay(void);

void pascal near bomb_marisa(void)
{
    if(bomb_frame < 80) {
        if(bomb_frame == 2) {
            scroll_active = false;
            graph_scrollup(0);
            bg_render_bombing = nullfunc_near;
        }
        marisa_bomb_draw();
        bomb_dream_decay();
    } else {
        if(bomb_frame == 80) {
            snd_se_play(15);
            if(stage_id != 5) {
                scroll_active = true;
            }
            items_pull_to_player = false;
            goto restore_background;
        }
        if(bomb_frame < 96) {
restore_background:
            bg_render_bombing = bg_render_bombing_func;
            PaletteTone = 192 - ((bomb_frame - 80) * 6);
            palette_changed = true;
            if(bomb_frame == 82 && stage_id != 5) {
                graph_scrollup(scroll_line);
            }
        } else {
            bombing = false;
            PaletteTone = 100;
            palette_changed = true;
        }
    }
    bomb_frame++;
}
