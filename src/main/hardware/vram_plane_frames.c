/* Original MAIN near-data bank of physical PC-98 VRAM plane pointers. */
#pragma option -zCMAIN_VRAM_PLANES_TEXT -zPmain_01
#ifdef __cplusplus
#error Native video-plane DATA must be produced by the C compiler
#endif
#include "src/shared/hardware/vram_plane_frames.h"

PC98VramPlane near VRAM_PLANE_B = PC98_VRAM_AT(VRAM_SEGMENT_BLUE);
PC98VramPlane near VRAM_PLANE_R = PC98_VRAM_AT(VRAM_SEGMENT_RED);
PC98VramPlane near VRAM_PLANE_G = PC98_VRAM_AT(VRAM_SEGMENT_GREEN);
PC98VramPlane near VRAM_PLANE_E = PC98_VRAM_AT(VRAM_SEGMENT_EXTENDED);

typedef char main_vram_pointer_size[(sizeof(PC98VramPlane) == 4) ? 1 : -1];
typedef char main_four_planes_size[(4 * sizeof(PC98VramPlane) == 16) ? 1 : -1];
