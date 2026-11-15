// game_exit_to_dos(): game_exit(), then back to DOS (ReC98's TH02 wrapper).
#pragma option -zCEXIT_DOS_TEXT -zPshared_exit
#include "src/shared/core/game_exit.hpp"
#pragma codeseg EXIT_DOS_TEXT shared_exit
#pragma samecodeseg game_exit

void far game_exit_to_dos(void)
{
    game_exit();
    key_beep_on();
    text_systemline_show();
    text_cursor_show();
}
