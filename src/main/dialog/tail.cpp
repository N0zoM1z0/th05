// The last four dialog functions, in original order: animation, face
// loading, bomb background restore and the Extra Stage sprite override.
// ReC98: th05/main/dialog/dialog.cpp.
//
// In this combined build only the face loader and the sprite override come
// out exactly as in the original. dialog_animate() and dialog_exit() are
// matched by animate.cpp and exit.cpp, but stay here to keep the layout.
#pragma option -zCDIALOG_TAIL_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/tail.hpp"
#pragma option -a2

// Same body as animate.cpp.
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

// Replaces the face at (left, top) with face [face_id] of the current side's
// faceset, or just removes it for FACE_NONE. The faceset comes from EMS if
// available, otherwise from disk.
void pascal near dialog_face_load_unput_put_free_8(int left, int top, int face_id)
{
    size_t size;
    uint32_t offset;
    char near *faceset_fn = faceset_boss_format;
    char near *faceset_playchar_fn = faceset_playchar_format;
    if(face_id != FACE_NONE) {
        if(Ems) {
            if(dialog_side == SIDE_PLAYCHAR) {
                offset = EMS_FACESET_PLAYCHAR_OFFSET;
            } else {
                offset = EMS_FACESET_BOSS_OFFSET;
            }
            // Each face is stored as its alpha plane followed by the four
            // color planes. The product is only 16 bits wide.
            size = cdg_slots[CDG_DIALOG_FACE].bitplane_size;
            offset += (face_id * size * (PLANE_COUNT + 1));
            allocate_and_load_from_ems(cdg_slots[CDG_DIALOG_FACE].seg_alpha(), offset, size);
            offset += size;
            size *= PLANE_COUNT;
            allocate_and_load_from_ems(cdg_slots[CDG_DIALOG_FACE].seg_colors(), offset, size);
            offset += size;   // ZUN bloat: never used
        } else {
            // Patch the stage or character digit into the file name.
            if(dialog_side != SIDE_PLAYCHAR) {
                faceset_fn[3] = ('0' + stage_id);
            } else {
                faceset_fn = faceset_playchar_fn;
                faceset_fn[3] = ('0' + playchar);
            }
            cdg_load_single(CDG_DIALOG_FACE, faceset_fn, face_id);
        }
    }
    frame_delay(1);
    dialog_face_unput_8(left, top);
    if(face_id != FACE_NONE) {
        cdg_put_8(left, top, CDG_DIALOG_FACE);
        cdg_free(CDG_DIALOG_FACE);
    }
}

// Same body as exit.cpp.
void near dialog_exit(void)
{
    if(Ems) {
        playchar_bomb_bg_load_from_ems();
    } else {
        switch(playchar) {
        case PLAYCHAR_REIMU:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_REIMU_FN, 0);
            break;
        case PLAYCHAR_MARISA:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_MARISA_FN, 0);
            break;
        case PLAYCHAR_MIMA:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_MIMA_FN, 0);
            break;
        case PLAYCHAR_YUUKA:
            cdg_load_single_noalpha(CDG_BG_PLAYCHAR_BOMB, BOMB_BG_YUUKA_FN, 0);
            break;
        }
    }
}

// Replaces the MIKO16.BFT sprites with the ST06_16.BFT ones used in the
// EX-Alice fight, also clearing all stage-specific sprites, then reloads the
// player's bomb shape sprites.
void near main_pat_exalice_override_and_super_clean_stage(void)
{
    super_clean(TINY_MIKO16_START, PAT_MAX);
    super_entry_bfnt(MIKO16_EXALICE_FN);
    for(int i = TINY_MIKO16_START; i < TINY_MIKO16_END; i++) {
        super_convert_tiny(i);
    }
    if(playchar == PLAYCHAR_YUUKA) {
        super_entry_bfnt(BOMB_SHAPE_YUUKA_FN_2);
    } else {
        super_entry_bfnt(BOMB_SHAPE_FN_2);
    }
}
