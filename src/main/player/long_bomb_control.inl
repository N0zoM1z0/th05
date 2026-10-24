// Shared natural lifecycle of Reimu/Yuuka's tile-mask and effect phases.
// The character wrappers supply their actual frame constants and callbacks.
void pascal near LONG_BOMB_FUNCTION(void)
{
    if(bomb_frame < 32) {
        tiles_bb_col = V_WHITE;
        bb_playchar_put(bomb_frame / 2);
    } else {
        if(bomb_frame == 32) {
            scroll_active = false;
            graph_scrollup(0);
            bg_render_bombing = nullfunc_near;
            goto draw_effect;
        }
        if(bomb_frame < LONG_BOMB_FADE_FRAME) {
draw_effect:
            LONG_BOMB_DRAW();
            bomb_dream_decay();
        } else {
            if(bomb_frame == LONG_BOMB_FADE_FRAME) {
                snd_se_play(15);
                if(stage_id != 5) {
                    scroll_active = true;
                }
                items_pull_to_player = false;
                goto restore_background;
            }
            if(bomb_frame < LONG_BOMB_END_FRAME) {
restore_background:
                bg_render_bombing = bg_render_bombing_func;
                PaletteTone = 192 - ((bomb_frame - LONG_BOMB_FADE_FRAME) * 3);
                palette_changed = true;
                if(bomb_frame == LONG_BOMB_SCROLL_FRAME && stage_id != 5) {
                    graph_scrollup(scroll_line);
                }
            } else {
                bombing = false;
                PaletteTone = 100;
                palette_changed = true;
            }
        }
    }
    bomb_frame++;
}
