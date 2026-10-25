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
