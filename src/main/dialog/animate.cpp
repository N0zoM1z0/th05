// Complete dialog animation from the unchanged maintained tail owner.
#pragma option -zCDIALOG_TAIL_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/tail.hpp"
#pragma option -a2
// The actual far Pascal provider shares original physical CS frame 0AE1.
#pragma samecodeseg GameExecl

void far dialog_animate(void)
{
    if(resident->demo_num != 0) {
        if(dialog_sequence_id == 0) {
            main_pat_exalice_override_and_super_clean_stage();
            super_entry_bfnt(st06_bb1);
            super_entry_bfnt(st06_bb2);
            snd_load(BGM_EXTRA_BOSS_FN, SND_LOAD_SONG);
            snd_kaja_func(KAJA_SONG_PLAY, 0);
            file_ropen(DEMO_EXTRA_PART_2_FN);
            file_read(DemoBuf, (DEMO_N_EXTRA * sizeof(REC<1>)));
            file_close();
            stage_frame = 0;
            dialog_sequence_id++;
        } else {
            hmem_free(reinterpret_cast<void __seg *>(DemoBuf));
            palette_black_out(8);
            GameExecl(DIALOG_BINARY_OP);
        }
        return;
    }
    cdg_free(CDG_BG_PLAYCHAR_BOMB);
    dialog_pre();
    dialog_run();
    dialog_exit();
    dialog_post();
}

