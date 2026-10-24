// Natural ReC98 b6ba5b0a: th04/main/player/pos.cpp, GAME5 ABI.
#pragma option -zCPLAYER_P_TEXT -zPmain_01
#include "src/main/runtime/small.hpp"


static const pixel_t MOVE_MARGIN_LEFT = 8;
static const pixel_t MOVE_MARGIN_TOP = 8;
static const pixel_t MOVE_MARGIN_RIGHT = 8;
static const pixel_t MOVE_MARGIN_BOTTOM = 16;

#define clamp(v, min, max) \
	/* Sneaky! That's how we can pretend this is an actual function that */ \
	/* returns a value. */ \
	v; \
	if(static_cast<subpixel_t>(v) < small_to_sp(min)) { \
		v = small_to_sp(min); \
	} else if(static_cast<subpixel_t>(v) > small_to_sp(max)) { \
		v = small_to_sp(max); \
	}

void near player_pos_update_and_clamp(void)
{
	/* _DX:_AX = */ player_pos.update_seg1();
	_AX = clamp(_AX, (0 + MOVE_MARGIN_LEFT), (PLAYFIELD_W - MOVE_MARGIN_RIGHT));
	_DX = clamp(_DX, (0 + MOVE_MARGIN_TOP), (PLAYFIELD_H - MOVE_MARGIN_BOTTOM));
	player_pos.cur.x.v = _AX;
	player_pos.cur.y.v = _DX;
}
