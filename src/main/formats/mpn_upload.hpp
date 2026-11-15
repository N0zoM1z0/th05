// mpn_load() and the far .MPN helpers it calls.
#ifndef TH05_MAIN_FORMATS_MPN_UPLOAD_HPP
#define TH05_MAIN_FORMATS_MPN_UPLOAD_HPP

#include <dos.h>
#include "src/shared/abi.hpp"

extern "C" {
    void pascal far mpn_load_inner(const char far *filename);
    void pascal far mpn_put(int left, int top, unsigned int image);
    void pascal far mpn_free(void);
}

// The tile images are blitted to a reserved area of VRAM, the rightmost
// 4 tile columns (x = 576 to 639) over the full screen height, which the
// game covers with black text RAM cells. 4 * 25 = 100 tile images.
enum {
    MPN_UPLOAD_TILE_W = 16,
    MPN_UPLOAD_TILE_H = 16,
    MPN_UPLOAD_SCREEN_W = 640,
    MPN_UPLOAD_SCREEN_H = 400,
    MPN_CACHE_COLUMNS = 4
};

#pragma codeseg MPN_UPLOAD_TEXT main_01
extern "C" int pascal near mpn_load(const char far *filename);

#endif
