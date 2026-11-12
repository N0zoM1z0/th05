// The original STD script allocation begins with no resident segment.
// ReC98 th04/formats/std[data].asm: `_std_seg dw 0`.
#pragma option -zCSTD_SEG_INIT_TEXT -zPmain_01
#include "src/shared/abi.hpp"

unsigned char __seg *std_seg = 0;
typedef char std_startup_handle_is_word[(sizeof(std_seg) == 2) ? 1 : -1];
