// Natural reconstruction from the original TH05 MAINE line-animation CFG.
// Pinned ReC98 th05/end/allcast.cpp supplies the surrounding state/caller
// semantics; th05_maine.asm supplies disassembly evidence, not a source body.
#pragma option -zCALLCAST_LINES_TEXT -zPgroup_01
#include "src/maine/allcast/lines.hpp"

static const screen_x_t ALLCAST_LINE_LEFT = 64;
static const int ALLCAST_LINE_SPACING = 32;
static const vc2 ALLCAST_LINE_COLOR = 15;

bool near screen_line_next_animate(void)
{
    const shiftjis_t far *text = LINES[line_id_total];
    screen_y_t top = ((RES_Y / 2) - (16 / 2))
        - ((allcast_lines_per_screen[loaded_screen_id - 1] - 1)
            * (ALLCAST_LINE_SPACING / 2))
        + (line_id_on_screen * ALLCAST_LINE_SPACING);

    graph_putsa_fx_func = FX_MASK_4;
    for(int i = 0; i < FX_MASK; i++) {
        graph_putsa_fx(ALLCAST_LINE_LEFT, top, ALLCAST_LINE_COLOR, text);
        wait_flip_and_check_measure_target();
        graph_putsa_fx(ALLCAST_LINE_LEFT, top, ALLCAST_LINE_COLOR, text);
        wait_flip_and_check_measure_target();
        graph_putsa_fx_func--;
    }

    graph_putsa_fx_func = FX_WEIGHT_BOLD;
    graph_putsa_fx(ALLCAST_LINE_LEFT, top, ALLCAST_LINE_COLOR, text);
    wait_flip_and_check_measure_target();
    graph_putsa_fx(ALLCAST_LINE_LEFT, top, ALLCAST_LINE_COLOR, text);
    wait_flip_and_check_measure_target();

    line_id_total++;
    line_id_on_screen++;
    if(line_id_on_screen >= allcast_lines_per_screen[loaded_screen_id - 1]) {
        line_id_on_screen = 0;
        return true;
    }
    return false;
}
