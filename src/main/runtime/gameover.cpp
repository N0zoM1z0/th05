// Game over: the playfield fade, the GAME OVER animation and the continue
// menu. Choosing not to continue hands off to MAINE for the score screen.
#pragma option -zCGAMEOVER_TEXT -zPmain_01
#include "src/main/runtime/gameover.hpp"
#pragma codeseg GAMEOVER_TEXT main_01

// Gaiji (font) slots. The playfield fade uses the 8 cels just below
// GAIJI_FADE_END; higher ones cover more of the screen.
#define GAIJI_FADE_END 0x40
#define GAIJI_BOLD_0 0xA0
#define GAIJI_BOLD_G 0xB0

// Fades the playfield in, one cel every 4 frames. Returns 1 when done.
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
                    gaiji_putca(x, y, (GAIJI_FADE_END - cel_num), GAMEOVER_TX_BLACK);
                }
            }
        }
    }
    gameover_fade_frame++;
    return 0;
}

// Fades the playfield out, one cel every 4 frames. Returns 1 when done.
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
                    gaiji_putca(x, y, (GAIJI_FADE_END - cel_num), GAMEOVER_TX_BLACK);
                }
            }
        }
    }
    return 0;
}

// Returns GAMEOVER_KEEP_RUNNING if the player continues. Otherwise, it
// starts MAINE and doesn't return.
unsigned char near gameover_run(void)
{
    // ZUN bloat: one variable for both the X column of the animation and
    // the result of the continue menu.
    int i;
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
    // A bold G slides in from the right, bounces off the left side and
    // stops where the full GAME OVER text then appears.
    for(i = 0x32; i > 8; i -= 2) {
        gaiji_putca(i, 12, GAIJI_BOLD_G, GAMEOVER_TX_WHITE);
        frame_delay(1);
        text_putsa(i, 12, gameover_erase_in, GAMEOVER_TX_WHITE);
    }
    for(i = 8; i < 0x14; i += 2) {
        gaiji_putca(i, 12, GAIJI_BOLD_G, GAMEOVER_TX_WHITE);
        frame_delay(1);
        text_putsa(i, 12, gameover_erase_out, GAMEOVER_TX_WHITE);
    }
    gaiji_putsa(20, 12, gGAMEOVER, GAMEOVER_TX_WHITE);
    input_wait_for_change(0);
    overlay_wipe();
    i = gameover_continue_menu();
    gameover_fade_frame = 0x20;
    while(1) {
        if(gameover_fade_out()) {
            break;
        }
        frame_delay(1);
    }
    if(i == GAMEOVER_KEEP_RUNNING) {
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
        snd_kaja_interrupt((2 << 8) | 4); // KAJA_SONG_FADE, speed 4
        palette_black_out(4);
        GameExecl(maine_binary);
    }
    return static_cast<unsigned char>(i);
}

// Returns GAMEOVER_KEEP_RUNNING if the player continues, 1 otherwise. There
// are no continues in the Extra Stage, and three per game otherwise.
unsigned char near gameover_continue_menu(void)
{
    unsigned char attr;
    unsigned char credits;
    int selected;
    int input;

    if(stage_id == 6) {
        return 1;
    }
    selected = 0;
    // Nonzero until the first poll, so that a key held from the game over
    // animation isn't taken as a menu choice.
    input = 1;
    credits = (3 - continues_used);
    if(credits == 0) {
        return 1;
    }
    gaiji_putsa(19, 10, gCONTINUE_QUESTION, GAMEOVER_TX_WHITE);
    gaiji_putsa(24, 13, gYES, (GAMEOVER_TX_GREEN | GAMEOVER_TX_REVERSE));
    gaiji_putsa(25, 15, gNO, GAMEOVER_TX_WHITE);
    gaiji_putsa(19, 22, gCREDIT, GAMEOVER_TX_GREEN);
    gaiji_putca(33, 22, (GAIJI_BOLD_0 + credits), GAMEOVER_TX_GREEN);

    for(;;) {
        input_reset_sense_held();
        // Only react on frames after a frame without input.
        if(input == 0) {
            input = key_det;
            if((input & GAMEOVER_INPUT_UP) || (input & GAMEOVER_INPUT_DOWN)) {
                selected = (1 - selected);
                if(selected == 0) {
                    attr = (GAMEOVER_TX_GREEN | GAMEOVER_TX_REVERSE);
                } else {
                    attr = GAMEOVER_TX_WHITE;
                }
                gaiji_putsa(24, 13, gYES, attr);
                if(selected == 1) {
                    attr = (GAMEOVER_TX_GREEN | GAMEOVER_TX_REVERSE);
                } else {
                    attr = GAMEOVER_TX_WHITE;
                }
                gaiji_putsa(25, 15, gNO, attr);
            }
            if(input & GAMEOVER_INPUT_CANCEL) {
                selected = 1;
                break;
            }
            if(input & GAMEOVER_INPUT_OK) {
                break;
            }
            if(input & GAMEOVER_INPUT_SHOT) {
                break;
            }
        } else {
            input = key_det;
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
        // The lowest digit of the score shares its byte with this counter.
        continues_used++;
        score_reset();
        hud_score_put();
        return GAMEOVER_KEEP_RUNNING;
    }
    return 1;
}
