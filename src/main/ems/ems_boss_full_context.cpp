// Original first declarations bind every genuine MAIN01 lifecycle callback
// to the one physical source CODE segment before any nested header changes.
#pragma option -zCDEMO_TEXT
#include "src/shared/abi.hpp"
// The original SHARED section is a separate ungrouped code frame.
// No generated SHARED SEGDEF in this aggregate; foreign binder owns the genuine ungrouped frame.
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

// The actual original 1826-byte MAIN entry+loop+game+stage initialization
// directly precedes the genuine 1400-byte runtime+session+demo+EMS body.
// The full 3226-byte original code is compiled from complete real C++ function bodies.
#include "src/main/ems/ems_boss_stage_prefix.inl"
#include "src/main/ems/ems_boss_lifecycle_prefix.inl"
