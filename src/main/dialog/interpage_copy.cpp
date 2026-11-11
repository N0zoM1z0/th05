// Complete original 56-byte EGC hardware copy of the 384x368 playfield.
// ReC98 preserves the page-select, register and 16-bit row-loop semantics.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
#include "src/main/dialog/interpage_copy_body.inl"
