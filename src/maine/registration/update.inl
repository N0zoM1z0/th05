void near glyphballs_update(void)
{
    int pattern;
    int left;
    int top;
    uint8_t angle_delta;
    uint8_t target_angle;
    register glyphball_t near *ball;
    register int i;

    for((ball = glyphballs, i = 0); i < REGISTRATION_NAME_LENGTH; (i++, ball++)) {
        if(ball->phase == GBP_FREE) {
            continue;
        }
        if(ball->phase == GBP_DONE) {
            ball->phase = GBP_FREE;
        }
        if(ball->pos.prev.x.v < 0) {
            ball->pos.prev.x.v = 0;
        }
        if(ball->pos.prev.y.v < 0) {
            ball->pos.prev.y.v = 0;
        }
        bgimage_put_rect_16(
            (ball->pos.prev.x.v / 16) - (REG_CLOUD_SIZE / 2),
            (ball->pos.prev.y.v / 16) - (REG_CLOUD_SIZE / 2),
            REG_CLOUD_SIZE, REG_CLOUD_SIZE);
    }
    reg_name_put(entered_place, playchar, entered_name_cursor);

    for((ball = glyphballs, i = 0); i < REGISTRATION_NAME_LENGTH; (i++, ball++)) {
        if(ball->phase == GBP_FREE) {
            continue;
        }
        switch(ball->phase) {
        case GBP_CLOUD_AT_ORIGIN:
            ball->pos.prev = ball->pos.cur;
            left = (ball->pos.cur.x.v / 16) - (REG_CLOUD_SIZE / 2);
            top = (ball->pos.cur.y.v / 16) - (REG_CLOUD_SIZE / 2);
            pattern = (static_cast<unsigned int>(ball->phase_frame) >> 1) +
                REG_GLYPH_CLOUD;
            if(pattern < REG_GLYPH_CLOUD + REG_GLYPH_CELS) {
                break;
            }
            ball->phase++;
            // The final cloud frame moves immediately, without resetting age.
        case GBP_FLOAT_TO_TARGET:
            ball->pos.prev = ball->pos.cur;
            vector2_at(ball->pos.velocity, 0, 0, ball->speed.v, ball->angle);
            ball->pos.cur.x.v += ball->pos.velocity.x.v;
            ball->pos.cur.y.v += ball->pos.velocity.y.v;
            left = (ball->pos.cur.x.v / 16) - (REG_BALL_SIZE / 2);
            top = (ball->pos.cur.y.v / 16) - (REG_BALL_SIZE / 2);
            if(left < 0) {
                left = 0;
                ball->angle = 0x80 - ball->angle;
                ball->pos.cur.x.v = (REG_BALL_SIZE / 2) * 16;
            } else if(left >= 640 - REG_BALL_SIZE) {
                left = 640 - REG_BALL_SIZE;
                ball->angle = 0x80 - ball->angle;
                ball->pos.cur.x.v = (640 - (REG_BALL_SIZE / 2)) * 16;
            }
            if(top < 0) {
                top = 0;
                ball->angle = -ball->angle;
                ball->pos.cur.y.v = (REG_BALL_SIZE / 2) * 16;
            } else if(top >= 400 - REG_BALL_SIZE) {
                top = 400 - REG_BALL_SIZE;
                ball->angle = -ball->angle;
                ball->pos.cur.y.v = (400 - (REG_BALL_SIZE / 2)) * 16;
            }
            pattern = ((static_cast<unsigned int>(ball->phase_frame) >> 2) & 3) +
                REG_GLYPH_BALL;
            target_angle = iatan2(ball->target.y - ball->pos.cur.y,
                ball->target.x - ball->pos.cur.x);
            angle_delta = ball->angle - target_angle;
            if(angle_delta >= 0x80) {
                if(angle_delta >= static_cast<uint8_t>(-2)) {
                    ball->angle = target_angle;
                    if(ball->speed.v < 8 * 16) {
                        ball->speed.v += 2;
                    }
                } else {
                    if(angle_delta > static_cast<uint8_t>(-0x10)) {
                        angle_delta = 1;
                        if(ball->speed.v < 8 * 16) {
                            ball->speed.v += 2;
                        }
                    } else {
                        angle_delta = (256 - angle_delta) / 16;
                        if(ball->speed.v > 8) {
                            ball->speed.v -= 2;
                        }
                    }
                    ball->angle += angle_delta;
                }
            } else {
                if(angle_delta <= 2) {
                    ball->angle = target_angle;
                    if(ball->speed.v < 8 * 16) {
                        ball->speed.v += 2;
                    }
                } else {
                    if(angle_delta < 0x10) {
                        angle_delta = 1;
                        if(ball->speed.v < 8 * 16) {
                            ball->speed.v += 2;
                        }
                    } else {
                        angle_delta /= 16;
                        if(ball->speed.v > 8) {
                            ball->speed.v -= 2;
                        }
                    }
                    ball->angle -= angle_delta;
                }
            }
            if(static_cast<unsigned int>(ball->pos.cur.x - ball->target.x + 4 * 16) <
                    8 * 16 &&
               static_cast<unsigned int>(ball->pos.cur.y - ball->target.y + 4 * 16) <
                    8 * 16) {
                ball->phase++;
                ball->phase_frame = 0;
                hi.score.g_name[entered_place][i] = ball->glyph;
            }
            break;

        case GBP_SPLASH_AT_TARGET:
            pattern = (static_cast<unsigned int>(ball->phase_frame) >> 2) +
                REG_GLYPH_SPLASH;
            if(pattern >= REG_GLYPH_SPLASH + REG_GLYPH_CELS) {
                ball->phase++;
                continue;
            }
            ball->pos.prev = ball->target;
            left = (ball->target.x.v / 16) - (REG_CLOUD_SIZE / 2);
            top = (ball->target.y.v / 16) - (REG_CLOUD_SIZE / 2);
            break;

        case GBP_REMOVE_REQUEST:
            ball->phase--;
            continue;
        }
        // Invalid phases also reach this path with the original stale locals.
        ball->phase_frame++;
        super_put_rect(left, top, pattern);
    }
}
