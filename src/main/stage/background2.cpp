// Stage 2 background: the particle initializer and the per-frame update in one
// translation unit, as they are laid out in the original code segment.
// Not part of the build; the two functions are compiled from their own files.
#pragma option -zCSTAGE2_TEXT -zPmain_01
#include "src/main/stage/background2.hpp"

#define TH05_STAGE2_BG_COMBINED 1
#include "src/main/stage/particle_init.cpp"
#include "src/main/stage/stage2_update.cpp"
#undef TH05_STAGE2_BG_COMBINED
