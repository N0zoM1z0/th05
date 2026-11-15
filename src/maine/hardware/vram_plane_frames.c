/* Far pointers to the four PC-98 graphics planes (B, R, G, E at segments
 * A800h, B000h, B800h and E000h), as in ReC98's
 * th05/hardware/vram_planes[data].asm. The original also had a _VRAM_PLANE
 * alias for the first pointer; it is not declared here. */
#pragma option -zCVRAM_PLANES_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error This file is compiled as C
#endif
#include "src/shared/hardware/vram_plane_frames.h"

PC98VramPlane near VRAM_PLANE_B = PC98_VRAM_AT(VRAM_SEGMENT_BLUE);
PC98VramPlane near VRAM_PLANE_R = PC98_VRAM_AT(VRAM_SEGMENT_RED);
PC98VramPlane near VRAM_PLANE_G = PC98_VRAM_AT(VRAM_SEGMENT_GREEN);
PC98VramPlane near VRAM_PLANE_E = PC98_VRAM_AT(VRAM_SEGMENT_EXTENDED);

typedef char vram_far_pointer_size[(sizeof(PC98VramPlane) == 4) ? 1 : -1];
typedef char vram_four_plane_bytes[(4 * sizeof(PC98VramPlane) == 16) ? 1 : -1];
