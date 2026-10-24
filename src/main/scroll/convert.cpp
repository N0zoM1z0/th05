// Natural ReC98 b6ba5b0a: th04/main/scrolly3.cpp.
// The two real near-Pascal functions end before the trailing reference NOP.
#pragma option -zCSCROLLY3_TEXT -zPmain_03 -k- -G
#include "src/main/runtime/small.hpp"


#define roll(y) \
	if(y >= RES_Y) { \
		y -= RES_Y; \
	} else if(y < 0) { \
		y += RES_Y; \
	}

extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_seg3(subpixel_t y)
{
	#define ret static_cast<vram_y_t>(_AX) // Must be signed!

	_BX = _SP;
	ret = peek(_SS, (_BX + 2));

	ret = TO_PIXEL(ret);
	if(scroll_active) {
		ret += scroll_line;
	}
	roll(ret);
	return ret;

	#undef ret
}

extern "C" vram_y_t pascal near scroll_subpixel_y_to_vram_always(subpixel_t y)
{
	#define ret static_cast<vram_y_t>(_AX) // Must be signed!

	_BX = _SP;
	ret = peek(_SS, (_BX + 2));

	ret = (TO_PIXEL(ret) + scroll_line);
	roll(ret);
	return ret;

	#undef ret
}
