// Native 88-byte PC-98 dialog tile-box drawing, source-backed by ReC98 shared.cpp.
// The original GRCG and register-directed row loop use the actual 16-bit ABI.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
#include "src/main/dialog/box_put_body.inl"
