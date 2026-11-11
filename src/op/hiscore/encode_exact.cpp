// TH05 OP score checksum and backward key-based encoding, complete near Pascal.
#pragma option -zCSCORE_ENCODE_TEXT -zPop_01
#include <dos.h>
#include "src/op/hiscore/view.hpp"
extern "C" int pascal far irand(void);
#pragma codeseg SCORE_ENCODE_TEXT op_01
void pascal near scoredat_encode(void)
{
    int i;
    hi.score_sum = 0;
    i = offsetof(scoredat_section_t, score);
    while(i < sizeof(scoredat_section_t)) {
        hi.score_sum += reinterpret_cast<unsigned char *>(&hi)[i];
        i++;
    }
    hi.key1 = irand();
    hi.key2 = irand();
    unsigned char feedback = 0;
    i = sizeof(scoredat_section_t) - 1;
    while(i >= offsetof(scoredat_section_t, score)) {
        reinterpret_cast<unsigned char *>(&hi)[i] = (
            reinterpret_cast<unsigned char *>(&hi)[i] - (hi.key1 + feedback)
        );
        feedback = reinterpret_cast<unsigned char *>(&hi)[i];
        _AL = hi.key2;
        asm { ror byte ptr feedback, 3 }
        feedback ^= _AL;
        i--;
    }
}
