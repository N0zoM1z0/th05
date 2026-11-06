// Read overlapping WORDs from the byte ring and wrap only the low cursor byte.
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
