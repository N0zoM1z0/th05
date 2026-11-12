// The original 4-plane PC-98 background snapshot is unallocated at startup.
// A __seg pointer occupies one genuine 16-bit DATA word in this DOS ABI.
#pragma option -zCBGIMAGE_PLANES_INIT_TEXT
#include "src/shared/hardware/bgimage_free.hpp"

bgimage_planes_t bgimage = { 0, 0, 0, 0 };
typedef char bgimage_startup_has_4_segment_words[(sizeof(bgimage) == 8) ? 1 : -1];
