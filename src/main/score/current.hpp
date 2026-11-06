// MAIN's raw DOS file interface and unchanged complete TH05 score records.
#ifndef TH05_MAIN_SCORE_CURRENT_HPP
#define TH05_MAIN_SCORE_CURRENT_HPP
#include <dos.h>
#pragma codeseg SCORE_CODE_TEXT main_01
unsigned char pascal near scoredat_decode(void);
void pascal near scoredat_encode(void);
#pragma codeseg SHARED
#include "src/op/hiscore/view.hpp"
extern playchar_t playchar;
extern const char near main_score_filename[11];
#pragma codeseg SCORE_IO_TEXT main_01
void near scoredat_load_for_cur(void);
void near scoredat_save_cur(void);
#endif
