// TH04 entry condition, with TH05's separately loaded in-memory score section.
#pragma option -zCSCORE_ENTRY_TEXT -zPmain_01 -k-
#include "src/main/score/continue_enter.hpp"
#pragma codeseg SCORE_ENTRY_TEXT main_01

void near hiscore_continue_enter(void)
{
    if(turbo_mode) {
        hiscore_continue_enter_raw();
    }
}
