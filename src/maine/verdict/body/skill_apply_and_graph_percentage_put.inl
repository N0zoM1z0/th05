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
