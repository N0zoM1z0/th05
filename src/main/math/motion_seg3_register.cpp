// Original 12-byte PlayfieldMotion update with native register-based point return.
#pragma option -zCMOTION_SEG3_TEXT -zPmain_03 -k-
#include <dos.h>
#include "src/shared/geometry.hpp"
#pragma codeseg MOTION_SEG3_TEXT main_03
PlayfieldPoint pascal near PlayfieldMotion::update_seg3()
{
    _BX = _SP;
    _BX = peek(_SS, _BX + 2);
    _AX = *reinterpret_cast<unsigned int near *>(_BX);
    *reinterpret_cast<unsigned int near *>(_BX + 4) = _AX;
    _AX += *reinterpret_cast<unsigned int near *>(_BX + 8);
    *reinterpret_cast<unsigned int near *>(_BX) = _AX;
    _BX += 2;
    _DX = *reinterpret_cast<unsigned int near *>(_BX);
    *reinterpret_cast<unsigned int near *>(_BX + 4) = _DX;
    _DX += *reinterpret_cast<unsigned int near *>(_BX + 8);
    *reinterpret_cast<unsigned int near *>(_BX) = _DX;
}
