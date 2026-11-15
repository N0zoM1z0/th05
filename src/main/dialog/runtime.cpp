// Box wipe/fade, command interpreter and script loop in one translation
// unit, without the graphics helpers that precede them. Like opcode.cpp,
// this build misses dialog_op()'s switch-table alignment byte; see
// opcode_full_context.cpp.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <string.h>
#include "src/main/dialog/runtime.hpp"

#include "src/main/dialog/box.inl"

#pragma option -a2
#include "src/main/dialog/opcode.inl"

#include "src/main/dialog/run.inl"
