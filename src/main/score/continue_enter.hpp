// High score entry on continue. The insertion itself is in continue_raw.cpp.
#ifndef TH05_MAIN_SCORE_CONTINUE_ENTER_HPP
#define TH05_MAIN_SCORE_CONTINUE_ENTER_HPP
#include "src/shared/abi.hpp"
extern unsigned char turbo_mode;

#pragma codeseg SCORE_TEXT main_01
void near hiscore_continue_enter_raw(void);
#pragma codeseg SCORE_ENTRY_TEXT main_01
void near hiscore_continue_enter(void);
#pragma codeseg
#endif
