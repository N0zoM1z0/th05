// Natural maintained TH04 donor, independently adapted to TH05's original
// input polling, separate remaining-life/bomb globals and game-over behavior.
#pragma option -zCGAMEOVER_TEXT -zPmain_01
#include "src/main/runtime/gameover.hpp"
#pragma codeseg GAMEOVER_TEXT main_01

unsigned char near gameover_fade_in(void)
{
    unsigned char cel_num;
    if(gameover_fade_frame >= 0x24) {
        overlay_wipe();
        overlay1 = nullfunc_near;
        return 1;
    }
    if((gameover_fade_frame % 4) == 0) {
        cel_num = (gameover_fade_frame / 4);
        if(cel_num != 0) {
            for(int y = 1; y < 24; y++) {
                for(int x = 4; x < 52; x += 2) {
                    gaiji_putca(x, y, (0x40 - cel_num), GAMEOVER_TX_BLACK);
                }
            }
        }
    }
    gameover_fade_frame++;
    return 0;
}

unsigned char near gameover_fade_out(void)
{
    unsigned char cel_num;
    if(gameover_fade_frame == 0) {
        overlay_black();
        overlay1 = nullfunc_near;
        return 1;
    }
    gameover_fade_frame--;
    if((gameover_fade_frame % 4) == 0) {
        cel_num = (gameover_fade_frame / 4);
        if(cel_num != 0) {
            for(int y = 1; y < 24; y++) {
                for(int x = 4; x < 52; x += 2) {
                    gaiji_putca(x, y, (0x40 - cel_num), GAMEOVER_TX_BLACK);
                }
            }
        }
    }
    return 0;
}

unsigned char near gameover_run(void)
{
    int y;
    gameover_fade_frame = 0x20;
    while(1) {
        if(gameover_fade_out()) {
            break;
        }
        frame_delay(1);
    }
    PaletteTone = 50;
    palette_show();
    while(1) {
        if(gameover_fade_in()) {
            break;
        }
        frame_delay(1);
    }
    for(y = 0x32; y > 8; y -= 2) {
        gaiji_putca(y, 12, 0xB0, GAMEOVER_TX_WHITE);
        frame_delay(1);
        text_putsa(y, 12, gameover_erase_in, GAMEOVER_TX_WHITE);
    }
    for(y = 8; y < 0x14; y += 2) {
        gaiji_putca(y, 12, 0xB0, GAMEOVER_TX_WHITE);
        frame_delay(1);
        text_putsa(y, 12, gameover_erase_out, GAMEOVER_TX_WHITE);
    }
    gaiji_putsa(20, 12, gGAMEOVER, GAMEOVER_TX_WHITE);
    input_wait_for_change(0);
    overlay_wipe();
    y = gameover_continue_menu();
    gameover_fade_frame = 0x20;
    while(1) {
        if(gameover_fade_out()) {
            break;
        }
        frame_delay(1);
    }
    if(y == GAMEOVER_KEEP_RUNNING) {
        PaletteTone = 100;
        palette_show();
        while(1) {
            if(gameover_fade_in()) {
                break;
            }
            frame_delay(1);
        }
        overlay_wipe();
    } else {
        resident->end_sequence = GAMEOVER_END_SCORE;
        snd_kaja_interrupt((2 << 8) | 4);
        palette_black_out(4);
        GameExecl(maine_binary);
    }
    return static_cast<unsigned char>(y);
}

unsigned char near gameover_continue_menu(void)
{
    unsigned char atrb;
    unsigned char credits;
    int selected;
    int previous_input;

    if(stage_id == 6) {
        return 1;
    }
    selected = 0;
    previous_input = 1;
    credits = (3 - continues_used);
    if(credits == 0) {
        return 1;
    }
    gaiji_putsa(19, 10, gCONTINUE_QUESTION, GAMEOVER_TX_WHITE);
    gaiji_putsa(24, 13, gYES, (GAMEOVER_TX_GREEN | GAMEOVER_TX_REVERSE));
    gaiji_putsa(25, 15, gNO, GAMEOVER_TX_WHITE);
    gaiji_putsa(19, 22, gCREDIT, GAMEOVER_TX_GREEN);
    gaiji_putca(33, 22, (0xA0 + credits), GAMEOVER_TX_GREEN);

    for(;;) {
        input_reset_sense_held();
        if(previous_input == 0) {
            previous_input = key_det;
            if((previous_input & GAMEOVER_INPUT_UP) || (previous_input & GAMEOVER_INPUT_DOWN)) {
                selected = (1 - selected);
                if(selected == 0) {
                    atrb = (GAMEOVER_TX_GREEN | GAMEOVER_TX_REVERSE);
                } else {
                    atrb = GAMEOVER_TX_WHITE;
                }
                gaiji_putsa(24, 13, gYES, atrb);
                if(selected == 1) {
                    atrb = (GAMEOVER_TX_GREEN | GAMEOVER_TX_REVERSE);
                } else {
                    atrb = GAMEOVER_TX_WHITE;
                }
                gaiji_putsa(25, 15, gNO, atrb);
            }
            if(previous_input & GAMEOVER_INPUT_CANCEL) {
                selected = 1;
                break;
            }
            if(previous_input & GAMEOVER_INPUT_OK) {
                break;
            }
            if(previous_input & GAMEOVER_INPUT_SHOT) {
                break;
            }
        } else {
            previous_input = key_det;
        }
        frame_delay(1);
    }
    if(selected == 0) {
        hiscore_continue_enter();
        power = 1;
        dream = 1;
        bombs = resident->credit_bombs;
        lives = resident->credit_lives;
        shot_level_update();
        hud_lives_put();
        hud_bombs_put();
        continues_used++;
        score_reset();
        hud_score_put();
        return GAMEOVER_KEEP_RUNNING;
    }
    return 1;
}
