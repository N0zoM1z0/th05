// dialog_box_put(), the GRCG blitter for one fade-in stage of a dialog box,
// built on its own.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
#include "src/main/dialog/box_put_body.inl"
