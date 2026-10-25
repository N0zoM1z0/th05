// Full canonical resident and eight-byte score records, never an opaque view.
#ifndef TH05_HUD_SCORE_RESET_HPP
#define TH05_HUD_SCORE_RESET_HPP
#include "src/main/hud/resident.hpp"

extern score_lebcd_t score;
extern unsigned long score_delta;
extern unsigned long score_delta_frame;
extern unsigned char hiscore_popup_shown;
#pragma codeseg SCORE_RESET_TEXT main_01
void near score_reset(void);
#pragma codeseg

typedef char reset_score_is_8[(sizeof(score) == 8) ? 1 : -1];
typedef char reset_delta_is_4[(sizeof(score_delta) == 4) ? 1 : -1];
typedef char reset_frame_delta_is_4[(sizeof(score_delta_frame) == 4) ? 1 : -1];
#endif
