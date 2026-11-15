// Declarations for the plain C++ sparks_render() attempt (render_candidate.cpp).
#ifndef TH05_SPARK_RENDER_CANDIDATE_HPP
#define TH05_SPARK_RENDER_CANDIDATE_HPP
#include <dos.h>
#include "src/main/effects/spark/lifecycle.hpp"

typedef pixel_t screen_x_t;
typedef char spark_screen_coordinate_is_2[(sizeof(screen_x_t) == 2) ? 1 : -1];
#pragma codeseg SPARK_BATCH_TEXT main_01
// Takes the GRCG color in AH, not as a stack argument.
void near grcg_setcolor_direct_raw(void);
extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
// Takes left in AX, top in DX and the cel (spark age) in CL.
extern "C" void __fastcall near spark_render(screen_x_t left, vram_y_t top);
extern "C" void near sparks_render(void);
#endif
