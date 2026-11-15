// The first two bytes of MAIN's data segment: the debug-mode fast-forward
// state used by gameplay_loop(), and whether Q toggles it (set by
// stage_session_init() in debug mode).
#pragma option -zCDEBUG_FRAME_INIT_TEXT -zPmain_01
#include "src/main/hud/resident.hpp"

signed char debug_frame_step = 0;
bool debug_frame_step_enabled = false;

typedef char debug_frame_step_is_byte[(sizeof(debug_frame_step) == 1) ? 1 : -1];
typedef char debug_frame_enabled_is_byte[(sizeof(debug_frame_step_enabled) == 1) ? 1 : -1];
