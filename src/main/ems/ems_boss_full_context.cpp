// One translation unit holding the 3,226 bytes of MAIN code from main() to
// eyecatch_animate(), in their original order. ems_preload_boss_faceset()
// compiles to the right bytes on its own, but Turbo C++ only writes its
// four fixups in the original order [71,24,133,114] when everything before
// it in this code segment is compiled together with it: the amount of code
// before a function decides where the compiler splits its LEDATA and FIXUPP
// records.
//
// The function bodies in the two .inl files are copies of the ones in
// runtime/, demo/ and ems/ems.cpp.
#pragma option -zCDEMO_TEXT
#include "src/shared/abi.hpp"
// SHARED is a separate, ungrouped code segment. The link scaffold provides
// it; this file must not create a SHARED segment of its own.
// A function's first declaration fixes its code segment. Declare the later
// functions here, in DEMO_TEXT, before the included headers declare them
// under other segment names.
#pragma codeseg DEMO_TEXT main_01
void near stage_runtime_init(void);
extern "C" void near stage_session_free(void);
extern "C" int near pause(void);
void near demo_load(void);
void near DemoPlay(void);
void near ems_allocate_and_preload_eyecatch(void);
void near bomb_bg_load__ems_preload_playchar_cdgs(void);
void pascal near ems_preload_boss_faceset(const char far *filename);
void near eyecatch_animate(void);

// 1,826 bytes: main(), gameplay_loop(), gameplay_session_init() and
// stage_session_init(). Then 1,400 bytes: stage_runtime_init(),
// stage_session_free(), pause(), demo_load(), DemoPlay() and the EMS code.
#include "src/main/ems/ems_boss_stage_prefix.inl"
#include "src/main/ems/ems_boss_lifecycle_prefix.inl"
