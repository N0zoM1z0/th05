// First part of the combined unit in ems_boss_full_context.cpp: main(),
// gameplay_loop(), gameplay_session_init() and stage_session_init().
//
// Name these (empty) code segments before the SHARED externs; the link
// scaffold expects their segment definitions in this order.
#pragma codeseg RUNTIME_MAIN01_TEXT main_01
#pragma codeseg SESSION_MAIN01_TEXT main_01
#pragma codeseg SESSION_INIT_TEXT main_01
#pragma codeseg STAGE_SESSION_TEXT main_01
// (SHARED itself comes from the link scaffold.)
#pragma codeseg RUNTIME_MAIN03_TEXT main_03
#pragma codeseg BULLET_A_TEXT main_03
#pragma codeseg STAGE_SESSION_MAIN03_CONTEXT main_03
#pragma codeseg DEMO_TEXT main_01
void main(void);
void near gameplay_loop(void);
void near gameplay_session_init(void);
void near stage_session_init(void);
#define TH05_RUNTIME_COMBINED 1
#include "src/main/runtime/entry.cpp"
#include "src/main/runtime/gameplay_loop.cpp"
#undef TH05_RUNTIME_COMBINED

// gameplay_session_init(): TH04's new-game setup, with TH05's four
// characters and rank/demo handling.

#include "src/main/runtime/gameplay_session_init.hpp"
#pragma codeseg DEMO_TEXT main_01

#include "src/main/runtime/gameplay_session_init_body.inl"

// stage_session_init(): TH04's session_init.cpp, with TH05's debug/demo,
// character and resource handling.

#include "src/main/runtime/stage_session_context.hpp"
#pragma codeseg DEMO_TEXT main_01
// Word-aligns the switch jump tables, after all struct definitions so that
// their layout is unaffected.
#pragma option -a2

// master.lib's VRAM page selection macros
#define graph_accesspage(page) outportb(0xA6, (page))
#define graph_showpage(page) outportb(0xA4, (page))

#include "src/main/runtime/stage_session_init_body.inl"
