// Frees the segment holding the current stage's .STD file.
#pragma option -zCSTD_FREE_TEXT -zPmain_01 -k-
#include "src/main/formats/std_free.hpp"

void near std_free(void)
{
    if(std_seg) {
        hmem_free(std_seg);
        std_seg = 0;
    }
}
