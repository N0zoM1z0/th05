// Maintained TH04 release flow, with TH05's single allocated image bank.
#pragma option -zC_TEXT -k-
#include "src/main/formats/mpn_free.hpp"
#pragma codeseg _TEXT

extern "C" void pascal far mpn_free(void)
{
    if(mpn_images_seg) {
        hmem_free(mpn_images_seg);
        mpn_images_seg = 0;
    }
}
