// This release path is natural C++; the TH05 raw-DOS load path stays foreign.
#pragma option -zCMAP_FREE_TEXT -zPmain_01
#include "src/main/formats/map_free.hpp"

void near map_free(void)
{
    if(map_seg) {
        hmem_free(map_seg);
        map_seg = 0;
    }
}
