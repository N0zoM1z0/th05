// main() and gameplay_loop() as one translation unit, without the two
// initializers that follow them in MAIN. stage_complete_context.cpp builds
// the whole original module.
#pragma option -zCDEMO_TEXT -zPmain_01
#define TH05_RUNTIME_COMBINED 1
#include "src/main/runtime/entry.cpp"
#include "src/main/runtime/gameplay_loop.cpp"
#undef TH05_RUNTIME_COMBINED
