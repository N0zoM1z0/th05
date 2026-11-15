// Sara's foreground renderer compiled on its own. The order of the local
// variable declarations in foreground.inl decides which one Turbo C++ puts
// into DI; left, top, patnum matches the original.
#pragma option -zCBOSS_FG_TEXT -zPmain_01
#include "src/main/boss/foreground.hpp"
#pragma codeseg BOSS_FG_TEXT main_01
#include "src/main/boss/sara/foreground.inl"
