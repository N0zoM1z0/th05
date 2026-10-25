// Original MAINE near verdict callbacks and genuine far hardware/API boundaries.
#ifndef TH05_MAINE_VERDICT_ANIMATE_HPP
#define TH05_MAINE_VERDICT_ANIMATE_HPP
#include <dos.h>
#include "src/maine/verdict/format.hpp"
extern unsigned int PaletteTone;
extern const char near verdict_picture_filename[];
#pragma codeseg _TEXT
extern "C" {
    void pascal far palette_show(void);
    void pascal far palette_black_in(unsigned speed);
    void pascal far palette_black_out(unsigned speed);
    int pascal far graph_copy_page(int to_page);
}
#pragma codeseg SHARED
int pascal far pi_load(int slot, const char far *filename);
void pascal far pi_palette_apply(int slot);
void pascal far pi_put_8(screen_x_t left, screen_y_t top, int slot);
void pascal far pi_free(int slot);
void pascal far frame_delay(int frames);
int pascal far input_wait_for_change(int frames);
#ifdef TH05_VERDICT_FULL_FAMILY
#pragma codeseg VERDICT_FULL_TEXT group_01
#else
#pragma codeseg VERDICT_FOREIGN_TEXT group_01
#endif
void near verdict_main(void);
void near verdict_comments_put(void);
#ifdef TH05_VERDICT_FULL_FAMILY
#pragma codeseg VERDICT_FULL_TEXT group_01
#else
#pragma codeseg VERDICT_ANIMATE_TEXT group_01
#endif
void near verdict_animate(void);
#define verdict_graph_accesspage(page) outportb(0xA6, page)
#define verdict_graph_showpage(page) outportb(0xA4, page)
#endif
