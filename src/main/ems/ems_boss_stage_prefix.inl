// Four true original-order MAIN functions; the 803-byte initializer is the new source owner.
// The identical default option was already selected before original forward declarations.
// Declare the real empty compiler segments before the original SHARED externs.
#pragma codeseg RUNTIME_MAIN01_TEXT main_01
#pragma codeseg SESSION_MAIN01_TEXT main_01
#pragma codeseg SESSION_INIT_TEXT main_01
#pragma codeseg STAGE_SESSION_TEXT main_01
// No generated SHARED SEGDEF in this aggregate; foreign binder owns the genuine ungrouped frame.
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

// Natural new-game initialization adapted from maintained TH04 core source.
// TH05's four-character and rank/demo behavior follows the actual target.

#include "src/main/runtime/gameplay_session_init.hpp"
#pragma codeseg DEMO_TEXT main_01

#include "src/main/runtime/gameplay_session_init_body.inl"

// Natural stage entry adapted from maintained TH04 session_init.cpp,
// with TH05's actual debug/demo, four-character and resource behavior.

#include "src/main/runtime/stage_session_context.hpp"
#pragma codeseg DEMO_TEXT main_01
// Keep all canonical object types complete before compiler table alignment.
#pragma option -a2

// Real PC-98 graphics-page hardware boundary, as in the maintained master API.
#define graph_accesspage(page) outportb(0xA6, (page))
#define graph_showpage(page) outportb(0xA4, (page))

#include "src/main/runtime/stage_session_init_body.inl"
