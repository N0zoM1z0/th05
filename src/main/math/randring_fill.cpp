// Fill the shared byte ring backward, then reset both cursor bytes.
#pragma option -zCRANDRING_FILL_TEXT -zPmain_01 -k-
#include "src/shared/abi.hpp"

extern unsigned char randring[256];
extern uint16_t randring_p;
#pragma codeseg _TEXT
extern "C" int pascal far IRand(void);
#pragma codeseg RANDRING_FILL_TEXT main_01

void near randring_fill(void)
{
    register int ring_index;
    ring_index = 255;
    do {
        randring[ring_index] = IRand();
    } while(--ring_index >= 0);
    randring_p = 0;
}
