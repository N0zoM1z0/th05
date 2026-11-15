/* The HP bar value shown in the previous frame (see hp.cpp). */
#pragma option -zCHUD_HP_PREV_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif

#include "src/main/boss/late_game_state_publics.h"

int near hud_hp_bar_value_prev = 0;
typedef char native_hud_hp_bar_value_prev_width[(sizeof(hud_hp_bar_value_prev) == 2) ? 1 : -1];
