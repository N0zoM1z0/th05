// Natural new-game initialization adapted from maintained TH04 core source.
// TH05's four-character and rank/demo behavior follows the actual target.
#pragma option -zCSESSION_INIT_TEXT -zPmain_01
#include "src/main/runtime/gameplay_session_init.hpp"
#pragma codeseg SESSION_INIT_TEXT main_01

void near gameplay_session_init(void)
{
    resident->graze = 0;
    resident->miss_count = 0;
    resident->bombs_used = 0;
    resident->end_sequence = 0x37; // ES_INGAME
    playchar = resident->playchar;
    bombs = resident->credit_bombs;
    lives = resident->credit_lives;
    for(int i = 0; i < SCORE_DIGITS; i++) {
        score.digits[i] = 0;
    }
    power = 1;
    dream = 1;
    bb_txt_load();

    switch(playchar) {
    case SESSION_REIMU:
        playchar_speed_aligned = 56;
        playchar_speed_diagonal = 40;
        playchar_bomb_func = bomb_reimu;
        break;
    case SESSION_MARISA:
        playchar_speed_aligned = 64;
        playchar_speed_diagonal = 48;
        playchar_bomb_func = bomb_marisa;
        break;
    case SESSION_MIMA:
        playchar_speed_aligned = 72;
        playchar_speed_diagonal = 52;
        playchar_bomb_func = bomb_mima;
        break;
    case SESSION_YUUKA:
        playchar_speed_aligned = 56;
        playchar_speed_diagonal = 40;
        playchar_bomb_func = bomb_yuuka;
        break;
    }
    playchar_shot_funcs = SHOT_FUNCS[playchar];

    if(resident->demo_num != 0) {
        if(resident->demo_num < 5) {
            playperf = 40;
            rank = SESSION_LUNATIC;
        } else {
            playperf = 32;
            rank = SESSION_EXTRA;
        }
        turbo_mode = true;
    } else {
        playperf = 32;
        if(stage_id == 6) {
            rank = SESSION_EXTRA;
            turbo_mode = true;
        } else {
            rank = resident->rank;
            turbo_mode = resident->turbo_mode;
        }
    }

    score_reset();
    hiscore_load();
    switch(rank) {
    case SESSION_EASY:
        item_point_score_at_full_dream = 6000;
        graze_score = 25;
        playperf_min = 16;
        playperf_max = 32;
        bullet_template_tune = bullet_template_tune_easy;
        break;
    case SESSION_NORMAL:
        item_point_score_at_full_dream = 10000;
        graze_score = 50;
        playperf_min = 24;
        playperf_max = 40;
        bullet_template_tune = bullet_template_tune_normal;
        break;
    case SESSION_HARD:
        item_point_score_at_full_dream = 15000;
        playperf = 44;
        graze_score = 100;
        playperf_min = 44;
        playperf_max = 54;
        bullet_template_tune = bullet_template_tune_hard;
        break;
    case SESSION_LUNATIC:
        item_point_score_at_full_dream = 20000;
        graze_score = 200;
        playperf = 48;
        playperf_min = 48;
        playperf_max = 58;
        bullet_template_tune = bullet_template_tune_lunatic;
        break;
    case SESSION_EXTRA:
        item_point_score_at_full_dream = 40000u;
        graze_score = 500;
        playperf_min = 32;
        playperf_max = 36;
        bullet_template_tune = bullet_template_tune_normal;
        break;
    }
}
