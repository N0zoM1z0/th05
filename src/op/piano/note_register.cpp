// piano_current_note_from(): returns the note currently played by a PMD part,
// or 0xFF if the part is resting. Called from assembly with DS:BX pointing to
// the part's near pointer.
//
// The plain C++ version of this function compiles to 51 bytes instead of 30:
// Borland loads the two adjacent bytes separately, spills the gate into a
// local and adds a stack frame. Loading both through AX matches the original.
// Borland does not save BX on its own here, hence the explicit PUSH/POP.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/pmd_part.hpp"
#pragma codeseg SHARED
extern "C" char __fastcall near piano_current_note_from(
    int unused_ax, int unused_dx, PmdPart near *near *part)
{
    asm { push bx }
    _BX = *reinterpret_cast<unsigned int near *>(_BX);

    // AL = remaining length of the current note, AH = gate time
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
