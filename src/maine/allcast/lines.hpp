// TH05 all-cast line animation and genuine foreign storage/interfaces.
#ifndef TH05_ALLCAST_LINES_HPP
#define TH05_ALLCAST_LINES_HPP

#pragma codeseg MAINE_01_TEXT group_01
#include "src/maine/allcast/allcast.hpp"
bool near wait_flip_and_check_measure_target(void);

typedef uint8_t shiftjis_t;

// Complete canonical definition from src/maine/verdict/main.hpp. This
// independent owner preserves the same type and full original word domain.
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

// The seven genuine counts begin at DS:08DC. The old ASM label at 08DA
// aliases the preceding far pointer's segment word; it is not a dummy count.
// Use the actual counts and the natural zero-based screen index instead.
extern int allcast_lines_per_screen[7];

#pragma codeseg SHARED
extern "C" void pascal far graph_putsa_fx(screen_x_t left, screen_y_t top,
    vc2 color, const shiftjis_t far *text);

#pragma codeseg ALLCAST_LINES_TEXT group_01
bool near screen_line_next_animate(void);

typedef char allcast_line_pointer_is_far[
    (sizeof(const shiftjis_t far *) == 4) ? 1 : -1];
typedef char allcast_line_fx_is_word[
    (sizeof(graph_putsa_fx_func_t) == 2) ? 1 : -1];
typedef char allcast_line_result_is_byte[(sizeof(bool) == 1) ? 1 : -1];

#endif
