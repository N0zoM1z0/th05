// Natural maintained TH04 gameover/gameexecl semantics, with independently
// reviewed TH05 score reset, resident statistics and resource-release order.
#pragma option -zCHANDOFF_TEXT -zPmain_01
#include "src/main/runtime/handoff.hpp"
#pragma codeseg HANDOFF_TEXT main_01

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

    // TC4's real 16-bit process.h takes mutable far strings. These legacy
    // qualifier casts preserve the original pointers and their actual ABI.
    // In large model NULL is a four-byte sentinel for this variadic API.
    return execl((char far *)binary_fn, (char far *)binary_fn, NULL);
}
