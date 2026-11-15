// playfield_copy_front_to_back(), the EGC copy of the whole playfield from
// the front to the back VRAM page, built on its own.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
#include "src/main/dialog/interpage_copy_body.inl"
