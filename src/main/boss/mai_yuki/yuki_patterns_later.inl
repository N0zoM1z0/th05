// Four complete snow/vector/acceleration solo-Yuki patterns.
bool near yuki_solo_snow_fan(void)
{
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 9, 8);
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.patnum = YUKI_SOLO_BALL_RED;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = (5 | (12 << 8));
        bullet_template.angle = 0;
        bullet_template_tune();
        boss.sprite = YUKI_SOLO_SPRITE_FIRE;
        b4ball_template.speed.v = 4 * 16;
    } else {
        if((boss.phase_frame % 32) == 0) {
            bullet_template.speed.v = randring2_next16_and(0x1F) + 16;
            bullets_add_regular();
            b4ball_template.angle = player_angle_from(
                b4ball_template.origin.x, b4ball_template.origin.y, 0);
            b4balls_add();
            b4ball_template.angle -= 12;
            b4balls_add();
            b4ball_template.angle -= 12;
            b4balls_add();
            b4ball_template.angle += 36;
            b4balls_add();
            b4ball_template.angle += 12;
            b4balls_add();
            snd_se_play(15);
        }
        if(boss.phase_frame == 160) {
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        }
        if((boss.phase_state.patterns_seen >= 2) && (boss.phase_frame >= 64)) {
            boss_flystep_random((boss.phase_frame % 64) - 32);
        }
    }
    return false;
}

bool near yuki_solo_snow_cross(void)
{
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 9, 8);
        boss.sprite = YUKI_SOLO_SPRITE_FIRE;
        b4ball_template.speed.v = 2 * 16;
    } else {
        if(boss.phase_frame == 32) {
            snd_se_play(15);
        }
        if((boss.phase_frame % 4) == 0) {
            b4balls_add();
            b4ball_template.angle += 0x40;
            b4balls_add();
            b4ball_template.angle += 0x40;
            b4balls_add();
            b4ball_template.angle += 0x40;
            b4balls_add();
            b4ball_template.angle += 0x40;
            b4ball_template.angle += yuki_solo_snow_step;
        }
        if(boss.phase_frame == 64) {
            boss.phase_frame = 0;
            boss.mode = 0;
            yuki_solo_snow_step = -yuki_solo_snow_step;
            return true;
        }
    }
    return false;
}

bool near yuki_solo_vector_stacks(void)
{
    if(boss.phase_frame == 24) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_STACK;
        bullet_template.patnum = YUKI_SOLO_VECTOR_RED;
        reinterpret_cast<uint16_t &>(bullet_template.stack) = (8 | (6 << 8));
        bullet_template.angle = 0x10;
        bullet_template.speed.v = 2 * 16;
        bullet_template_tune();
        boss.sprite = YUKI_SOLO_SPRITE_FIRE;
    } else if(boss.phase_frame >= 24) {
        if((boss.phase_frame % 2) == 0) {
            bullet_template.angle = yuki_solo_angle;
            bullets_add_regular();
            yuki_solo_angle += yuki_solo_angle_step;
            snd_se_play(15);
        }
        if(boss.phase_frame == 64) {
            yuki_solo_angle_step = -yuki_solo_angle_step;
            if(yuki_solo_angle_step < 0x7F) {
                yuki_solo_angle = 0x10;
            } else {
                yuki_solo_angle = 0x70;
            }
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        }
        if(boss.phase_state.patterns_seen > 2) {
            boss_flystep_random((boss.phase_frame % 64) - 25);
        }
    }
    return false;
}

bool near yuki_solo_speedup(void)
{
    if(boss.phase_frame == 8) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RANDOM_ANGLE;
        bullet_template.special_motion = BSM_SPEEDUP;
        bullet_special.speed_delta.v = 1;
        bullet_template.patnum = YUKI_SOLO_VECTOR_RED;
        bullet_template.spread = rank * 2 + 4;
        boss.sprite = YUKI_SOLO_SPRITE_FIRE;
        bullet_template.speed.v = 2 * 16;
    } else if(boss.phase_frame > 8) {
        if((boss.phase_frame % 4) == 0) {
            bullets_add_special();
        }
        if(boss.phase_frame >= 128) {
            if(boss.phase_frame < 320) {
                boss_flystep_random((boss.phase_frame % 64) - 32);
            } else {
                boss_flystep_random(boss.phase_frame % 64);
            }
        }
    }
    return false;
}
