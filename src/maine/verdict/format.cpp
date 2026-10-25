// Complete MAINE verdict number/score/fraction formatting, C5E7..C8AE.
#pragma option -zCVERDICT_FMT_TEXT -zPgroup_01
#include "src/maine/verdict/format.hpp"

void pascal near graph_3_digit_put(screen_x_t left, screen_y_t top, uint16_t num)
{
    int digit_seen = 0;
    char glyphs[4];
    int digit;

    glyphs[0] = VERDICT_GLYPH_EMPTY;
    digit = num / 100;
    num %= 100;
    if(!graph_3_digit_put_as_fixed_2_digit) {
        digit_seen |= digit;
        if(digit_seen) {
            glyphs[0] = VERDICT_GLYPH_ZERO + digit;
        } else {
            glyphs[0] = VERDICT_GLYPH_EMPTY;
        }
    }
    digit = num / 10;
    num %= 10;
    digit_seen |= digit;
    digit_seen |= graph_3_digit_put_as_fixed_2_digit;
    if(digit_seen) {
        glyphs[1] = VERDICT_GLYPH_ZERO + digit;
    } else {
        glyphs[1] = VERDICT_GLYPH_EMPTY;
    }
    glyphs[2] = VERDICT_GLYPH_ZERO + num;
    glyphs[3] = VERDICT_GLYPH_NULL;
    graph_gaiji_puts(left, top, VERDICT_GLYPH_WIDTH, glyphs, verdict_text_color);
}

void pascal near verdict_score_put(screen_x_t left, screen_y_t top,
    const score_lebcd_t far &score)
{
    unsigned char digit;
    unsigned char digit_seen;
    char glyphs[SCORE_DIGITS + 2];
    int i;

    // The highest stored byte may hold two decimal digits above 99,999,999.
    if(score.digits[SCORE_DIGITS - 1] >= 10) {
        digit = score.digits[SCORE_DIGITS - 1] / 10;
        glyphs[0] = VERDICT_GLYPH_ZERO + digit;
        digit_seen = 1;
    } else {
        glyphs[0] = VERDICT_GLYPH_EMPTY;
        digit_seen = 0;
    }
    for(i = 1; i <= SCORE_DIGITS; i++) {
        digit = score.digits[SCORE_DIGITS - i] % 10;
        digit_seen |= digit;
        if(digit_seen || i == SCORE_DIGITS) {
            glyphs[i] = VERDICT_GLYPH_ZERO + digit;
        } else {
            glyphs[i] = VERDICT_GLYPH_EMPTY;
        }
    }
    glyphs[SCORE_DIGITS + 1] = VERDICT_GLYPH_NULL;
    graph_gaiji_puts(left, top, VERDICT_GLYPH_WIDTH, glyphs, verdict_text_color);
    graph_putsa_fx(left + (9 * VERDICT_GLYPH_WIDTH), top,
        verdict_text_color, verdict_score_unit);
}

void pascal near skill_apply_and_graph_percentage_put(screen_x_t left,
    screen_y_t top, uint16_t total, uint16_t share)
{
    register screen_x_t left_origin = left;
    register screen_y_t top_origin = top;
    uint16_t digits;
    uint32_t fraction;

    if(total) {
        fraction = 1000000UL;
    } else {
        fraction = 0;
    }
    if(total != share) {
        if(total) {
            fraction /= total;
        } else {
            fraction = 0;
        }
        fraction *= share;
    }
    if(!skill_subtract) {
        skill = skill + fraction;
    } else {
        skill = skill - fraction;
    }
    if(verdict_capture_quarter) {
        verdict_skill_quarter = fraction / 4;
    }

    digits = fraction / 10000UL;
    graph_3_digit_put(left_origin, top_origin, digits);
    fraction %= 10000UL;
    digits = fraction / 100UL;
    graph_3_digit_put_as_fixed_2_digit = true;
    graph_3_digit_put(left_origin + 48, top_origin, digits);
    graph_3_digit_put_as_fixed_2_digit = false;
    graph_putsa_fx(left_origin + 48, top_origin, verdict_text_color,
        verdict_decimal_point);
    graph_putsa_fx(left_origin + 96, top_origin, verdict_text_color,
        verdict_percent_sign);
}

void pascal near graph_fraction_of_million_put(screen_x_t left,
    screen_y_t top, uint32_t num)
{
    screen_x_t left_origin = left;
    screen_y_t top_origin = top;
    uint16_t digits;

    digits = num / 10000UL;
    graph_3_digit_put(left_origin, top_origin, digits);
    num %= 10000UL;
    digits = num / 100UL;
    graph_3_digit_put_as_fixed_2_digit = true;
    graph_3_digit_put(left_origin + 48, top_origin, digits);
    graph_3_digit_put_as_fixed_2_digit = false;
    graph_putsa_fx(left_origin + 48, top_origin, verdict_text_color,
        verdict_fraction_point);
}
