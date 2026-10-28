// Natural TH05 dialog boxes/commands/run loop from ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47. The three compiler-body ASM
// rendering/copy helpers and the separate animation/EMS owner stay foreign.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <string.h>
#include "src/main/dialog/runtime.hpp"

#include "src/main/dialog/box.inl"

#pragma option -a2
#include "src/main/dialog/opcode.inl"

#include "src/main/dialog/run.inl"
