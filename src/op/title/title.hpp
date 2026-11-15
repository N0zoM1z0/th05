// Declarations for the OP title screen: CDG/PI loaders and the sprite set
// shared by all OP menus. Based on ReC98 th04/sprites/op_cdg.hpp,
// th05/formats/pi.hpp and th03/formats/cdg.h.
#ifndef TH05_OP_TITLE_HPP
#define TH05_OP_TITLE_HPP

#include "src/op/charselect/menu.hpp"

#if GAME != 5 || BINARY != 'O'
#error This header is for TH05 OP.EXE only
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
    cdg_load_all(CDG_NUMERAL, "sft1.cd2");
    cdg_load_all(CDG_MAIN, "sft2.cd2");
    cdg_load_all(CDG_CURSOR, "car.cd2");
}

#endif
