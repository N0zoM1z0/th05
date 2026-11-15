// Standalone build of glyphball_spawn() and glyphballs_update(), which are
// adjacent in the original (see full_context.cpp).
#pragma option -zCREG_MOTION_TEXT -zPGROUP_01
#include "src/maine/registration/motion.hpp"
#pragma codeseg REG_MOTION_TEXT GROUP_01
#pragma option -a
#include "src/maine/registration/spawn.inl"
#include "src/maine/registration/update.inl"
