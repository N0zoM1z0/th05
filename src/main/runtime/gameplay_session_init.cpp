// gameplay_session_init() on its own. In MAIN, it is part of the module
// built by stage_complete_context.cpp.
#pragma option -zCSESSION_INIT_TEXT -zPmain_01
#include "src/main/runtime/gameplay_session_init.hpp"
#pragma codeseg SESSION_INIT_TEXT main_01

#include "src/main/runtime/gameplay_session_init_body.inl"
