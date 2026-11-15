// hiscore_continue_enter(): on a continue, tries to enter the current score
// into the high score list under the name CONTINUE. This only happens in
// turbo mode. Unlike TH04, the list is not reloaded from the score file first.
#pragma option -zCSCORE_ENTRY_TEXT -zPmain_01 -k-
#include "src/main/score/continue_enter.hpp"
#pragma codeseg SCORE_ENTRY_TEXT main_01

void near hiscore_continue_enter(void)
{
    if(turbo_mode) {
        hiscore_continue_enter_raw();
    }
}
