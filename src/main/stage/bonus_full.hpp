// Stage Clear and All Clear bonus tallies, and the state and HUD functions
// they use.
#ifndef TH05_STAGE_BONUS_FULL_HPP
#define TH05_STAGE_BONUS_FULL_HPP
#include "src/main/stage/bonus_helpers.hpp"
#include "src/main/stage/bonus_previous_resources.h"

extern unsigned char stage_id;
extern unsigned char dream;
extern unsigned char lives;
extern unsigned char stage_point_items_collected;
extern unsigned char extends_gained;
extern unsigned int stage_graze;
extern unsigned int extend_point_items_collected;
extern unsigned int PaletteTone;
extern unsigned long score_delta;

// Tally labels (bonus_pointers.cpp) and gaiji captions (bonus_glyph_text.cpp)
extern const char near *BONUS_STAGE;
extern const char near *BONUS_DREAM;
extern const char near *GRAZEX50;
extern const char near *POINT_ITEMS;
extern const char near *BONUS_NOMISS;
extern const char near *BONUS_NOBOMB;
extern const char near *BONUS_TOTAL;
extern const char near *ALL_CLEAR;
extern const char near *PLAYER_REM;
extern const char near *POINT_TOTAL;
extern const char near gpCLEAR_BONUS[];
extern const char near gpCONGRATULATION[];
// Text RAM attributes
static const unsigned int BONUS_TX_WHITE = 0xE1;
static const unsigned int BONUS_TX_CYAN = 0xA1;

#pragma codeseg _TEXT
extern "C" {
    void pascal far palette_show(void);
    void pascal far gaiji_putsa(int left, int row, const char far *text,
        unsigned int attr);
}
#pragma codeseg BONUS_MAIN01_TEXT main_01
extern "C" {
    void pascal far playperf_raise(char delta);
    void pascal far playperf_lower(char delta);
}
#pragma codeseg BONUS_HELP_TEXT main_03
// Far functions in the same code segment as the bonus functions. TLINK turns
// the far calls into NOP / PUSH CS / near CALL.
void pascal far hud_points_put(unsigned int left, unsigned int row,
    unsigned long points);
void pascal far hud_5_digit_put(unsigned int left, unsigned int row,
    unsigned int value, unsigned int attr);
#pragma samecodeseg hud_points_put
#pragma samecodeseg hud_5_digit_put
void near stage_clear_bonus(void);
void near stage_allclear_bonus(void);
#endif
