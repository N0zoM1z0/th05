// PlayfieldMotion::update_seg3(): prev = cur, cur += velocity, return cur.
// ZUN bloat: main_01 and main_03 each have an identical copy of this method.
//
// The motion layout is cur at +0, prev at +4, velocity at +8. The original
// returns the new point in AX (X) and DX (Y), straight from the additions.
// A plain C++ version (see motion_seg1.cpp) makes Borland build the structure
// return in memory and reload it, so this one is written with pseudo-registers
// and deliberately has no return statement: AX:DX already hold the result.
#pragma option -zCMOTION_SEG3_TEXT -zPmain_03 -k-
#include <dos.h>
#include "src/shared/geometry.hpp"
#pragma codeseg MOTION_SEG3_TEXT main_03
PlayfieldPoint pascal near PlayfieldMotion::update_seg3()
{
    // BX = `this`, read from the stack above the near return address.
    _BX = _SP;
    _BX = peek(_SS, _BX + 2);

    // X: prev.x = cur.x; cur.x += velocity.x; result X stays in AX.
    _AX = *reinterpret_cast<unsigned int near *>(_BX);
    *reinterpret_cast<unsigned int near *>(_BX + 4) = _AX;
    _AX += *reinterpret_cast<unsigned int near *>(_BX + 8);
    *reinterpret_cast<unsigned int near *>(_BX) = _AX;

    // Y, one word further: same steps, result Y stays in DX.
    _BX += 2;
    _DX = *reinterpret_cast<unsigned int near *>(_BX);
    *reinterpret_cast<unsigned int near *>(_BX + 4) = _DX;
    _DX += *reinterpret_cast<unsigned int near *>(_BX + 8);
    *reinterpret_cast<unsigned int near *>(_BX) = _DX;
}
