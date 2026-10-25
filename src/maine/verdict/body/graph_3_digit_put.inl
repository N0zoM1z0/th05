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
