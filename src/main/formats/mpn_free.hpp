// Full 16x16, four-plane .MPN image and its two-byte allocated-segment handle.
#ifndef TH05_MPN_FREE_HPP
#define TH05_MPN_FREE_HPP
#include "src/shared/abi.hpp"

struct mpn_image_t {
    uint16_t plane[4][16];
};
extern mpn_image_t __seg *mpn_images_seg;

#pragma codeseg _TEXT
extern "C" void pascal far hmem_free(void __seg *block);
extern "C" void pascal far mpn_free(void);
#pragma codeseg

typedef char mpn_image_is_128[(sizeof(mpn_image_t) == 128) ? 1 : -1];
typedef char mpn_segment_is_2[(sizeof(mpn_images_seg) == 2) ? 1 : -1];
#endif
