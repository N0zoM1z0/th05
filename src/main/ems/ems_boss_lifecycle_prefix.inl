// Original complete 174+334+208+684 MAIN01 lifecycle source bodies.
#pragma codeseg LIFECYCLE_TEXT main_01
#include "src/shared/abi.hpp"
#pragma codeseg LIFECYCLE_TEXT main_01
void near stage_runtime_init(void);
// Natural maintained TH04 stage_runtime_init with actual TH05 state fields.
#include "src/main/ems/ems_boss_stage_runtime_types.hpp"
#pragma codeseg LIFECYCLE_TEXT main_01

void near stage_runtime_init(void)
{
    stage_state_init();
    stage_frame = 0;
    bombing_disabled = false;
    scroll_line = 0;
    tile_ring_scroll_row_prev = 0;
    scroll_line_on_page[0] = 0;
    scroll_line_on_page[1] = 0;
    scroll_subpixel_line.v = 0;
    scroll_row_advance_current = 0;
    scroll_row_advance_previous = 0;
    playfield_shake_x = 0;
    playfield_shake_y = 0;
    player_pos.cur.x.v = 192 * 16;
    player_pos.cur.y.v = 320 * 16;
    player_pos.prev.x.v = 192 * 16;
    player_pos.prev.y.v = 320 * 16;
    player_miss_animation_frame = 0;
    miss_time = 0;
    player_is_hit = false;
    player_invincibility_time = 64;
    stage_point_items_collected = 0;
    shot_time = 0;
    std_update = std_update_frames_then_animate_dialog_and_activate_boss_if_done;
    scroll_active = true;
    shot_level_update();
    randring_fill();
    items_init();
    bomb_reset();
    sparks_init();
    hud_score_put();
    pointnums_init();
    hud_put();
    bg_render_bombing_func = tiles_render_all;
    tiles_invalidate_reset();
}

// Diagnostic original-order 334+208+684-byte MAIN01 compiler context.
#include "src/shared/abi.hpp"
#pragma codeseg LIFECYCLE_TEXT main_01
// The real eight original function signatures, declared in one source order.
extern "C" void near stage_session_free(void);
extern "C" int near pause(void);
void near demo_load(void);
void near DemoPlay(void);
void near ems_allocate_and_preload_eyecatch(void);
void near bomb_bg_load__ems_preload_playchar_cdgs(void);
void pascal near ems_preload_boss_faceset(const char far *filename);
void near eyecatch_animate(void);
// Actual unchanged function bodies: src/main/runtime/session_end.cpp
// Natural TH04 maintained stage/session_init.cpp cleanup and menu semantics,
// with TH05's actual slot ranges, held-input service and release condition.
#include "src/main/runtime/session_end.hpp"
#pragma codeseg LIFECYCLE_TEXT main_01
#pragma codeseg LIFECYCLE_TEXT main_01

extern "C" void near stage_session_free(void)
{
    bb_boss_free();
    dialog_free();
    std_free();
    map_free();
    super_clean(STAGE_PATTERN_FIRST, STAGE_PATTERN_END);
    for(int i = STAGE_CDG_FIRST; i < STAGE_CDG_END; i++) {
        cdg_free(i);
    }
}

extern "C" int near pause(void)
{
    int selected = 0;
    while(key_det != 0) {
        input_reset_sense_held();
    }
    gaiji_putsa(26, 12, gsCHUUDAN, PAUSE_TX_YELLOW);
    gaiji_putsa(26, 14, gsSAIKAI, PAUSE_TX_WHITE + PAUSE_TX_UNDERLINE);
    gaiji_putsa(26, 15, gsSHUURYOU, PAUSE_TX_YELLOW);
    while(1) {
        input_wait_for_change(0);
        if((key_det & PAUSE_INPUT_UP) || (key_det & PAUSE_INPUT_DOWN)) {
            selected = 1 - selected;
            if(selected == 0) {
                gaiji_putsa(26, 14, gsSAIKAI, PAUSE_TX_WHITE + PAUSE_TX_UNDERLINE);
                gaiji_putsa(26, 15, gsSHUURYOU, PAUSE_TX_YELLOW);
            } else {
                gaiji_putsa(26, 14, gsSAIKAI, PAUSE_TX_YELLOW);
                gaiji_putsa(26, 15, gsSHUURYOU, PAUSE_TX_WHITE + PAUSE_TX_UNDERLINE);
            }
        }
        if(key_det & PAUSE_INPUT_Q) {
            return 1;
        }
        if(key_det & PAUSE_INPUT_CANCEL) {
            selected = 0;
            break;
        }
        if((key_det & PAUSE_INPUT_SHOT) || (key_det & PAUSE_INPUT_OK)) {
            break;
        }
    }
    // TH05 waits only for CANCEL release here; other held inputs survive.
    while(key_det & PAUSE_INPUT_CANCEL) {
        input_reset_sense_held();
    }
    text_putsa(26, 12, aGAME_PAUSE_SPACES_1, PAUSE_TX_WHITE);
    text_putsa(26, 14, aGAME_PAUSE_SPACES_2, PAUSE_TX_WHITE);
    text_putsa(26, 15, aGAME_PAUSE_SPACES_3, PAUSE_TX_WHITE);
    return selected;
}

#pragma codeseg LIFECYCLE_TEXT main_01
// Actual unchanged function bodies: src/main/demo/demo.cpp
// Natural TH05 behavior from ReC98 th05/demo.cpp -> th04/main/demo.cpp,
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47. No instruction macro is retained.
#include "src/main/demo/demo.hpp"
#pragma codeseg LIFECYCLE_TEXT main_01

