// Real four-character byte domain, identical to the canonical TH05 playchar ABI.
#ifndef TH05_MREG_SPAWN_HPP
#define TH05_MREG_SPAWN_HPP
#include "src/maine/registration/glyphball.hpp"

typedef enum {
    PLAYCHAR_REIMU = 0,
    PLAYCHAR_MARISA = 1,
    PLAYCHAR_MIMA = 2,
    PLAYCHAR_YUUKA = 3,
    PLAYCHAR_COUNT = 4,
    _playchar_t_FORCE_UINT8 = 0xFF
} playchar_t;

#pragma codeseg _TEXT
extern "C" int pascal far irand(void);
#pragma codeseg REG_FRAME_TEXT GROUP_01
void near registration_frame(void);
#pragma codeseg REG_SPAWN_TEXT GROUP_01
void pascal near glyphball_spawn(int x, int y, int place, playchar_t pc, uint8_t cursor);
#pragma codeseg

typedef char reg_spawn_playchar_is_byte[(sizeof(playchar_t) == 1) ? 1 : -1];
static const uint8_t REGISTRATION_SPACE_GLYPH = 0xCD;
static const uint8_t REGISTRATION_EMPTY_GLYPH = 0x02;
#endif
