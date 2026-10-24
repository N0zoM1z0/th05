bool near mai_pattern_reversing_rings(void)
{
    if(boss.phase_frame == 48) {
        boss_statebyte[15] = 0x20;
        boss_statebyte[12] = static_cast<unsigned char>(-4);
    }
    if((boss.phase_frame % 4) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.angle = boss_statebyte[15];
        boss_statebyte[15] += boss_statebyte[12];
        bullet_template.patnum = MY_PAT_SMALL_BALL_BLUE;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(-8);
        bullet_template.spread = 4;
        bullet_template.speed.v = mai_yuki_speed(2.375f);
        bullet_template_tune();
        bullets_add_regular();
        if((boss.phase_frame % 16) == 0) {
            boss_statebyte[15] = boss_statebyte[15] -
                (randring2_next16_and(7) + 0x10);
            boss_statebyte[12] = -boss_statebyte[12];
        }
        snd_se_play(3);
    }
    if(boss.phase_frame == 256) {
        return true;
    }
    return false;
}

bool near yuki_pattern_random_aimed_fan(void)
{
    if((boss.phase_frame % 16) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.angle = randring2_next16_and(0x3f) - 0x20;
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        bullet_template.origin.x = boss2.pos.cur.x;
        bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_spread(7, 5);
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        bullet_template.speed.v = randring2_next16_and(0x1f) + to_sp(1.0f);
        bullet_template_tune();
        bullets_add_special();
    }
    return false;
}

bool near yuki_pattern_random_rings(void)
{
    if((boss.phase_frame % 16) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.angle = randring2_next16();
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        bullet_template.origin.x = boss2.pos.cur.x;
        bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(-8);
        bullet_template.spread = 32;
        bullet_template.speed.v = mai_yuki_speed(2.5f);
        bullet_template_tune();
        bullets_add_regular();
    }
    return false;
}

bool near yuki_pattern_small_ball_stacks(void)
{
    if((boss.phase_frame % 16) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_STACK_AIMED;
        bullet_template.angle = 0;
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        bullet_template.origin.x = boss2.pos.cur.x;
        bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_stack(8, 0.25f);
        bullet_template.speed.v = mai_yuki_speed(2.0f);
        bullet_template_tune();
        bullets_add_regular();
    }
    return false;
}

bool near yuki_pattern_small_ball_fan(void)
{
    if((boss.phase_frame % 8) == 0) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = 0x40;
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        bullet_template.origin.x = boss2.pos.cur.x;
        bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_spread(8, 12);
        bullet_template.speed.v = mai_yuki_speed(4.0f);
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(3);
    }
    return false;
}

bool near yuki_pattern_ball_stacks(void)
{
    if((boss.phase_frame % 8) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_STACK_AIMED;
        bullet_template.angle = 0;
        bullet_template.patnum = MY_PAT_BALL_RED;
        bullet_template.origin.x = boss2.pos.cur.x;
        bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_stack(8, 0.375f);
        bullet_template.speed.v = mai_yuki_speed(2.0f);
        bullet_template_tune();
        bullets_add_regular();
    }
    return false;
}

bool near yuki_pattern_random_pellets(void)
{
    if((boss.phase_frame % 2) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = randring2_next16();
        bullet_template.patnum = 0;
        bullet_template.origin.x = boss2.pos.cur.x;
        bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_spread(2, 2);
        bullet_template.speed.v = randring2_next16_and(0x1f) + to_sp(1.5f);
        bullet_template_tune();
        bullets_add_regular();
    }
    return false;
}

bool near yuki_pattern_reversing_rings(void)
{
    if(boss.phase_frame == 48) {
        boss_statebyte[14] = 0;
        boss_statebyte[13] = 4;
    }
    if((boss.phase_frame % 4) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.angle = boss_statebyte[14];
        boss_statebyte[14] += boss_statebyte[13];
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        bullet_template.origin.x = boss2.pos.cur.x;
        bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(-8);
        bullet_template.spread = 4;
        bullet_template.speed.v = mai_yuki_speed(2.375f);
        bullet_template_tune();
        bullets_add_regular();
        if((boss.phase_frame % 16) == 0) {
            boss_statebyte[14] = randring2_next16_and(7) + boss_statebyte[14] + 0x10;
            boss_statebyte[13] = -boss_statebyte[13];
        }
    }
    return false;
}

bool near yuki_pattern_cheetos(void)
{
    unsigned char angle;
    if((boss.phase_frame == 48) || (boss.phase_frame == 96)) {
        cheeto_template.origin = boss2.pos.cur;
        cheeto_template.col = 11;
        cheeto_template.speed.v = mai_yuki_speed(2.0f);
        if(boss.pos.cur.x.v >= boss2.pos.cur.x.v) {
            angle = 0x40;
        } else {
            angle = static_cast<unsigned char>(-0x40);
        }
        cheeto_template.angle = player_angle_from(
            cheeto_template.origin.x, cheeto_template.origin.y, angle);
        cheetos_add();
        snd_se_play(15);
    }
    return false;
}

bool near mai_pattern_cheetos(void)
{
    unsigned char angle;
    if((boss.phase_frame == 48) || (boss.phase_frame == 96)) {
        cheeto_template.origin = boss.pos.cur;
        cheeto_template.col = 9;
        cheeto_template.speed.v = mai_yuki_speed(2.0f);
        if(boss.pos.cur.x.v < boss2.pos.cur.x.v) {
            angle = 0x40;
        } else {
            angle = static_cast<unsigned char>(-0x40);
        }
        cheeto_template.angle = player_angle_from(
            cheeto_template.origin.x, cheeto_template.origin.y, angle);
        cheetos_add();
        snd_se_play(15);
    }
    return (boss.phase_frame == 128);
}
