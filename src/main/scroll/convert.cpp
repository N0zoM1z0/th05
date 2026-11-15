// Subpixel Y to VRAM Y conversions in MAIN's third code segment (ReC98
// th04/main/scrolly3.cpp). Both read their stack parameter through SP and
// return the result in AX.
#pragma option -zCSCROLLY3_TEXT -zPmain_03 -k- -G
#include "src/main/runtime/small.hpp"

// Wraps a VRAM Y coordinate back into the 400-line ring. Only corrects by
// one ring height, which is enough for on-screen coordinates.
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
