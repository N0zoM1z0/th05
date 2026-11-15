// The background snapshot's plane segments start out unallocated (0).
// Each __seg pointer is one 16-bit word.
#pragma option -zCBGIMAGE_PLANES_INIT_TEXT
#include "src/shared/hardware/bgimage_free.hpp"

bgimage_planes_t bgimage = { 0, 0, 0, 0 };
typedef char bgimage_startup_has_4_segment_words[(sizeof(bgimage) == 8) ? 1 : -1];
