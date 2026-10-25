// Natural C++ candidate for the conventional BX fastcall note query.
#pragma option -zCSHARED -k-
#include "src/shared/sound/pmd_part.hpp"
#pragma codeseg SHARED

extern "C" char __fastcall near piano_current_note_from(
    int unused_ax, int unused_dx, PmdPart near *near *part
)
{
    PmdPart near *current = *part;
    unsigned char gate = current->gate_time;
    if(gate > 4) {
        gate = 4;
    }
    if(current->remaining_length > gate && current->remaining_length > 1) {
        return current->note;
    }
    return -1;
}
