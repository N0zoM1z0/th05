// Complete final EX-Alice patterns, preserving actual signed frame arithmetic.
#pragma option -zCEXALICE_FIN_TEXT -zPmain_03
#include "src/main/boss/exalice/final_patterns.hpp"

bool near exalice_pattern_cross_cheetos(void)
{
    if((boss.phase_frame % 16) == 0) {
        bullet_template.speed.v = to_sp(3.5f);
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.patnum = 47;
        bullet_template.angle = 0;
        exalice_set_spread(9, 15);
        bullets_add_regular();
        if((boss.phase_frame % 64) == 0) {
            cheeto_template.col = 11;
            cheeto_template.speed.v = to_sp(3);
            if((boss.phase_frame % 128) == 0) {
                cheeto_template.angle = player_angle_from(
                    cheeto_template.origin.x, cheeto_template.origin.y, 0x20);
            } else {
                cheeto_template.angle = player_angle_from(
                    cheeto_template.origin.x, cheeto_template.origin.y,
                    static_cast<unsigned char>(-0x20));
            }
            cheetos_add();
            snd_se_play(15);
        }
    }
    return (boss.phase_frame == 256);
}

bool near exalice_pattern_turning_cheetos(void)
{
    if((boss.phase_frame % 8) == 0) {
        cheeto_template.col = 11;
        cheeto_template.speed.v = to_sp(4);
        if((boss.phase_frame % 16) == 0) {
            cheeto_template.angle = player_angle_from(
                cheeto_template.origin.x, cheeto_template.origin.y, 0x40);
        } else {
            cheeto_template.angle = player_angle_from(
                cheeto_template.origin.x, cheeto_template.origin.y,
                static_cast<unsigned char>(-0x40));
        }
        cheetos_add();
        snd_se_play(15);
    }
    boss_flystep_random(boss.phase_frame % 32);
    return (boss.phase_frame == 128);
}

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

void near exalice_pattern_final_fan(void)
{
    gather_add_only_3stack(boss.phase_frame - 64, 6, 7);
    if(boss.phase_frame == 64) {
        boss.sprite = 181;
        snd_se_play(8);
        bullet_template.patnum = 116;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = randring2_next16();
        exalice_set_spread(5, 21);
        boss_statebyte[15] = 0;
        boss.pos.velocity.x.v = 0;
    }
    if(boss.phase_frame >= 128) {
        if((boss.phase_frame % 2) == 0) {
            bullet_template.speed.v =
                (static_cast<unsigned long>(3400 - boss.hp) * 64 / 3400) + to_sp(2.5f);
            bullets_add_regular();
            bullet_template.angle += 0x80;
            bullets_add_regular();
            bullet_template.angle += 0x87;
            snd_se_play(9);
        }
        boss.pos.cur.x.v = polar(to_sp(192), boss.pos.velocity.x.v,
            SinTable8[boss_statebyte[15]]);
        boss_statebyte[15] += 2;
        // The radius spans64 pixels, converted to16 subpixels per pixel.
        boss.pos.velocity.x.v =
            ((static_cast<unsigned long>(3400 - boss.hp) * 64) * 16) / 3400;
    }
}
