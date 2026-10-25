// Natural complete MPN upload candidate; exact acceptance is reviewed separately.
#pragma option -zC_TEXT
#include "src/main/formats/mpn_upload.hpp"

#pragma codeseg MPN_UPLOAD_TEXT main_01

extern "C" int pascal near mpn_load(const char far *filename)
{
    mpn_load_inner(filename);
    unsigned char page = 1;
    do {
        outportb(0xA6, page);
        unsigned int image = 0;
        for(unsigned int left = MPN_UPLOAD_SCREEN_W -
            (MPN_CACHE_COLUMNS * MPN_UPLOAD_TILE_W);
            left < MPN_UPLOAD_SCREEN_W; left += MPN_UPLOAD_TILE_W) {
            for(unsigned int top = 0; top < MPN_UPLOAD_SCREEN_H;
                top += MPN_UPLOAD_TILE_H) {
                mpn_put(static_cast<int>(left), static_cast<int>(top), image);
                image++;
            }
        }
    } while(--page == 0);
    mpn_free();
    // The maintained historical int interface has no assigned return value.
}
