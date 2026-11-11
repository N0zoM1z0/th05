#pragma option -zC_TEXT
#include "src/main/formats/mpn_upload.hpp"
#pragma codeseg MPN_UPLOAD_TEXT main_01
extern "C" int pascal near mpn_load(const char far *filename)
{
    mpn_load_inner(filename);
    _AL = 1;
    page_begin:
        asm { out 0A6h, al }
        asm { push ax }
        _BP = 0;
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
        asm { dec al; je page_begin }
    mpn_free();
}
