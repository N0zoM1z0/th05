// Shared VSync wait with the original far Pascal word-argument boundary.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/abi.hpp"

extern "C" volatile unsigned int vsync_Count1;

void pascal far frame_delay(int frames)
{
    // Far return occupies four bytes; retain the original unsigned word view.
    _BX = _SP;
    _BX = peek(_SS, (_BX + 4));
    vsync_Count1 = 0;
    while(vsync_Count1 < _BX) {
    }
}
