// Natural complete commentary renderer, original D16F..D1B1.
#pragma option -zCVERDICT_COMMENT_TEXT -zPgroup_01
#include "src/maine/verdict/display.hpp"
#pragma codeseg VERDICT_COMMENT_TEXT group_01
void near verdict_comments_put(void)
{
    if(verdict_comments[0][0]) {
        graph_putsa_fx(verdict_text_left + 48, verdict_text_top + 296,
            verdict_comment_color, verdict_comments[0]);
        graph_putsa_fx(verdict_text_left + 48, verdict_text_top + 312,
            verdict_comment_color, verdict_comments[1]);
    }
}
