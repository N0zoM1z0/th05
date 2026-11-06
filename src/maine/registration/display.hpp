// One true declaration context for the adjacent name and row renderers.
#ifndef TH05_MREG_DISPLAY_HPP
#define TH05_MREG_DISPLAY_HPP
#include <dos.h>
#pragma codeseg _TEXT
extern "C" {
    void pascal far graph_gaiji_puts(int left, int top, int step,
        const char far *text, unsigned int color);
    void pascal far graph_gaiji_putc(int left, int top, int glyph,
        unsigned int color);
    void pascal far grcg_setcolor(int mode, unsigned int color);
    void pascal far grcg_hline(int left, int right, int y);
    void pascal far grcg_vline(int x, int top, int bottom);
}
#pragma codeseg SHARED
extern "C" void pascal far bgimage_put_rect_16(
    int left, int top, int width, int height);
#include "src/op/hiscore/view.hpp"
extern uint8_t entered_place;
extern playchar_t playchar;
#pragma codeseg REG_VALUES_TEXT GROUP_01
void pascal near registration_score_put(int place, int pc);
void pascal near registration_stage_put(int place, int pc, int glyph);
#pragma codeseg REG_DISPLAY_TEXT GROUP_01
void pascal near reg_name_put(int place, playchar_t pc, uint8_t cursor);
void pascal near registration_place_put(int place, int pc);
#endif
