// Declarations for the standalone update.cpp.
#ifndef TH05_MREG_UPDATE_HPP
#define TH05_MREG_UPDATE_HPP
#include "src/maine/registration/glyphball.hpp"
#include "src/op/hiscore/view.hpp"

extern uint8_t entered_place;
extern playchar_t playchar;
extern int entered_name_cursor;

#pragma codeseg _TEXT
extern "C" {
    int pascal far iatan2(int y, int x);
    void pascal far super_put_rect(int left, int top, int pattern);
}
#pragma codeseg SHARED
extern "C" void pascal far bgimage_put_rect_16(
    int left, int top, int width, int height);
#include "src/shared/math/vector.hpp"
#pragma codeseg REG_NAME_TEXT GROUP_01
void pascal near reg_name_put(int place, playchar_t pc, uint8_t cursor);
#pragma codeseg REG_UPDATE_TEXT GROUP_01
void near glyphballs_update(void);
#pragma codeseg

// super_*() patterns (ReC98 names): 32x32 clouds and splashes in sctm0.bft,
// 16x16 balls in sctm1.bft.
static const int PAT_GLYPHBALL_CLOUD = 20;
static const int PAT_GLYPHBALL_SPLASH = 24;
static const int PAT_GLYPHBALL = 28;
static const int GLYPHBALL_CELS = 4;
static const int GLYPHBALL_CLOUD_SPLASH_W = 32;
static const int GLYPHBALL_W = 16;
#endif
