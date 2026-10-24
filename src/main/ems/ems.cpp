// Natural TH05 EMS resource cache from ReC98 th05/ems.cpp ->
// th04/main/ems.cpp, b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
#pragma option -zCEMS_TEXT -zPmain_01
#include "src/main/ems/ems.hpp"

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
