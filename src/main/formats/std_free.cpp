// Complete natural release function; no raw-DOS loader body is supplied here.
#pragma option -zCSTD_FREE_TEXT -zPmain_01 -k-
#include "src/main/formats/std_free.hpp"

void near std_free(void)
{
    if(std_seg) {
        hmem_free(std_seg);
        std_seg = 0;
    }
}
