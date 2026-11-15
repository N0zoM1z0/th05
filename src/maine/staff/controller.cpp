// Standalone build of staffroll_animate(). Its bytes match, but its
// relocations come out in a different order; the matching build is
// staff_complete_context.cpp.
#pragma option -zCSTAFF_CONTROL_TEXT -zPgroup_01
#include "src/maine/staff/state_publics.h"
#include "src/maine/staff/controller.hpp"
#pragma codeseg STAFF_CONTROL_TEXT group_01

#include "src/maine/staff/controller_body.inl"