void near demo_load(void)
{
    size_t size = ((resident->demo_num <= 4)
        ? sizeof(REC<DEMO_N>)
        : sizeof(REC<DEMO_N_EXTRA>)
    );
    DemoBuf = static_cast<uint8_t far *>(hmem_allocbyte(size));
    char far *fn = demo_fn;
    fn[4] = ('0' - 1 + resident->demo_num);
    file_ropen(fn);
    file_read(DemoBuf, size);
    file_close();
}

void near DemoPlay(void)
{
    size_t shift_offset = (resident->demo_num <= 4) ? DEMO_N : DEMO_N_EXTRA;
    if((key_det & ~INPUT_MOVEMENT) == 0) {
        key_det = DemoBuf[stage_frame];
        shiftkey = DemoBuf[stage_frame + shift_offset];
        if((resident->demo_num > 4) || (stage_frame < (DEMO_N - 4))) {
            return;
        }
    }
    hmem_free(reinterpret_cast<void __seg *>(DemoBuf));
    palette_black_out(8);
    GameExecl(DEMOPLAY_BINARY_OP);
}

#pragma codeseg LIFECYCLE_TEXT main_01
// Actual unchanged function bodies: src/main/ems/ems.cpp
// Natural TH05 EMS resource cache from ReC98 th05/ems.cpp ->
// th04/main/ems.cpp, b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
#include "src/main/ems/ems_boss_context_types.hpp"
#pragma codeseg LIFECYCLE_TEXT main_01

inline void ems_write_cdg_color_planes(seg_t &handle, long offset, main_cdg_slot_t slot)
{
    ems_write(handle, offset, cdg_slots[slot].seg_colors(),
        (cdg_slots[slot].bitplane_size * PLANE_COUNT));
}

// Deliberately preserve the original unbounded slot walk. It stops only when
// a slot has no loaded alpha plane; the original cache offsets are not clamps.
#define ems_transfer_cdgs_until_freed_slot(offset_first, slot_first) { \
    int slot = slot_first; \
    uint32_t offset = offset_first; \
    size_t bitplane_size = cdg_slots[slot_first].bitplane_size; \
    while(cdg_slots[slot].seg_alpha()) { \
        ems_write(Ems, offset, cdg_slots[slot].seg_alpha(), bitplane_size); \
        offset += bitplane_size; \
        ems_write(Ems, offset, cdg_slots[slot].seg_colors(), (bitplane_size * PLANE_COUNT)); \
        offset += (bitplane_size * PLANE_COUNT); \
        cdg_free(slot); \
        slot++; \
    } \
}

void near ems_allocate_and_preload_eyecatch(void)
{
    stage_id = resident->stage;
    if(stage_id == STAGE_EXTRA) {
        rank = RANK_EXTRA;
    } else {
        rank = resident->rank;
    }
    Ems = 0;
    if(!ems_exist() || (ems_space() < EMSSIZE)) {
        return;
    }
    Ems = ems_allocate(EMSSIZE);
    if(Ems) {
        ems_setname(Ems, EMS_NAME);
        cdg_load_single_noalpha(CDG_EYECATCH, eyename, 0);
        ems_write_cdg_color_planes(Ems, EMS_EYECATCH_OFFSET, CDG_EYECATCH);
        cdg_free(CDG_EYECATCH);
    }
}

// The original four word-sized switch entries start on an even boundary.
#pragma option -a2
void near bomb_bg_load__ems_preload_playchar_cdgs(void)
{
    bbname[2] = ('0' + resident->playchar);
    cdg_load_all_noalpha(CDG_BG_PLAYCHAR_BOMB, bbname);
    if(Ems) {
        ems_write_cdg_color_planes(Ems, EMS_PLAYCHAR_BOMB_BG_OFFSET, CDG_BG_PLAYCHAR_BOMB);
        switch(playchar) {
        case PLAYCHAR_REIMU:
            cdg_load_all(CDG_FACESET_PLAYCHAR, FACESET_REIMU_FN_0);
            break;
        case PLAYCHAR_MARISA:
            cdg_load_all(CDG_FACESET_PLAYCHAR, FACESET_MARISA_FN_0);
            break;
        case PLAYCHAR_MIMA:
            cdg_load_all(CDG_FACESET_PLAYCHAR, FACESET_MIMA_FN);
            break;
        case PLAYCHAR_YUUKA:
            cdg_load_all(CDG_FACESET_PLAYCHAR, FACESET_YUUKA_FN);
            break;
        }
        ems_transfer_cdgs_until_freed_slot(EMS_FACESET_PLAYCHAR_OFFSET, CDG_FACESET_PLAYCHAR)
    }
}

void pascal near ems_preload_boss_faceset(const char far *fn)
{
    if(!Ems) {
        return;
    }
    cdg_load_all(CDG_FACESET_BOSS, fn);
    ems_transfer_cdgs_until_freed_slot(EMS_FACESET_BOSS_OFFSET, CDG_FACESET_BOSS)
}

void near eyecatch_animate(void)
{
    if(Ems) {
        allocate_and_load_from_ems(cdg_slots[CDG_EYECATCH].seg_colors(),
            EMS_EYECATCH_OFFSET, (cdg_slots[CDG_EYECATCH].bitplane_size * PLANE_COUNT));
    } else {
        cdg_load_single_noalpha(CDG_EYECATCH, eyename, 0);
    }
    palette_settone(0);
    cdg_put_noalpha_8(
        (PLAYFIELD_LEFT + (PLAYFIELD_W / 2) - (EYECATCH_W / 2)),
        (PLAYFIELD_TOP + (PLAYFIELD_H / 2) - (EYECATCH_H / 2)),
        CDG_EYECATCH);
    cdg_free(CDG_EYECATCH);
    palette_black_in(1);
}
