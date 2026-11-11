// Real PMD note state, 16-bit near fastcall BX pointer and AX packed bytes.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/pmd_part.hpp"
#pragma codeseg SHARED
extern "C" char __fastcall near piano_current_note_from(
    int unused_ax, int unused_dx, PmdPart near *near *part)
{
    asm { push bx }
    _BX = *reinterpret_cast<unsigned int near *>(_BX);
    _AX = *reinterpret_cast<unsigned int near *>(_BX + offsetof(PmdPart, remaining_length));
    if(_AH > 4) {
        _AH = 4;
    }
    if(_AL <= _AH) goto resting;
    if(_AL <= 1) goto resting;
    _AL = *reinterpret_cast<unsigned char near *>(_BX + offsetof(PmdPart, note));
    goto done;
resting:
    _AL = 0xFF;
done:
    asm { pop bx }
    return _AL;
}
