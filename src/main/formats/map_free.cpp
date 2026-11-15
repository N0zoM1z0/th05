// Frees the segment holding the current stage's .MAP tile sections.
#pragma option -zCMAP_FREE_TEXT -zPmain_01 -k-
#include "src/main/formats/map_free.hpp"

void near map_free(void)
{
    if(map_seg) {
        hmem_free(map_seg);
        map_seg = 0;
    }
}
