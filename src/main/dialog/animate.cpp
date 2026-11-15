// dialog_animate(): runs a pre-boss dialog script, or, during the Extra Stage
// replay, skips it and loads the assets and replay data it would have loaded.
// tail.cpp keeps an identical copy so that its later functions land at their
// original offsets; only this standalone build reproduces the original call
// to GameExecl().
#pragma option -zCDIALOG_TAIL_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/tail.hpp"
#pragma option -a2
// GameExecl() lives in the same code segment. Telling the compiler so lets
// TLINK turn the far call into the original NOP / PUSH CS / CALL near.
#pragma samecodeseg GameExecl

void far dialog_animate(void)
{
    // A replay reaching this point must be the Extra Stage one, the only one
    // long enough. The dialog is skipped.
    if(resident->demo_num != 0) {
        if(dialog_sequence_id == 0) {
            // Pre-boss: load everything _DM06.TX2 would have loaded, then the
            // second half of the replay. ZUN bloat: this could have been part
            // of demo_load().
            main_pat_exalice_override_and_super_clean_stage();
            super_entry_bfnt(st06_bb1);
            super_entry_bfnt(st06_bb2);
            snd_load(BGM_EXTRA_BOSS_FN, SND_LOAD_SONG);
            snd_kaja_func(KAJA_SONG_PLAY, 0);
            file_ropen(DEMO_EXTRA_PART_2_FN);
            file_read(DemoBuf, (DEMO_N_EXTRA * sizeof(REC<1>)));
            file_close();
            stage_frame = 0;   // indexes DemoBuf during replays
            dialog_sequence_id++;
        } else {
            // Post-boss: return to the title screen.
            hmem_free(reinterpret_cast<void __seg *>(DemoBuf));
            palette_black_out(8);
            GameExecl(DIALOG_BINARY_OP);
        }
        return;
    }
    cdg_free(CDG_BG_PLAYCHAR_BOMB);   // dialog_exit() reloads it
    dialog_pre();
    dialog_run();
    dialog_exit();
    dialog_post();
}

