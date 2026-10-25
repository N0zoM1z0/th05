// Coherent stage-two background owner, sharing the two maintained bodies.
#pragma option -zCSTAGE2_TEXT -zPmain_01
#include "src/main/stage/background2.hpp"

#define TH05_STAGE2_BG_COMBINED 1
#include "src/main/stage/particle_init.cpp"
#include "src/main/stage/stage2_update.cpp"
#undef TH05_STAGE2_BG_COMBINED
