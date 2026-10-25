// Complete score storage and actual MAINE numeric-rendering interfaces.
#ifndef TH05_MAINE_VERDICT_FORMAT_HPP
#define TH05_MAINE_VERDICT_FORMAT_HPP

#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'E'
#error This owner is the TH05 MAINE verdict formatter
#endif

typedef int screen_x_t;
typedef int screen_y_t;
typedef uint8_t shiftjis_t;
typedef unsigned int vc2;

// Semantic codes in the real shared gaiji domain, not bitmap contents.
enum verdict_numeric_glyph_t {
    VERDICT_GLYPH_NULL = 0,
    VERDICT_GLYPH_EMPTY = 0x02,
    VERDICT_GLYPH_ZERO = 0xA0,
    VERDICT_GLYPH_ONE,
    VERDICT_GLYPH_TWO,
    VERDICT_GLYPH_THREE,
    VERDICT_GLYPH_FOUR,
    VERDICT_GLYPH_FIVE,
    VERDICT_GLYPH_SIX,
    VERDICT_GLYPH_SEVEN,
    VERDICT_GLYPH_EIGHT,
    VERDICT_GLYPH_NINE
};
static const int VERDICT_GLYPH_WIDTH = 16;

extern bool skill_subtract;
extern bool graph_3_digit_put_as_fixed_2_digit;
extern uint32_t skill;
extern bool verdict_capture_quarter;
extern uint32_t verdict_skill_quarter;
extern vc2 verdict_text_color;

// These four distinct original DS arrays remain foreign semantic UI strings.
extern const shiftjis_t near verdict_score_unit[];
extern const shiftjis_t near verdict_decimal_point[];
extern const shiftjis_t near verdict_percent_sign[];
extern const shiftjis_t near verdict_fraction_point[];

#pragma codeseg _TEXT
extern "C" void pascal far graph_gaiji_puts(screen_x_t left, screen_y_t top,
    pixel_t step, const char far *text, vc2 color);
#pragma codeseg SHARED
extern "C" void pascal far graph_putsa_fx(screen_x_t left, screen_y_t top,
    vc2 color, const shiftjis_t far *text);

#ifdef TH05_VERDICT_FULL_FAMILY
#pragma codeseg VERDICT_FULL_TEXT group_01
#else
#pragma codeseg VERDICT_FMT_TEXT group_01
#endif
void pascal near graph_3_digit_put(screen_x_t left, screen_y_t top, uint16_t num);
void pascal near verdict_score_put(screen_x_t left, screen_y_t top,
    const score_lebcd_t far &score);
void pascal near skill_apply_and_graph_percentage_put(screen_x_t left,
    screen_y_t top, uint16_t total, uint16_t share);
void pascal near graph_fraction_of_million_put(screen_x_t left,
    screen_y_t top, uint32_t num);

typedef char verdict_score_storage_is_8[(sizeof(score_lebcd_t) == 8) ? 1 : -1];
typedef char verdict_score_digits_are_8[(sizeof(((score_lebcd_t *)0)->digits) == 8) ? 1 : -1];
typedef char verdict_score_pointer_is_far[(sizeof(const score_lebcd_t far *) == 4) ? 1 : -1];
typedef char verdict_flag_is_1[(sizeof(skill_subtract) == 1) ? 1 : -1];
typedef char verdict_skill_is_4[(sizeof(skill) == 4) ? 1 : -1];
typedef char verdict_color_is_2[(sizeof(verdict_text_color) == 2) ? 1 : -1];

#endif
