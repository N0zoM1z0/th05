// Complete dialog command interpreter, independent of box/run producers.
#pragma option -zCDIALOG_OP_TEXT -zPmain_01
#include <string.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_OP_TEXT main_01
#pragma option -a2
#include "src/main/dialog/opcode.inl"
