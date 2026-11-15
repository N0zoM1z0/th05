// dialog_face_unput_8(), the EGC copy that restores a face area from the
// other VRAM page, built on its own.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
#include "src/main/dialog/face_unput_body.inl"
