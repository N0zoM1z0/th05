// Hands control to another executable (OP or MAINE): saves the score and the
// play statistics to the resident structure, frees everything, and execl()s.
#pragma option -zCHANDOFF_TEXT -zPmain_01
#include "src/main/runtime/handoff.hpp"
#pragma codeseg HANDOFF_TEXT main_01

// Copies the score into the resident structure, then resets it.
void near game_state_save_score(void)
{
    for(int i = 0; i < SCORE_DIGITS; i++) {
        resident->score_last.digits[i] = score.digits[i];
    }
    score_reset();
}

int pascal far GameExecl(const char far *binary_fn)
{
    game_state_save_score();
    if(Ems) {
        ems_free(Ems);
    }
    resident->std_frames = total_std_frames;
    resident->items_spawned = items_spawned;
    resident->items_collected = items_collected;
    resident->point_items_collected = total_point_items_collected;
    resident->max_valued_point_items_collected = total_max_valued_point_items_collected;
    resident->enemies_gone = enemies_gone;
    resident->enemies_killed = enemies_killed;
    resident->slow_frames = total_slow_frames;
    resident->frames = total_frames;

    bb_txt_free();
    cdg_free_all();
    bb_boss_free();
    dialog_free();
    bb_playchar_free();
    std_free();
    map_free();
    super_free();
    graph_hide();
    text_clear();
    game_exit();

    // Turbo C++ 4.0's execl() takes non-const strings, hence the casts.
    // In the large model, NULL is 0L, a four-byte terminator. Only returns
    // if DOS can't start the program.
    return execl((char far *)binary_fn, (char far *)binary_fn, NULL);
}
