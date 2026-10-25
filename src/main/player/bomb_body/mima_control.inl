void pascal near bomb_mima(void)
{
    if(bomb_frame < 64) {
        if(bomb_frame == 2) {
            scroll_active = false;
            graph_scrollup(0);
            bg_render_bombing = nullfunc_near;
        }
        mima_bomb_draw();
        bomb_dream_decay();
    } else {
        if(bomb_frame == 64) {
            snd_se_play(15);
            if(stage_id != 5) {
                scroll_active = true;
            }
            items_pull_to_player = false;
            goto restore_background;
        }
        if(bomb_frame < 80) {
restore_background:
            bg_render_bombing = bg_render_bombing_func;
            PaletteTone = 192 - ((bomb_frame - 64) * 6);
            palette_changed = true;
            if(bomb_frame == 66 && stage_id != 5) {
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
