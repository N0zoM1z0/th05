/* Four initialized far pointers to MAINE's PC-98 planar video hardware. */
#pragma option -zCVRAM_PLANES_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error Physical far pointer resources require C initialized DATA
#endif
#include "src/shared/hardware/vram_plane_frames.h"

PC98VramPlane near VRAM_PLANE_B = PC98_VRAM_AT(VRAM_SEGMENT_BLUE);
PC98VramPlane near VRAM_PLANE_R = PC98_VRAM_AT(VRAM_SEGMENT_RED);
PC98VramPlane near VRAM_PLANE_G = PC98_VRAM_AT(VRAM_SEGMENT_GREEN);
PC98VramPlane near VRAM_PLANE_E = PC98_VRAM_AT(VRAM_SEGMENT_EXTENDED);

typedef char vram_far_pointer_size[(sizeof(PC98VramPlane) == 4) ? 1 : -1];
typedef char vram_four_plane_bytes[(4 * sizeof(PC98VramPlane) == 16) ? 1 : -1];
