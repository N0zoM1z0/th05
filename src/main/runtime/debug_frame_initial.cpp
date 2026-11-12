// Original first two MAIN _DATA bytes; code consumers determine their roles.
// ReC98 th05_main.asm opens DATA with two explicit `db 0` values.
#pragma option -zCDEBUG_FRAME_INIT_TEXT -zPmain_01
#include "src/main/hud/resident.hpp"

signed char debug_frame_step = 0;
bool debug_frame_step_enabled = false;

typedef char debug_frame_step_is_byte[(sizeof(debug_frame_step) == 1) ? 1 : -1];
typedef char debug_frame_enabled_is_byte[(sizeof(debug_frame_step_enabled) == 1) ? 1 : -1];
