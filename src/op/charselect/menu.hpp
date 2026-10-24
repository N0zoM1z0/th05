// TH05 character selection interfaces, reused canonical resident/menu types.
// Natural-source provenance: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47,
// th05/m_char.cpp, th04/op/darken.cpp, planar.h, bgimage.hpp and op/impl.hpp.
#ifndef TH05_OP_CHARSELECT_MENU_HPP
#define TH05_OP_CHARSELECT_MENU_HPP

#include "src/op/main/menu.hpp"

typedef int bool16;
typedef int vram_offset_t;
typedef int vram_byte_amount_t;
typedef uint8_t dots8_t;
typedef uint16_t dots16_t;
typedef uint32_t dots32_t;
#define BYTE_DOTS 8
#define ROW_SIZE 80
static const uint8_t INPUT_NONE = 0;

// Actual foreign pointer object, not a constant substituted for its storage.
extern dots8_t far *VRAM_PLANE_B;
extern unsigned char playchar_menu_sel;
extern unsigned char playchar_menu_rank;
extern bool selectable_with[PLAYCHAR_COUNT];
extern unsigned char cleared_with[PLAYCHAR_COUNT][RANK_COUNT];

extern "C" {
    extern volatile unsigned int vsync_Count1;
    void pascal far cdg_put_noalpha_8(screen_x_t left, vram_y_t top, int slot);
    void pascal far grcg_byteboxfill_x(int left, int top, int right, int bottom);
    void far bgimage_snap(void);
    void far bgimage_free(void);
    void pascal far bgimage_put_rect_16(screen_x_t left, screen_y_t top,
        pixel_t width, pixel_t height);
    void pascal far palette_black_in(unsigned int speed);
}
#define palette_settone(tone_value) (PaletteTone = tone_value, palette_show())
#define graph_showpage(page_value) outportb(0xA4, page_value)
#define grcg_boxfill_8(left_value, top_value, right_value, bottom_value) \
    grcg_byteboxfill_x((left_value / BYTE_DOTS), top_value, \
        (right_value / BYTE_DOTS), bottom_value)

static inline vram_offset_t vram_offset_shift(screen_x_t x, vram_y_t y) {
    return (x >> 3) + (y << 6) + (y << 4);
}
// Genuine far memory access to the selected 1bpp hardware plane. The compiler
// emits the store; no instruction bytes or register-body transcription.
#define grcg_put(offset_value, pattern_value, bit_count) \
    *(dots##bit_count##_t far *)(VRAM_PLANE_B + offset_value) = pattern_value

inline void sync_pages_and_delay(void) {
    vsync_Count1 = 0;
    frame_delay(1);
    graph_showpage(1);
    graph_copy_page(0);
    vsync_Count1 = 0;
    frame_delay(1);
    graph_showpage(0);
}

void pascal near pic_darken(unsigned char playchar);
void pascal near pic_put(bool16 darkened);
void near playchar_menu_put_initial(void);

typedef char th05_charselect_word_bool_is_2[(sizeof(bool16) == 2) ? 1 : -1];
typedef char th05_charselect_offset_is_2[(sizeof(vram_offset_t) == 2) ? 1 : -1];
typedef char th05_charselect_pattern_is_4[(sizeof(dots32_t) == 4) ? 1 : -1];
typedef char th05_charselect_vram_pointer_is_4[(sizeof(VRAM_PLANE_B) == 4) ? 1 : -1];
typedef char th05_charselect_selectable_is_4[(sizeof(selectable_with) == 4) ? 1 : -1];
typedef char th05_charselect_cleared_is_20[(sizeof(cleared_with) == 20) ? 1 : -1];

#endif
