/* Far pointers to the four PC-98 VRAM planes (blue A800, red B000, green
 * B800, extended E000). OP and MAINE have their own copies. */
#pragma option -zCMAIN_VRAM_PLANES_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/shared/hardware/vram_plane_frames.h"

PC98VramPlane near VRAM_PLANE_B = PC98_VRAM_AT(VRAM_SEGMENT_BLUE);
PC98VramPlane near VRAM_PLANE_R = PC98_VRAM_AT(VRAM_SEGMENT_RED);
PC98VramPlane near VRAM_PLANE_G = PC98_VRAM_AT(VRAM_SEGMENT_GREEN);
PC98VramPlane near VRAM_PLANE_E = PC98_VRAM_AT(VRAM_SEGMENT_EXTENDED);

typedef char main_vram_pointer_size[(sizeof(PC98VramPlane) == 4) ? 1 : -1];
typedef char main_four_planes_size[(4 * sizeof(PC98VramPlane) == 16) ? 1 : -1];
