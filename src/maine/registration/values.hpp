// Score/stage display uses native near-Pascal word arguments and Master frames.
#ifndef TH05_MREG_VALUES_HPP
#define TH05_MREG_VALUES_HPP
#pragma codeseg _TEXT
extern "C" {
    void pascal far super_put(int left, int top, int pattern);
    void pascal far graph_gaiji_putc(int left, int top, int glyph,
        unsigned int color);
}
#pragma codeseg SHARED
#include "src/op/hiscore/view.hpp"
extern uint8_t entered_place;
extern playchar_t playchar;
#pragma codeseg REG_VALUES_TEXT GROUP_01
void pascal near registration_score_put(int place, int pc);
void pascal near registration_stage_put(int place, int pc, int glyph);
#endif
