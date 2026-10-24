// TH05 EMS cache and complete CDG16 ABI. Natural ReC98 provenance:
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47, th04/main/ems.hpp,
// th03/formats/cdg.h, th04/sprites/main_cdg.h, th05/playchar.h.
#ifndef TH05_MAIN_EMS_HPP
#define TH05_MAIN_EMS_HPP
#include "src/main/hud/resident.hpp"
#if GAME != 5 || BINARY != 'M'
#error This owner is TH05 MAIN EMS resource caching
#endif

typedef uint16_t seg_t;
typedef uint8_t dots8_t;
enum cdg_plane_layout_t {
    CDG_COLORS = 0, CDG_COLORS_AND_ALPHA = 1, CDG_ALPHA = 2
};
// The actual file header and loaded-slot structure, not a reduced field view.
struct CDG {
    uint16_t bitplane_size;
    int pixel_w;
    int pixel_h;
    int offset_at_bottom_left;
    uint16_t vram_dword_w;
    uint8_t image_count;
    signed char plane_layout;
    dots8_t __seg *seg[2];
    dots8_t __seg *&seg_alpha() { return seg[0]; }
    dots8_t __seg *&seg_colors() { return seg[1]; }
};
static const int CDG_SLOT_COUNT = 64;
extern CDG cdg_slots[CDG_SLOT_COUNT];

static const int FACESET_PLAYCHAR_COUNT = 6;
static const int FACESET_BOSS_COUNT = 6;
enum main_cdg_slot_t {
    CDG_BG_PLAYCHAR_BOMB = 0,
    CDG_PER_STAGE,
    CDG_FACESET_PLAYCHAR,
    CDG_DIALOG_FACE = CDG_FACESET_PLAYCHAR,
    CDG_FACESET_PLAYCHAR_last = CDG_FACESET_PLAYCHAR + FACESET_PLAYCHAR_COUNT - 1,
    CDG_FACESET_BOSS,
    CDG_FACESET_BOSS_last = CDG_FACESET_BOSS + FACESET_BOSS_COUNT - 1,
    CDG_FACESET_BOSS_sentinel,
    CDG_BG_BOSS = 16,
    CDG_BG_2,
    CDG_PER_STAGE_last = 30,
    CDG_EYECATCH,
    CDG_COUNT
};
enum playchar_t {
    PLAYCHAR_REIMU = 0, PLAYCHAR_MARISA = 1, PLAYCHAR_MIMA = 2,
    PLAYCHAR_YUUKA = 3, PLAYCHAR_COUNT = 4,
    _playchar_t_FORCE_UINT8 = 0xFF
};
enum rank_t {
    RANK_EASY, RANK_NORMAL, RANK_HARD, RANK_LUNATIC, RANK_EXTRA,
    RANK_COUNT, RANK_SHOW_SETUP_MENU = 0xFF, _rank_t_FORCE_INT16 = 0x7FFF
};
static const unsigned char STAGE_EXTRA = 6;
static const int PLAYFIELD_LEFT = 32;
static const int PLAYFIELD_TOP = 16;
static const int PLAYFIELD_W = 384;
static const int PLAYFIELD_H = 368;
static const int EYECATCH_W = 288;
static const int EYECATCH_H = 176;
static const int BOMB_BG_W_MAX = (PLAYFIELD_W / 6) * 5;
static const int BOMB_BG_H_MAX = PLAYFIELD_H;
static const int FACE_W = 128;
static const int FACE_H = 128;
static const int PLANE_COUNT = 4;
static const int BYTE_DOTS = 8;

// Preserve the real32-bit constants; a TC4 signed enum would truncate them.
#define sizeof_planar_rect(w, h) ((((w) / BYTE_DOTS) * (h)) * static_cast<uint32_t>(PLANE_COUNT))
static const uint32_t EMS_EYECATCH_OFFSET = 0;
static const uint32_t EMS_EYECATCH_END = EMS_EYECATCH_OFFSET + sizeof_planar_rect(EYECATCH_W, EYECATCH_H);
static const uint32_t EMS_PLAYCHAR_BOMB_BG_OFFSET = 34000UL;
static const uint32_t EMS_PLAYCHAR_BOMB_BG_END = EMS_PLAYCHAR_BOMB_BG_OFFSET + sizeof_planar_rect(BOMB_BG_W_MAX, BOMB_BG_H_MAX);
static const uint32_t EMS_FACESET_PLAYCHAR_OFFSET = 100000UL;
static const uint32_t EMS_FACESET_PLAYCHAR_END = EMS_FACESET_PLAYCHAR_OFFSET + FACESET_PLAYCHAR_COUNT * sizeof_planar_rect(FACE_W, FACE_H);
static const uint32_t EMS_FACESET_BOSS_OFFSET = 200000UL;
static const uint32_t EMS_FACESET_BOSS_END = EMS_FACESET_BOSS_OFFSET + FACESET_BOSS_COUNT * sizeof_planar_rect(FACE_W, FACE_H);
static const uint32_t EMSSIZE = 320000UL;

