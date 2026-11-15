// dialog_op() on its own. Built like this, the compiler leaves out the
// alignment byte before the command switch table, so the exact build uses
// opcode_full_context.cpp instead.
#pragma option -zCDIALOG_OP_TEXT -zPmain_01
#include <string.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_OP_TEXT main_01
#pragma option -a2
#include "src/main/dialog/opcode.inl"
