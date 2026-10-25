// Natural TH04 verdict animation donor with actual TH05 display/wait steps.
#pragma option -zCVERDICT_ANIMATE_TEXT -zPgroup_01
#include "src/maine/verdict/animate.hpp"
#pragma codeseg VERDICT_ANIMATE_TEXT group_01
void near verdict_animate(void)
{
    PaletteTone = 0;
    palette_show();
    verdict_graph_accesspage(1);
    pi_load(0, verdict_picture_filename);
    pi_palette_apply(0);
    pi_put_8(0, 0, 0);
    pi_free(0);
    graph_copy_page(0);
    palette_black_in(4);
    verdict_graph_accesspage(0);
    verdict_graph_showpage(0);
    verdict_main();
    frame_delay(64);
    verdict_comments_put();
    input_wait_for_change(0);
    palette_black_out(2);
}
