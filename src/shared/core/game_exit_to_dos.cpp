// Natural ReC98 TH02 wrapper, with the real same-CS foreign cleanup call.
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
