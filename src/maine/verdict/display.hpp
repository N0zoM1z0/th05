// Verdict comment lines and the per-stage score tally shown in the staff roll.
#ifndef TH05_MAINE_VERDICT_DISPLAY_HPP
#define TH05_MAINE_VERDICT_DISPLAY_HPP
#include "src/maine/verdict/format.hpp"
extern screen_x_t verdict_text_left;
extern screen_y_t verdict_text_top;
extern vc2 verdict_comment_color;
// Two 30-byte records read from _ude.txt by verdict_main().
extern shiftjis_t near verdict_comments[2][30];
extern const shiftjis_t near verdict_stage_1_title[];
extern const shiftjis_t near verdict_stage_2_title[];
extern const shiftjis_t near verdict_stage_3_title[];
extern const shiftjis_t near verdict_stage_4_title[];
extern const shiftjis_t near verdict_stage_5_title[];
extern const shiftjis_t near verdict_stage_6_title[];
extern const shiftjis_t near verdict_final_score_title[];
#ifdef TH05_VERDICT_FULL_FAMILY
#pragma codeseg VERDICT_FULL_TEXT group_01
#else
#pragma codeseg VERDICT_COMMENT_TEXT group_01
#endif
void near verdict_comments_put(void);
#ifdef TH05_VERDICT_FULL_FAMILY
#pragma codeseg VERDICT_FULL_TEXT group_01
#else
#pragma codeseg VERDICT_SCORES_TEXT group_01
#endif
void near verdict_stage_scores_put(void);
#endif
