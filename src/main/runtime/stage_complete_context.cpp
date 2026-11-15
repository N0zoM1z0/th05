// The MAIN module that starts the game: main(), gameplay_loop(),
// gameplay_session_init() and stage_session_init(), in their original order.
//
// One compiler translation unit reproduces one original module, so the four
// function bodies are #included in the order they appear in MAIN.EXE.
// stage_session_init() only comes out right in this context:
// - Its switch tables are word-aligned. Compiled alone, the function starts at
//   an even offset and needs no alignment byte before the tables; after the
//   three preceding functions it starts at an odd offset, and the compiler
//   emits the original zero byte.
// - With main() included first, the fixups of stage_session_init() come out
//   in the original order. Without it, the one at +56 is emitted first
//   instead of last.
#pragma option -zCDEMO_TEXT
// These empty segment declarations reproduce the original segment order:
// four main_01 segments, then the ungrouped SHARED segment, then three
// main_03 segments. Otherwise SHARED gets absorbed into a neighboring group,
// and the CS operands of far calls into it change.
#pragma codeseg RUNTIME_MAIN01_TEXT main_01
#pragma codeseg SESSION_MAIN01_TEXT main_01
#pragma codeseg SESSION_INIT_TEXT main_01
#pragma codeseg STAGE_SESSION_TEXT main_01
#pragma codeseg SHARED
#pragma codeseg RUNTIME_MAIN03_TEXT main_03
#pragma codeseg BULLET_A_TEXT main_03
#pragma codeseg STAGE_SESSION_MAIN03_CONTEXT main_03
#pragma codeseg DEMO_TEXT main_01
// Borland binds a function to the code segment that is active at its first
// declaration. These prototypes come before the headers, which declare some
// of the same functions in other segments, so all four belong to DEMO_TEXT.
void main(void);
void near gameplay_loop(void);
void near gameplay_session_init(void);
void near stage_session_init(void);
#define TH05_RUNTIME_COMBINED 1
#include "src/main/runtime/entry.cpp"
#include "src/main/runtime/gameplay_loop.cpp"
#undef TH05_RUNTIME_COMBINED

// New-game initialization.

#include "src/main/runtime/gameplay_session_init.hpp"
#pragma codeseg DEMO_TEXT main_01

#include "src/main/runtime/gameplay_session_init_body.inl"

// Stage entry. stage_session_context.hpp is stage_session_init.hpp without
// the snd_load_func_t enum, which main.hpp already defined above.

#include "src/main/runtime/stage_session_context.hpp"
#pragma codeseg DEMO_TEXT main_01
// Word alignment for the switch tables in stage_session_init(). It has to
// come after the headers, so that it doesn't change any struct layout.
#pragma option -a2

// PC-98 graphics page selection: port A6 = accessed page, A4 = shown page.
#define graph_accesspage(page) outportb(0xA6, (page))
#define graph_showpage(page) outportb(0xA4, (page))

#include "src/main/runtime/stage_session_init_body.inl"
