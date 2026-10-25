// Complete stage1/2/4 render callbacks using the accepted full midboss ABI.
#ifndef TH05_MIDBOSS_RENDER_124_HPP
#define TH05_MIDBOSS_RENDER_124_HPP

#pragma codeseg _TEXT
extern "C" {
    void pascal far super_roll_put(int left, int top, int patnum);
    void pascal far super_roll_put_1plane(int left, int top, int patnum,
        int pattern_plane, unsigned int put_plane);
}
#pragma codeseg MID_FG_TEXT main_01
// Real first declarations precede the canonical stage callback list.
void pascal near midboss1_render(void);
void pascal near midboss2_render(void);
void pascal near midboss4_render(void);
#include "src/main/midboss/render5.hpp"

extern unsigned char stage_frame_mod8;
extern unsigned char stage_frame_mod16;
static const int MID1_PHASE2_PAT = 208;
static const int MID1_PHASE3_PAT = 212;
static const int MID2_STILL_PAT = 202;
static const int MID2_MOVING_PAT = 206;
static const unsigned int MID_FG_PUT_PLANES = 0xFF00 | 0xC0;
typedef char mid_fg_full_midboss[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
#endif
