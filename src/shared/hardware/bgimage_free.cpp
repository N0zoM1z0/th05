// Natural maintained TH04 resource-release body; foreign image planes unchanged.
#pragma option -zCSHARED -k-
#include "src/shared/hardware/bgimage_free.hpp"
#pragma codeseg SHARED

extern "C" void far bgimage_free(void)
{
    if(bgimage.B != 0) {
        hmem_free(bgimage.B);
        hmem_free(bgimage.R);
        hmem_free(bgimage.G);
        hmem_free(bgimage.E);
        bgimage.B = 0;
    }
}
