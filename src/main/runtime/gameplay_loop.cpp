// The per-frame gameplay loop, run once per stage until `quit` is set.
#ifndef TH05_RUNTIME_COMBINED
#pragma option -zCDEMO_TEXT -zPmain_01
#endif
#include "src/main/runtime/gameplay_loop.hpp"
#pragma codeseg DEMO_TEXT main_01
// playperf_raise() is far, in the same physical code segment (see entry.cpp).
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
        outportb(0x7C, 0); // GRCG off
        overlay1();
        overlay2();
        playfield_shake_update_and_render();
        input_reset_sense();

        total_slow_frames += (slowdown_caused_by_bullets |
            (vsync_Count1 >= slowdown_factor));
        total_frames++;
        // Debug mode: Q toggles a fast-forward mode. While debug_frame_step
        // is nonzero, the frame delay is skipped and the player can't be hit.
        // Press Q: 0 -> -2, release: -1, press again: 1, release: back to 0.
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
        outportb(0xA6, page_front); // graph_accesspage()
        outportb(0xA4, page_back);  // graph_showpage()
        page_front = page_back;
        page_back ^= 1;
        snd_se_update();
        frames_unused++;

        // ZUN bloat: the original copies the old frame number into DX and
        // never uses it, and masks the new one with a word-sized AND. Neither
        // `++stage_frame & 15` nor any other plain expression reproduces that,
        // so the counter is written with pseudo-registers. Loading DX first
        // gives the right size, but swaps the first two instructions.
        _AX = stage_frame;
        _DX = _AX;
        ++_AX;
        stage_frame = _AX;
        stage_frame_mod16 = (_AX &= 15);
        stage_frame_mod8 = (stage_frame_mod16 & 7);
        stage_frame_mod4 = (stage_frame_mod8 & 3);
        stage_frame_mod2 = (stage_frame_mod4 & 1);
        // Raise the play performance rank every 4096 frames.
        ((stage_frame & 4095) == 0)
            ? (void)playperf_raise(1)
            : (void)0;
        score_update_and_render();
    } while(quit == Q_KEEP_RUNNING);
}
