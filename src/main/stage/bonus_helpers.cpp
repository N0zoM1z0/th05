// Multipliers applied to both clear bonuses: boss timeout, starting lives,
// continues and difficulty. bonus_full.cpp compiles these into its own
// translation unit and provides the code segment pragmas itself.
#ifndef TH05_BONUS_HELPERS_COMBINED
#pragma option -zCBONUS_HELP_TEXT -zPmain_03
#include "src/main/stage/bonus_helpers.hpp"
#endif

// Multiplies [points] by [factor] tenths and prints the matching description
// in red for a penalty, or in green otherwise.
void pascal near stage_bonus_factor_apply(int row, int description, int factor,
    unsigned long far *points)
{
    int color;
    *points *= factor;
    *points /= 10UL;
    color = ((factor < 10) ? BONUS_TX_RED : BONUS_TX_GREEN);
    text_putsa(6, row, STAGE_CLEAR_BONUS_DESC[description], color);
}

void pascal near stage_bonus_apply_modifiers(unsigned long far *points)
{
    // A boss that timed out instead of being defeated voids the whole bonus.
    if(boss.phase_state.defeat_bonus == 0) {
        stage_bonus_factor_apply(20, 0, 0, points);
        return;
    }
    // Other starting-life, continue and rank values leave the bonus unchanged.
    switch(resident->credit_lives) {
    case 6: stage_bonus_factor_apply(18, 1, 3, points); break;
    case 5: stage_bonus_factor_apply(18, 2, 5, points); break;
    case 4: stage_bonus_factor_apply(18, 3, 7, points); break;
    }
    switch(continues_used) {
    case 1: stage_bonus_factor_apply(19, 4, 8, points); break;
    case 2: stage_bonus_factor_apply(19, 5, 6, points); break;
    case 3: stage_bonus_factor_apply(19, 6, 4, points); break;
    }
    switch(rank) {
    case 0: stage_bonus_factor_apply(20, 7, 5, points); break;
    case 1: stage_bonus_factor_apply(20, 8, 10, points); break;
    case 2: stage_bonus_factor_apply(20, 9, 12, points); break;
    case 3: stage_bonus_factor_apply(20, 10, 14, points); break;
    }
}
