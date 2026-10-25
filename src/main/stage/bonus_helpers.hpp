// Complete resident/Boss state and real stage-bonus display interfaces.
#ifndef TH05_STAGE_BONUS_HELPERS_HPP
#define TH05_STAGE_BONUS_HELPERS_HPP
#include "src/main/boss/movement.hpp"
#include "src/main/hud/resident.hpp"

extern unsigned char continues_used;
extern unsigned char rank;
// TH05 uses eleven real two-byte near pointers; strings remain foreign.
extern const char near *const STAGE_CLEAR_BONUS_DESC[11];
static const unsigned int BONUS_TX_RED = 0x41;
static const unsigned int BONUS_TX_GREEN = 0x81;

#pragma codeseg _TEXT
extern "C" void pascal far text_putsa(int left, int row,
    const char far *text, unsigned int attr);
#pragma codeseg BONUS_HELP_TEXT main_03
void pascal near stage_bonus_factor_apply(int row, int description, int factor,
    unsigned long far *points);
void pascal near stage_bonus_apply_modifiers(unsigned long far *points);

typedef char bonus_full_boss[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char bonus_full_resident[(sizeof(resident_t) == 128) ? 1 : -1];
typedef char bonus_credit_lives_13[(offsetof(resident_t, credit_lives) == 13) ? 1 : -1];
typedef char bonus_description_near22[(sizeof(STAGE_CLEAR_BONUS_DESC) == 22) ? 1 : -1];
#endif
