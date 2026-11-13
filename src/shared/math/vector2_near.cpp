// Natural vector semantics from ReC98 b6ba5b0a th04/math/vector.hpp/vector2n.asm;
// the candidate's physical-register instructions and emitted bytes are omitted.
#pragma option -zCVECTOR2_NEAR_TEXT -zPmain_03
#include "src/shared/math/vector2_near.hpp"
#pragma codeseg VECTOR2_NEAR_TEXT main_03

extern "C" void pascal near vector2_near(
    SPPoint near &ret, unsigned char angle, subpixel_t length)
{
    _EDX = static_cast<signed long>(length);
    _BL = angle;
    _BH = 0;
    _BX += _BX;
    _ECX = *reinterpret_cast<const short near *>(
        reinterpret_cast<const char near *>(SinTable8) + _BX);
    _EAX = *reinterpret_cast<const short near *>(
        reinterpret_cast<const char near *>(CosTable8) + _BX);
    _EAX = static_cast<signed long>(_EAX * _EDX) >> VECTOR2_TRIG_FRAC_BITS;
    _EDX = static_cast<signed long>(_EDX * _ECX) >> VECTOR2_TRIG_FRAC_BITS;
    _BX = *reinterpret_cast<const unsigned int near *>(_BP + 8);
    *reinterpret_cast<short near *>(_BX) = _AX;
    *reinterpret_cast<short near *>(_BX + 2) = _DX;
}
