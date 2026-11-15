// All Cast credit line rendering: the line table and the state it shares with
// allcast.cpp.
#ifndef TH05_ALLCAST_LINES_HPP
#define TH05_ALLCAST_LINES_HPP

#pragma codeseg MAINE_01_TEXT group_01
#include "src/maine/allcast/allcast.hpp"
bool near wait_flip_and_check_measure_target(void);

typedef uint8_t shiftjis_t;

// Same definition as in src/maine/verdict/main.hpp. The FORCE_INT16 member
// keeps the enum word-sized.
enum graph_putsa_fx_func_t {
    FX_WEIGHT_NORMAL = 0, FX_WEIGHT_HEAVY = 1,
    FX_WEIGHT_BOLD = 2, FX_WEIGHT_BLACK = 3,
    FX_MASK, FX_MASK_1 = FX_MASK, FX_MASK_2, FX_MASK_3, FX_MASK_4, FX_MASK_END,
    _graph_putsa_fx_func_FORCE_INT16 = 0x7FFF
};
extern graph_putsa_fx_func_t graph_putsa_fx_func;

extern int loaded_screen_id;
extern int line_id_total;
extern int line_id_on_screen;
extern const shiftjis_t far *LINES[47];

// Number of credit lines on each of the seven screens. ReC98's disassembly
// labels this table one word earlier, on the segment of the last LINES
// pointer, which matches indexing it with the 1-based [loaded_screen_id].
extern int allcast_lines_per_screen[7];

#pragma codeseg SHARED
extern "C" void pascal far graph_putsa_fx(screen_x_t left, screen_y_t top,
    vc2 color, const shiftjis_t far *text);

#pragma codeseg ALLCAST_LINES_TEXT group_01
bool near screen_line_next_animate(void);

#endif
