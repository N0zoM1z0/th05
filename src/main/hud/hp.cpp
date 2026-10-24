// Natural ReC98 b6ba5b0a: th04/main/hud/hp.cpp, shared by GAME5.
#pragma option -zCHUD_HP_TEXT -zPmain_03
#include "src/main/runtime/small.hpp"

void pascal near hud_hp_update_and_render(int hp_cur, int hp_max)
{
	#define value_prev hud_hp_bar_value_prev
	extern int value_prev;

	int value_cur;

	if(hp_cur <= 0) {
		value_cur = 0;
	} else if(hp_cur >= hp_max) {
		value_cur = BAR_MAX;
	} else {
		value_cur = ((static_cast<long>(hp_cur) * BAR_MAX) / hp_max);
		if(value_cur < BAR_MAX) {
			value_cur++;
		}
	}
	if(value_prev < value_cur) {
		value_prev++;
	}
	if(value_prev > value_cur) {
		value_prev = value_cur;
	}
	hud_hp_put(value_prev);

	#undef value_prev
}
