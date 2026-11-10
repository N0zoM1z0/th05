// Natural stage entry adapted from maintained TH04 session_init.cpp,
// with TH05's actual debug/demo, four-character and resource behavior.
#pragma option -zCSTAGE_SESSION_TEXT -zPmain_01
#include "src/main/runtime/stage_session_init.hpp"
#pragma codeseg STAGE_SESSION_TEXT main_01
// Keep all canonical object types complete before compiler table alignment.
#pragma option -a2

// Real PC-98 graphics-page hardware boundary, as in the maintained master API.
#define graph_accesspage(page) outportb(0xA6, (page))
#define graph_showpage(page) outportb(0xA4, (page))

#include "src/main/runtime/stage_session_init_body.inl"
