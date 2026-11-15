// Plain C++ attempt at randring1_next16(), the raw reader of the random ring.
// Not built: the readers are kept as original assembly (randring_readers.asm).
// This register-local form compiles to 15 bytes with an extra DX-to-AX move;
// a non-register local gives 21 bytes and a prefix increment 19.
//
// It reads a 16-bit word at the cursor (two overlapping ring bytes) and then
// increments only the low byte of the cursor, so it wraps at 256. ZUN quirk:
// at index 255 the high byte of the sample is the cursor's own low byte,
// since the cursor variable directly follows the ring.
#pragma option -zCRANDRING_NEXT_TEXT -zPmain_01 -k-
#include "src/shared/abi.hpp"
#pragma codeseg RANDRING_NEXT_TEXT main_01

extern unsigned char randring[256];
extern uint16_t randring_p;

uint16_t near randring1_next16(void)
{
    register uint16_t value = *reinterpret_cast<const uint16_t near *>(
        &randring[randring_p]);
    reinterpret_cast<unsigned char near *>(&randring_p)[0]++;
    return value;
}
