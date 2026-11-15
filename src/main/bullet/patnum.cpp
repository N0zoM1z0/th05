// Sprite number of a directional 16x16 bullet or sword for a given angle.
// Same as ReC98's th05/main/bullet/patnum.cpp, minus its trailing alignment
// NOP, which belongs to the next function's segment here.
#pragma option -zCBULLET_P_TEXT -zPmain_03 -k-
#include "src/main/runtime/small.hpp"

// The function calculates a 16-bit return value, every call site assigns the
// result to a 16-bit variable, but ZUN still declared an 8-bit return type...
unsigned char pascal near bullet_patnum_for_angle(
	unsigned int patnum_base_, unsigned char angle
)
{
	#define angle_low  	static_cast<unsigned char>(_AL)
	#define angle_high 	static_cast<unsigned char>(_AH)
	#define angle_wide 	static_cast<unsigned int>(_AX)
	#define patnum_base	static_cast<unsigned int>(_BX)

	// Parameters are read straight off the stack, without a BP frame.
	_BX = _SP;
	angle_low = peekb(_SS, (_BX + 2)); /* = */ (angle);
	patnum_base = peek(_SS, (_BX + 4)); /* = */ (patnum_base_);
	// Offset by half of the per-sprite angle
	angle_low += ((ANGLE_PER_SPRITE / 2) - 1);

	// Yes, this is intended to also cover Yumeko's swords, which start
	// at a patnum higher than PAT_BULLET16_V. Make sure it stays that way.
	typedef char swords_use_full_circle[(PAT_SWORD > PAT_BULLET16_V) ? 1 : -1];
	if(patnum_base < PAT_BULLET16_V) {
		angle_low %= 0x80u;
	}

	angle_high ^= angle_high;
	angle_low >>= 3; // /= ANGLE_PER_SPRITE;
	angle_wide += patnum_base;
	return angle_wide;

	#undef patnum_base
	#undef angle_wide
	#undef angle_high
	#undef angle_low
}
