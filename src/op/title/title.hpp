// Real TH05 OP title ABI and shared sprite-load inline.
// Natural-source provenance: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47,
// th04/sprites/op_cdg.hpp, th05/formats/pi.hpp, th03/formats/cdg.h,
// pc98.h and th04/shiftjis/fnshared.hpp.
#ifndef TH05_OP_TITLE_HPP
#define TH05_OP_TITLE_HPP

#include "src/op/charselect/menu.hpp"

#if GAME != 5 || BINARY != 'O'
#error This owner is the TH05 OP title implementation
#endif

typedef bool page_t;
#define PAGE_COUNT 2
#define PI_MASK_COUNT 4u
#define BGM_MENU_MAIN_FN "op"
#define MENU_MAIN_BG_FN "op1.pi"

extern "C" {
    void pascal far cdg_load_all(int slot_first, const char far *filename);
    void pascal far cdg_load_single(int slot, const char far *filename, int n);
    void pascal far cdg_load_single_noalpha(int slot,
        const char far *filename, int n);
    void pascal far cdg_free_all(void);
}
void pascal far pi_put_masked_8(screen_x_t left, vram_y_t top,
    int slot, int mask_id);

inline void op_cdg_load_shared(void) {
    typedef char title_difficulty_sprite_extent_is_4[
        (CDG_OPTION_VALUE_RANK_last == CDG_OPTION_VALUE_RANK + 3) ? 1 : -1];
    cdg_load_all(CDG_NUMERAL, "sft1.cd2");
    cdg_load_all(CDG_MAIN, "sft2.cd2");
    cdg_load_all(CDG_CURSOR, "car.cd2");
}

typedef char th05_title_page_is_1[(sizeof(page_t) == 1) ? 1 : -1];

#endif
