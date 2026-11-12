/* OP's distinct four initialized PC-98 RGB+extended video far pointers. */
#pragma option -zCVRAM_PLANES_OP_TEXT -zPop_01
#ifdef __cplusplus
#error Hardware video address DATA must use C initialization
#endif
#include "src/shared/hardware/vram_plane_frames.h"

PC98VramPlane near VRAM_PLANE_B = PC98_VRAM_AT(VRAM_SEGMENT_BLUE);
PC98VramPlane near VRAM_PLANE_R = PC98_VRAM_AT(VRAM_SEGMENT_RED);
PC98VramPlane near VRAM_PLANE_G = PC98_VRAM_AT(VRAM_SEGMENT_GREEN);
PC98VramPlane near VRAM_PLANE_E = PC98_VRAM_AT(VRAM_SEGMENT_EXTENDED);

typedef char op_vram_ptr_is_four[(sizeof(PC98VramPlane) == 4) ? 1 : -1];
typedef char op_vram_bank_is_sixteen[(4 * sizeof(PC98VramPlane) == 16) ? 1 : -1];
