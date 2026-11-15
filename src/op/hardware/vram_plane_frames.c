/* OP.EXE's far pointers to the four PC-98 VRAM planes (B, R, G, E), from
 * master.lib's grp[data].asm. MAINE.EXE has its own copy. */
#pragma option -zCVRAM_PLANES_OP_TEXT -zPop_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/shared/hardware/vram_plane_frames.h"

PC98VramPlane near VRAM_PLANE_B = PC98_VRAM_AT(VRAM_SEGMENT_BLUE);
PC98VramPlane near VRAM_PLANE_R = PC98_VRAM_AT(VRAM_SEGMENT_RED);
PC98VramPlane near VRAM_PLANE_G = PC98_VRAM_AT(VRAM_SEGMENT_GREEN);
PC98VramPlane near VRAM_PLANE_E = PC98_VRAM_AT(VRAM_SEGMENT_EXTENDED);
