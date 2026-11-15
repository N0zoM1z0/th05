// Standalone build of glyphballs_update(). Not used by any unit: the bytes
// match, but the relocation order only does in motion.cpp.
#pragma option -zCREG_UPDATE_TEXT -zPGROUP_01
#include "src/maine/registration/update.hpp"
#pragma codeseg REG_UPDATE_TEXT GROUP_01
#pragma option -a

#include "src/maine/registration/update.inl"
