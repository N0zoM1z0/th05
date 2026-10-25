// Full four-plane segmented background ownership, without image data.
#ifndef TH05_BGIMAGE_FREE_HPP
#define TH05_BGIMAGE_FREE_HPP
#include "src/shared/abi.hpp"

struct bgimage_planes_t {
    unsigned char __seg *B;
    unsigned char __seg *R;
    unsigned char __seg *G;
    unsigned char __seg *E;
};
extern bgimage_planes_t bgimage;

#pragma codeseg _TEXT
extern "C" void pascal far hmem_free(void __seg *block);
#pragma codeseg SHARED
extern "C" void far bgimage_free(void);
#pragma codeseg

typedef char bgimage_planes_are_8[(sizeof(bgimage_planes_t) == 8) ? 1 : -1];
typedef char bgimage_B_at_0[(offsetof(bgimage_planes_t, B) == 0) ? 1 : -1];
typedef char bgimage_R_at_2[(offsetof(bgimage_planes_t, R) == 2) ? 1 : -1];
typedef char bgimage_G_at_4[(offsetof(bgimage_planes_t, G) == 4) ? 1 : -1];
typedef char bgimage_E_at_6[(offsetof(bgimage_planes_t, E) == 6) ? 1 : -1];
#endif
