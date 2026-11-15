// Shinki's 32x32 ball update, compiled on its own. The body lives in
// balls_update_body.inl, which shinki.cpp also includes.
#pragma option -zCB6_BALLS_TEXT -zPmain_03
#include "src/main/boss/shinki/shinki.hpp"
#pragma codeseg B6_BALLS_TEXT main_03
#include "src/main/boss/shinki/balls_update_body.inl"
