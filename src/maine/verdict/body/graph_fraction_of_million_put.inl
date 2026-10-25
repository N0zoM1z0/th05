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
