// Full registration entities, score section and actual graphics/math providers.
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

static const int REG_GLYPH_CLOUD = 20;
static const int REG_GLYPH_SPLASH = 24;
static const int REG_GLYPH_BALL = 28;
static const int REG_GLYPH_CELS = 4;
static const int REG_CLOUD_SIZE = 32;
static const int REG_BALL_SIZE = 16;
#endif
