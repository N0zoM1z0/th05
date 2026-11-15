// Standalone build of glyphball_spawn(). Not used by any unit: on its own,
// the function comes out one byte short. motion.cpp builds the matching one.
#pragma option -zCREG_SPAWN_TEXT -zPGROUP_01
#include "src/maine/registration/spawn.hpp"
#pragma codeseg REG_SPAWN_TEXT GROUP_01

#include "src/maine/registration/spawn.inl"
