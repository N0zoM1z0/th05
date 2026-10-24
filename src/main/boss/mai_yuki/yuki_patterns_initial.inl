// Three complete initial solo-Yuki patterns. Natural bodies only.
bool near yuki_solo_ring_sweep(void)
{
    if(boss.phase_frame == 48) {
        yuki_solo_angle = randring2_next16();
        yuki_solo_angle_step = 1;
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        bullet_template.patnum = YUKI_SOLO_SMALL_BALL_RED;
        bullet_template.spread = rank + 5;
        bullet_template.speed.v = 3 * 16 + 6;
        boss.sprite = YUKI_SOLO_SPRITE_FIRE;
        bullet_template_tune();
    } else if(boss.phase_frame > 48) {
        if((boss.phase_frame % 2) == 0) {
            bullet_template.angle = yuki_solo_angle;
            yuki_solo_angle += yuki_solo_angle_step;
            bullets_add_special();
            if((boss.phase_frame % 16) == 0) {
                yuki_solo_angle += yuki_solo_angle_step * 12;
            }
            snd_se_play(3);
        }
        if(boss.phase_frame == 160) {
            yuki_solo_angle_step = -yuki_solo_angle_step;
        }
        if(boss.phase_frame == 256) {
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        }
        if((boss.phase_state.patterns_seen >= 2) && (boss.phase_frame >= 64)) {
            boss_flystep_random(boss.phase_frame % 64);
        }
    }
    return false;
}

bool near yuki_solo_random_spreads(void)
{
    if(boss.phase_frame == 8) {
        bullet_template.angle = 0x80;
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        boss.sprite = YUKI_SOLO_SPRITE_FIRE;
        bullet_template.patnum = YUKI_SOLO_BALL_RED;
    } else if(boss.phase_frame > 8) {
        if((boss.phase_frame % 2) == 0) {
            bullet_template.speed.v = randring2_next16_and(0x1F) + 8;
            bullet_template.spread = randring2_next16_and(7);
            bullet_template.spread_angle_delta = 6;
            bullet_template_tune();
            bullets_add_regular();
            bullet_template.angle += 6;
            snd_se_play(3);
        }
        if(boss.phase_frame == 256) {
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        }
        if((boss.phase_state.patterns_seen >= 2) && (boss.phase_frame >= 64)) {
            boss_flystep_random(boss.phase_frame % 64);
        }
    }
    return false;
}

bool near yuki_solo_random_rings(void)
{
    if(boss.phase_frame == 8) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.patnum = 0;
        bullet_template.spread = 24;
        bullet_template_tune();
        boss.sprite = YUKI_SOLO_SPRITE_FIRE;
    } else if(boss.phase_frame > 8) {
        if((boss.phase_frame % 16) == 0) {
            bullet_template.angle = randring2_next16();
            bullet_template.speed.v = randring2_next16_and(0x1F) + 2 * 16;
            bullets_add_regular();
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
