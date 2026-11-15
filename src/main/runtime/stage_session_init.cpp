// stage_session_init() on its own. In MAIN, it is part of the module built
// by stage_complete_context.cpp; built alone, it lacks the alignment byte
// before its switch tables (see there).
#pragma option -zCSTAGE_SESSION_TEXT -zPmain_01
#include "src/main/runtime/stage_session_init.hpp"
#pragma codeseg STAGE_SESSION_TEXT main_01
// Word alignment for the switch tables, after all struct definitions.
#pragma option -a2

// PC-98 graphics page selection: port A6 = accessed page, A4 = shown page.
#define graph_accesspage(page) outportb(0xA6, (page))
#define graph_showpage(page) outportb(0xA4, (page))

#include "src/main/runtime/stage_session_init_body.inl"
