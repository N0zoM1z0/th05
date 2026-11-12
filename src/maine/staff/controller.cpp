// Complete natural TH05 staff-roll controller, original [E422,E801).
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47 th05_maine.asm
// supplies disassembly corroboration; bitmap device kernels remain external.
#pragma option -zCSTAFF_CONTROL_TEXT -zPgroup_01
#include "src/maine/staff/state_publics.h"
#include "src/maine/staff/controller.hpp"
#pragma codeseg STAFF_CONTROL_TEXT group_01

#include "src/maine/staff/controller_body.inl"
