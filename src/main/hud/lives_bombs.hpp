// Lives and bomb counters in the HUD. TH05 keeps both counts in standalone
// byte globals rather than in the resident structure as TH04 does.
#ifndef TH05_HUD_LIVES_BOMBS_HPP
#define TH05_HUD_LIVES_BOMBS_HPP
#include "src/shared/abi.hpp"

extern unsigned char lives;
extern signed char bombs;
extern const char hud_lives_extra[11];
extern const char hud_bombs_extra[11];

static const unsigned int HUD_RESOURCE_EMPTY = 0x02;
static const unsigned int HUD_RESOURCE_DIGIT_ZERO = 0xA0;
static const unsigned int HUD_RESOURCE_BOMB = 0xD3;
static const unsigned int HUD_RESOURCE_YINYANG = 0xD4;
static const unsigned int HUD_RESOURCE_WHITE = 0xE1;

// master.lib text RAM functions, declared as in overlay.hpp.
#pragma codeseg _TEXT
extern "C" {
    void far pascal gaiji_putca(unsigned x, unsigned y,
        unsigned glyph, unsigned attribute);
    void far pascal text_putsa(unsigned x, unsigned y,
        const char far *text, unsigned attribute);
}
#pragma codeseg HUD_RESOURCES_TEXT main_01
void far hud_lives_put(void);
void far hud_bombs_put(void);
#pragma codeseg

typedef char hud_lives_state_is_byte[(sizeof(lives) == 1) ? 1 : -1];
typedef char hud_bombs_state_is_byte[(sizeof(bombs) == 1) ? 1 : -1];
typedef char hud_extra_string_is_11[(sizeof(hud_lives_extra) == 11) ? 1 : -1];
#endif
