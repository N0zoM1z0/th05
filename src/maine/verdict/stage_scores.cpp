// Natural complete six-stage and final Score8 display, original D21D..D31F.
#pragma option -zCVERDICT_SCORES_TEXT -zPgroup_01
#include "src/maine/verdict/display.hpp"
#pragma codeseg VERDICT_SCORES_TEXT group_01
void near verdict_stage_scores_put(void)
{
    screen_x_t score_left;
    int stage;
    screen_y_t score_top;

    graph_putsa_fx(verdict_text_left, verdict_text_top + 64,
        verdict_text_color, verdict_stage_1_title);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 96,
        verdict_text_color, verdict_stage_2_title);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 128,
        verdict_text_color, verdict_stage_3_title);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 160,
        verdict_text_color, verdict_stage_4_title);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 192,
        verdict_text_color, verdict_stage_5_title);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 224,
        verdict_text_color, verdict_stage_6_title);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 288,
        verdict_text_color, verdict_final_score_title);

    score_left = verdict_text_left + 128;
    stage = 0;
    score_top = verdict_text_top + 64;
    for(; stage < MAIN_STAGE_COUNT; stage++, score_top += 32) {
        verdict_score_put(score_left, score_top, resident->stage_score[stage]);
    }
    verdict_score_put(score_left, verdict_text_top + 288, resident->score_last);
}
