// regist_view_menu() on its own. In view.cpp, the compiler splits the object
// record in the middle of this function, which reorders its relocations; this
// translation unit emits them in the original order. rank_render() and the
// viewer state live in view.cpp.
#pragma option -zCSCORE_MENU_TEXT -zPop_01
#include <dos.h>
#include "src/op/hiscore/view.hpp"
#include "src/op/hiscore/files.hpp"
#pragma codeseg SCORE_MENU_TEXT op_01
void near rank_render(void);
#include "src/op/hiscore/regist_view_menu.inl"
