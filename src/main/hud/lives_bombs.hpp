// TH05 resource-count HUD, using canonical standalone byte state.
// Natural donor: maintained TH04 src/main/hud/hud.cpp. Actual TH05 globals,
// signed display locals, unsigned bomb-count comparison and calls reviewed
// independently in locally attested MAIN.
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

// The same real MASTER declarations used by accepted overlay.hpp; no new
// bridge, guessed register convention or return value is introduced.
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
