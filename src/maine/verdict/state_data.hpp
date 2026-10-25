// DATA-only declarations matching the canonical verdict interfaces' types.
#ifndef TH05_MAINE_VERDICT_STATE_DATA_HPP
#define TH05_MAINE_VERDICT_STATE_DATA_HPP
#include "src/main/hud/resident.hpp"

// screen_x_t/screen_y_t are int; vc2 is unsigned int in format.hpp.
extern int verdict_text_left;
extern unsigned int verdict_text_color;
extern unsigned int verdict_comment_color;
extern int verdict_text_top;
extern bool skill_subtract;
extern char verdict_rank_glyphs[5][8];
extern bool graph_3_digit_put_as_fixed_2_digit;

typedef char verdict_state_coord_is_word[(sizeof(verdict_text_left) == 2) ? 1 : -1];
typedef char verdict_state_color_is_word[(sizeof(verdict_text_color) == 2) ? 1 : -1];
typedef char verdict_state_flag_is_byte[(sizeof(skill_subtract) == 1) ? 1 : -1];
#endif
