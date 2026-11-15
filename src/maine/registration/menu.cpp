// Standalone build of regist_menu(). Not used by any unit: the bytes match,
// but the relocations only come out in the original order in full_context.cpp.
#pragma option -zCREG_MENU_TEXT -zPGROUP_01
#include "src/maine/registration/menu.hpp"
#pragma codeseg REG_MENU_TEXT GROUP_01

#include "src/maine/registration/menu.inl"