extern seg_t Ems;
extern unsigned char stage_id;
extern unsigned char rank;
extern playchar_t playchar;
extern char far *eyename;
extern char far *bbname;
extern const char near EMS_NAME[];
extern const char near FACESET_REIMU_FN_0[];
extern const char near FACESET_MARISA_FN_0[];
extern const char near FACESET_MIMA_FN[];
extern const char near FACESET_YUUKA_FN[];
extern unsigned int PaletteTone;
extern "C" {
    unsigned pascal far ems_allocate(unsigned long length);
    int pascal far ems_exist(void);
    unsigned long pascal far ems_space(void);
    int pascal far ems_setname(unsigned handle, const char far *name);
    int pascal far ems_write(unsigned handle, long offset, const void far *memory, long size);
    int pascal far ems_read(unsigned handle, long offset, void far *memory, long size);
    void __seg *pascal far hmem_allocbyte(unsigned bytesize);
    void pascal far palette_show(void);
    void pascal far palette_black_in(unsigned speed);
    void pascal far cdg_load_single_noalpha(int slot, const char far *filename, int n);
    void pascal far cdg_load_all_noalpha(int slot, const char far *filename);
    void pascal far cdg_load_all(int slot, const char far *filename);
    void pascal far cdg_free(int slot);
    void pascal far cdg_put_noalpha_8(int left, int top, int slot);
}
void near ems_allocate_and_preload_eyecatch(void);
void near bomb_bg_load__ems_preload_playchar_cdgs(void);
void pascal near ems_preload_boss_faceset(const char far *filename);
void near eyecatch_animate(void);

#define allocate_and_load_from_ems(dst_seg, src_off, size) { \
    reinterpret_cast<void __seg *>(dst_seg) = hmem_allocbyte(size); \
    ems_read(Ems, src_off, dst_seg, size); \
}
#define palette_settone(tone) (PaletteTone = (tone), palette_show())

typedef char th05_ems_cdg_is_16[(sizeof(CDG) == 16) ? 1 : -1];
typedef char th05_ems_cdg_bitplane_at_0[(offsetof(CDG, bitplane_size) == 0) ? 1 : -1];
typedef char th05_ems_cdg_width_at_2[(offsetof(CDG, pixel_w) == 2) ? 1 : -1];
typedef char th05_ems_cdg_height_at_4[(offsetof(CDG, pixel_h) == 4) ? 1 : -1];
typedef char th05_ems_cdg_bottom_at_6[(offsetof(CDG, offset_at_bottom_left) == 6) ? 1 : -1];
typedef char th05_ems_cdg_dword_width_at_8[(offsetof(CDG, vram_dword_w) == 8) ? 1 : -1];
typedef char th05_ems_cdg_count_at_10[(offsetof(CDG, image_count) == 10) ? 1 : -1];
typedef char th05_ems_cdg_layout_at_11[(offsetof(CDG, plane_layout) == 11) ? 1 : -1];
typedef char th05_ems_cdg_segments_at_12[(offsetof(CDG, seg) == 12) ? 1 : -1];
typedef char th05_ems_segment_pointer_is_2[(sizeof(dots8_t __seg *) == 2) ? 1 : -1];
typedef char th05_ems_slots_is_1024[(sizeof(cdg_slots) == 1024) ? 1 : -1];
typedef char th05_ems_playchar_is_1[(sizeof(playchar_t) == 1) ? 1 : -1];
typedef char th05_ems_slot_is_1[(sizeof(main_cdg_slot_t) == 1) ? 1 : -1];
typedef char th05_ems_rank_is_2[(sizeof(rank_t) == 2) ? 1 : -1];
typedef char th05_ems_resident_rank_at_17[(offsetof(resident_t, rank) == 17) ? 1 : -1];
typedef char th05_ems_resident_stage_at_19[(offsetof(resident_t, stage) == 19) ? 1 : -1];
typedef char th05_ems_resident_playchar_at_20[(offsetof(resident_t, playchar) == 20) ? 1 : -1];
#endif
