#ifndef TH05_RUNTIME_COMBINED
#pragma option -zCDEMO_TEXT -zPmain_01
#endif
#include "src/main/runtime/gameplay_loop.hpp"
#pragma codeseg DEMO_TEXT main_01
#pragma samecodeseg playperf_raise

void near gameplay_loop(void)
{
    slowdown_factor = 1;
    frame_delay(1);
    input_reset_sense();
    do {
        input_sense();
        input_sense_hook();
        if(key_det & INPUT_CANCEL) {
            if(pause()) {
                quit = Q_QUIT_TO_OP;
            }
        }
        std_update();
        stage_vm();
        if(bombing == false) {
            bg_render_not_bombing();
        } else {
            bg_render_bombing();
        }

        pointnums_update();
        circles_update();
        sparks_update();
        player_update();
        shots_update();
        lasers_update();
        bullets_update();
        enemies_update();
        midboss_update();
        boss_update();
        items_update();
        gather_update();
        stage_render();
        if(bombing) {
            playchar_bomb_func();
        }
        boss_fg_render();
        midboss_render();
        enemies_render();
        shots_render();
        player_render();
        grcg_setmode_rmw();
        boss_custombullets_render();
        lasers_render();
        gather_render();
        sparks_render();
        items_render();
        pointnums_render();
        bullets_render();
        circles_render();
        outportb(0x7C, 0);
        overlay1();
        overlay2();
        playfield_shake_update_and_render();
        input_reset_sense();

        total_slow_frames += (slowdown_caused_by_bullets |
            (vsync_Count1 >= slowdown_factor));
        total_frames++;
        if(debug_frame_step_enabled) {
            if(key_det & INPUT_Q) {
                if(debug_frame_step == 0) {
                    debug_frame_step = -2;
                } else if(debug_frame_step == -1) {
                    debug_frame_step = 1;
                }
            } else {
                if(debug_frame_step == 1) {
                    debug_frame_step = 0;
                } else {
                    (debug_frame_step == -2)
                        ? (void)(debug_frame_step = -1)
                        : (void)0;
                }
            }
        }
        if(debug_frame_step == 0) {
            slowdown_frame_delay();
        } else {
            player_is_hit = false;
        }

        palette_changed
            ? (void)(palette_show(), palette_changed = false)
            : (void)0;
        scroll_driver();
        outportb(0xA6, page_front);
        outportb(0xA4, page_back);
        page_front = page_back;
        page_back ^= 1;
        snd_se_update();
        frames_unused++;

        // The new frame value directly supplies the modulo fields.
        stage_frame_mod16 = (++stage_frame & 15);
        stage_frame_mod8 = (stage_frame_mod16 & 7);
        stage_frame_mod4 = (stage_frame_mod8 & 3);
        stage_frame_mod2 = (stage_frame_mod4 & 1);
        ((stage_frame & 4095) == 0)
            ? (void)playperf_raise(1)
            : (void)0;
        score_update_and_render();
    } while(quit == Q_KEEP_RUNNING);
}
