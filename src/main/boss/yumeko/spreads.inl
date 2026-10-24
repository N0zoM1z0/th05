void near yumeko_pattern_counterrotating_spreads(void)
{
    if(boss.phase_frame < 16) {
        gather_add_only_3stack(boss.phase_frame - 1, 7, 6);
        if(boss.phase_frame == 4) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_NO_DECELERATE;
            bullet_template.group = BG_SPREAD;
            bullet_template.special_motion = BSM_EXACT_LINEAR;
            bullet_template.speed.v = 3 * 16 + 8;
            reinterpret_cast<uint16_t &>(bullet_template.spread) = (5 | (2 << 8));
            snd_se_play(8);
            yumeko_angle_a = 0x60;
            yumeko_angle_b = 0x40;
        }
        return;
    }
    if((boss.phase_frame % 8) == 0) {
        bullet_template.patnum = 44; // Blue ball.
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), yumeko_angle_a);
        bullet_template.angle = yumeko_angle_a + yumeko_angle_b;
        bullets_add_special();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), static_cast<unsigned char>(yumeko_angle_a + 0x80));
        bullet_template.angle += 0x80;
        bullets_add_special();

        bullet_template.patnum = 0;
        yumeko_angle_a = -yumeko_angle_a;
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(32), yumeko_angle_a);
        bullet_template.angle = yumeko_angle_a - yumeko_angle_b;
        bullets_add_special();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(32), static_cast<unsigned char>(yumeko_angle_a + 0x80));
        bullet_template.angle += 0x80;
        bullets_add_special();
        yumeko_angle_a = -yumeko_angle_a;
        yumeko_angle_a -= 8;
        yumeko_angle_b -= 6;
        snd_se_play(3);
    }
    if(boss.phase_frame == 256) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}

void near yumeko_pattern_mirrored_spreads(void)
{
    if(boss.phase_frame < 16) {
        gather_add_only_3stack(boss.phase_frame - 1, 7, 6);
        if(boss.phase_frame == 4) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_NO_DECELERATE;
            bullet_template.group = BG_SPREAD_AIMED;
            bullet_template.speed.v = 3 * 16 + 8;
            bullet_template.spread_angle_delta = 20;
            bullet_template.angle = 0;
            bullet_template.patnum = 68; // Green directional bullet.
            bullet_template_tune();
            snd_se_play(8);
            yumeko_angle_a = 0x80;
        }
        return;
    }
    if((boss.phase_frame % 8) == 0) {
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), yumeko_angle_a);
        bullet_template.spread = 5;
        bullets_add_regular();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), static_cast<unsigned char>(0x80 - yumeko_angle_a));
        bullet_template.spread = 4;
        bullets_add_regular();
        yumeko_angle_a += 8;
        snd_se_play(3);
    }
    if(boss.phase_frame == 192) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}
