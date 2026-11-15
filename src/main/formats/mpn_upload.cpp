// Loads a stage's .MPN tile images and blits all of them into the tile
// source area of both VRAM pages, then frees the images again.
//
// Register roles: AL = VRAM page (1, then 0), SI = left, DI = top,
// BP = image number. ZUN quirk: declared to return int, but never sets AX.
#pragma option -zC_TEXT
#include "src/main/formats/mpn_upload.hpp"
#pragma codeseg MPN_UPLOAD_TEXT main_01
extern "C" int pascal near mpn_load(const char far *filename)
{
    mpn_load_inner(filename);
    _AL = 1;
    page_begin:
        asm { out 0A6h, al }   // graph_accesspage(AL)
        asm { push ax }
        _BP = 0;   // both pages receive the same 100 images
        _SI = MPN_UPLOAD_SCREEN_W - MPN_CACHE_COLUMNS * MPN_UPLOAD_TILE_W;
        do {
            _DI = 0;
            do {
                mpn_put(_SI, _DI, _BP);
                _BP++;
                _DI += MPN_UPLOAD_TILE_H;
            } while(_DI < MPN_UPLOAD_SCREEN_H);
            _SI += MPN_UPLOAD_TILE_W;
        } while(_SI < MPN_UPLOAD_SCREEN_W);
        asm { pop ax }
        // Page 1 -> 0 loops once more; 0 -> 0xFF ends. Inline DEC/JE keeps
        // the original branch on the decrement's own flags.
        asm { dec al; je page_begin }
    mpn_free();
}
