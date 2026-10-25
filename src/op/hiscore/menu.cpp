// Standalone complete menu; actual near renderer and state remain foreign.
#pragma option -zCSCORE_MENU_TEXT -zPop_01
#include <dos.h>
#include "src/op/hiscore/view.hpp"
#include "src/op/hiscore/files.hpp"
#pragma codeseg SCORE_MENU_TEXT op_01
void near rank_render(void);
#include "src/op/hiscore/regist_view_menu.inl"
