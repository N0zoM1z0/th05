// Natural TH04 maintained stage/session_init.cpp cleanup and menu semantics,
// with TH05's actual slot ranges, held-input service and release condition.
#pragma option -zCSESSION_END_TEXT -zPmain_01
#include "src/main/runtime/session_end.hpp"
#pragma codeseg SESSION_END_TEXT main_01

extern "C" void near stage_session_free(void)
{
    bb_boss_free();
    dialog_free();
    std_free();
    map_free();
    super_clean(STAGE_PATTERN_FIRST, STAGE_PATTERN_END);
    for(int i = STAGE_CDG_FIRST; i < STAGE_CDG_END; i++) {
        cdg_free(i);
    }
}

extern "C" int near pause(void)
{
    int selected = 0;
    while(key_det != 0) {
        input_reset_sense_held();
    }
    gaiji_putsa(26, 12, gsCHUUDAN, PAUSE_TX_YELLOW);
    gaiji_putsa(26, 14, gsSAIKAI, PAUSE_TX_WHITE + PAUSE_TX_UNDERLINE);
    gaiji_putsa(26, 15, gsSHUURYOU, PAUSE_TX_YELLOW);
    while(1) {
        input_wait_for_change(0);
        if((key_det & PAUSE_INPUT_UP) || (key_det & PAUSE_INPUT_DOWN)) {
            selected = 1 - selected;
            if(selected == 0) {
                gaiji_putsa(26, 14, gsSAIKAI, PAUSE_TX_WHITE + PAUSE_TX_UNDERLINE);
                gaiji_putsa(26, 15, gsSHUURYOU, PAUSE_TX_YELLOW);
            } else {
                gaiji_putsa(26, 14, gsSAIKAI, PAUSE_TX_YELLOW);
                gaiji_putsa(26, 15, gsSHUURYOU, PAUSE_TX_WHITE + PAUSE_TX_UNDERLINE);
            }
        }
        if(key_det & PAUSE_INPUT_Q) {
            return 1;
        }
        if(key_det & PAUSE_INPUT_CANCEL) {
            selected = 0;
            break;
        }
        if((key_det & PAUSE_INPUT_SHOT) || (key_det & PAUSE_INPUT_OK)) {
            break;
        }
    }
    // TH05 waits only for CANCEL release here; other held inputs survive.
    while(key_det & PAUSE_INPUT_CANCEL) {
        input_reset_sense_held();
    }
    text_putsa(26, 12, aGAME_PAUSE_SPACES_1, PAUSE_TX_WHITE);
    text_putsa(26, 14, aGAME_PAUSE_SPACES_2, PAUSE_TX_WHITE);
    text_putsa(26, 15, aGAME_PAUSE_SPACES_3, PAUSE_TX_WHITE);
    return selected;
}
