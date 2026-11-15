// Verdict screen number formatting: shared state, gaiji codes and the four
// formatter functions in body/graph_*.inl and body/verdict_score_put.inl.
//
// Every extern function below is declared under the code segment its
// definition lives in (`#pragma codeseg`), because Borland binds a function to
// the segment of its first declaration. The formatter group's segment depends
// on whether full.cpp (all ten verdict functions) or a standalone wrapper is
// being compiled.
#ifndef TH05_MAINE_VERDICT_FORMAT_HPP
#define TH05_MAINE_VERDICT_FORMAT_HPP

#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'E'
#error This header is for TH05 MAINE.EXE only
#endif

typedef int screen_x_t;
typedef int screen_y_t;
typedef uint8_t shiftjis_t;
typedef unsigned int vc2;

// Gaiji codes of the bold verdict digits.
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

// If `true`, skill_apply_and_graph_percentage_put() will subtract the
// calculated fraction from [skill] rather than add it.
extern bool skill_subtract;

// ZUN bloat: Turn into a parameter of graph_3_digit_put().
extern bool graph_3_digit_put_as_fixed_2_digit;

extern uint32_t skill;

// If `true`, skill_apply_and_graph_percentage_put() also stores a quarter of
// the calculated fraction in [verdict_skill_quarter]. Only set for the stage
// completion rate, which therefore counts more towards the final skill value.
extern bool verdict_capture_quarter;
extern uint32_t verdict_skill_quarter;

extern vc2 verdict_text_color;

// Four separate string objects in the original, even though the two decimal
// points are identical. Defined in punctuation_data.c.
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
// Assumes that [num] is a 3-digit number and renders it right-aligned to the
// given VRAM position.
void pascal near graph_3_digit_put(screen_x_t left, screen_y_t top, uint16_t num);

// Renders all eight score digits, followed by the "点" unit. Unlike TH04, a
// top byte of 10 or more (scores above 99,999,999) adds a ninth digit.
void pascal near verdict_score_put(screen_x_t left, screen_y_t top,
    const score_lebcd_t far &score);

// Calculates ([share] / [total]), applies the result × 1,000,000 to [skill],
// and renders it as a right-aligned 3.2-digit percentage to the given VRAM
// position.
void pascal near skill_apply_and_graph_percentage_put(screen_x_t left,
    screen_y_t top, uint16_t total, uint16_t share);

// Calculates ([num] / 1,000,000) and renders the result as a right-aligned
// 3.2-digit fraction to the given VRAM position.
void pascal near graph_fraction_of_million_put(screen_x_t left,
    screen_y_t top, uint32_t num);

#endif
