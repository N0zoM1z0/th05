// MPN upload interfaces: native far helpers in _TEXT, near caller in main_01.
#ifndef TH05_MAIN_FORMATS_MPN_UPLOAD_HPP
#define TH05_MAIN_FORMATS_MPN_UPLOAD_HPP

#include <dos.h>
#include "src/shared/abi.hpp"

extern "C" {
    void pascal far mpn_load_inner(const char far *filename);
    void pascal far mpn_put(int left, int top, unsigned int image);
    void pascal far mpn_free(void);
}

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
