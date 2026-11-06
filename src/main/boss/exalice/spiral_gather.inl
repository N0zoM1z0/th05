bool near exalice_pattern_spiral_gather(void)
{
    bullet_template.origin.y.v += to_sp(104);
    gather_template.center.x.v = bullet_template.origin.x.v = exalice_sweep_x;
    if(boss.phase_frame == 64) {
        cheeto_template.angle = static_cast<unsigned char>(-0x3C);
        bullet_template.angle = 0x20;
        cheeto_template.speed.v = to_sp(5);
        bullet_template.speed.v = to_sp(3);
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_SPREAD;
        exalice_set_spread(3, 8);
        bullet_template.patnum = 47;
        boss_statebyte[15] = 0;
        boss_statebyte[14] = 0;
        boss_statebyte[13] = 0;
        snd_se_play(8);
    }
    if(boss.phase_frame < 128) {
        if((boss.phase_frame % 8) == 0) {
            gather_template.col = 14;
            gather_template.center.y = bullet_template.origin.y;
            gather_template.radius.v = to_sp(256);
            if((boss.phase_frame % 16) == 0) {
                gather_template.angle_delta = 2;
            } else {
                gather_template.angle_delta = static_cast<unsigned char>(-2);
            }
            gather_add_only();
        }
    } else if((boss.phase_frame % 2) == 0) {
        if((boss.phase_frame % 16) == 0) {
            gather_template.center.y = bullet_template.origin.y;
            gather_template.radius.v = to_sp(128);
            if((boss.phase_frame % 32) == 0) {
                gather_template.angle_delta = 2;
            } else {
                gather_template.angle_delta = static_cast<unsigned char>(-2);
            }
            gather_add_only();
        }
        bullet_template.angle = 0x80 - bullet_template.angle;
        bullets_add_regular_fixedspeed();
        bullet_template.angle = 0x80 - bullet_template.angle;
        bullets_add_regular_fixedspeed();
        snd_se_play(3);
        bullet_template.angle -= boss_statebyte[15];
        if((boss.phase_frame % 32) == 0) {
            boss_statebyte[15] += boss_statebyte[14];
            if(boss_statebyte[13] == 0) {
                boss_statebyte[14]++;
                if(boss_statebyte[14] >= 0x10) {
                    boss_statebyte[13]++;
                }
            } else {
                boss_statebyte[14]--;
                if(boss_statebyte[14] == 0) {
                    exalice_sweep_x = player_pos.cur.x;
                    return true;
                }
            }
        }
    }
    return false;
}
