// Checksums and encrypts the high score section in [hi] before it is written
// to GENSOU.SCR. Based on ReC98 th04/formats/scoredat/encode.cpp.
//
// The loops index the bytes of [hi] directly. A local byte pointer, as in
// ReC98's helper, costs a stack frame and extra loads in this compiler. The
// rotation is written in assembly with an explicit BYTE PTR, because the C
// version compiles to a 16-bit rotation.
//
// The unit must be compiled directly to an object with `tcc -c`. Going
// through `tcc -S` and TASM produces the same instruction bytes, but emits the
// two irand() relocations in the opposite order.
#pragma option -zCSCORE_ENCODE_TEXT -zPop_01
#include <dos.h>
#include "src/op/hiscore/view.hpp"
extern "C" int pascal far irand(void);
#pragma codeseg SCORE_ENCODE_TEXT op_01
void pascal near scoredat_encode(void)
{
    int i;

    // Sum of all score bytes, excluding the keys and the checksum itself
    hi.score_sum = 0;
    i = offsetof(scoredat_section_t, score);
    while(i < sizeof(scoredat_section_t)) {
        hi.score_sum += reinterpret_cast<unsigned char *>(&hi)[i];
        i++;
    }
    hi.key1 = irand();
    hi.key2 = irand();

    // Encrypt backwards, feeding each encrypted byte into the next one
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
