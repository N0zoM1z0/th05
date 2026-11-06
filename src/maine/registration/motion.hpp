// Complete adjacent glyph creation/animation context and true provider frames.
#ifndef TH05_MREG_MOTION_HPP
#define TH05_MREG_MOTION_HPP
#include "src/maine/registration/glyphball.hpp"
#include "src/op/hiscore/view.hpp"

extern uint8_t entered_place;
extern playchar_t playchar;
extern int entered_name_cursor;

#pragma codeseg _TEXT
extern "C" {
    int pascal far irand(void);
    int pascal far iatan2(int y, int x);
    void pascal far super_put_rect(int left, int top, int pattern);
}
#pragma codeseg SHARED
extern "C" void pascal far bgimage_put_rect_16(
    int left, int top, int width, int height);
#include "src/shared/math/vector.hpp"
#pragma codeseg REG_NAME_TEXT GROUP_01
void pascal near reg_name_put(int place, playchar_t pc, uint8_t cursor);
void near registration_frame(void);
#pragma codeseg REG_MOTION_TEXT GROUP_01
void pascal near glyphball_spawn(int x, int y, int place, playchar_t pc, uint8_t cursor);
void near glyphballs_update(void);

static const uint8_t REGISTRATION_SPACE_GLYPH = 0xCD;
static const uint8_t REGISTRATION_EMPTY_GLYPH = 0x02;
static const int REG_GLYPH_CLOUD = 20;
static const int REG_GLYPH_SPLASH = 24;
static const int REG_GLYPH_BALL = 28;
static const int REG_GLYPH_CELS = 4;
static const int REG_CLOUD_SIZE = 32;
static const int REG_BALL_SIZE = 16;
#endif
