// The whole dialog code segment from std_update_done() to dialog_run(), in
// original order. dialog_op() only gets the alignment byte before its switch
// table when everything before it is compiled in the same translation unit.
// Each body is also built on its own through its own .cpp file.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include <string.h>
#include "src/main/dialog/runtime.hpp"
#define TH05_DIALOG_OPCODE_FULL_CONTEXT 1
#include "src/main/dialog/boss_transition.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
#include "src/main/dialog/boss_transition_body.inl"
#include "src/main/dialog/box_put_body.inl"
#include "src/main/dialog/interpage_copy_body.inl"
#include "src/main/dialog/face_unput_body.inl"
#include "src/main/dialog/box.inl"
#pragma option -a2
#include "src/main/dialog/opcode.inl"
#include "src/main/dialog/run.inl"
