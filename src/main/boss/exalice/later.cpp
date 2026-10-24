// Three complete natural EX-Alice patterns following the first charged set.
#pragma option -zCEXALICE_LAT_TEXT -zPmain_03
#include "src/main/boss/exalice/later.hpp"

bool near exalice_pattern_firewave_fans(void)
{
    if(boss.phase_frame == 64) {
        boss_statebyte[14] = 0x40;
        boss_statebyte[13] = 0;
        pellet_bottom_col = 7;
    }
    if((boss.phase_frame % 2) == 0) {
        if((boss.phase_frame % 4) == 0) {
            bullet_template.spawn_type = 0x10;
            bullet_template.patnum = 0;
            bullet_template.group = BG_SPREAD_AIMED;
            exalice_set_spread(5, 6);
            bullet_template.speed.v = to_sp(5);
            bullet_template.angle = boss_statebyte[14];
            bullets_add_regular();
            bullet_template.angle = -bullet_template.angle;
            bullets_add_regular();
            if(boss_statebyte[13] == 0) {
                boss_statebyte[14] -= 3;
                if(boss_statebyte[14] <= 0x14) {
                    boss_statebyte[13]++;
                }
            } else {
                boss_statebyte[14] += 3;
                if(boss_statebyte[14] >= 0x40) {
                    boss_statebyte[13]--;
                }
            }
            if((boss.phase_frame % 16) == 0) {
                exalice_aim_origin.x.v = randring2_next16_mod(to_sp(96)) +
                    bullet_template.origin.x.v - to_sp(48);
                exalice_aim_origin.y.v = randring2_next16_mod(to_sp(64)) +
                    bullet_template.origin.y.v - to_sp(32);
                boss_statebyte[15] = player_angle_from(
                    exalice_aim_origin.x, exalice_aim_origin.y, 0);
            }
        }
        bullet_template.origin.x = exalice_aim_origin.x;
        bullet_template.origin.y = exalice_aim_origin.y;
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.angle = boss_statebyte[15];
        bullet_template.group = BG_SINGLE;
        bullet_template.speed.v = to_sp(6);
        bullet_template.patnum = EXALICE_PAT_V_RED;
        bullets_add_regular();
    }
    if((boss.phase_frame % 128) == 0) {
        firewaves_add(128, (boss.phase_frame % 256) == 0);
        snd_se_play(13);
    }
    if(boss.phase_frame >= 256) {
        boss_flystep_random((boss.phase_frame & 0x7F) - 96);
    }
    return false;
}

bool near exalice_pattern_gravity_stacks(void)
{
    if((boss.phase_frame % 2) == 0) {
        bullet_template.spawn_type = 0x10;
        bullet_template.speed.v = randring2_next16_and(0x1F) + to_sp(0.75f);
        bullet_template.angle = randring2_next16_and(0x7F) + 0x80;
        bullet_template.group = BG_SPREAD;
        bullet_template.special_motion = BSM_GRAVITY;
        bullet_special.speed_delta.v = 1;
        bullet_template.patnum = 46;
        exalice_set_spread(3, 12);
        bullets_add_special();
        if((boss.phase_frame % 4) == 0) {
            snd_se_play(3);
            bullet_template.spawn_type = 0x02 | 0x10;
            bullet_template.origin.x.v = randring2_next16_mod(to_sp(96)) -
                to_sp(48) + bullet_template.origin.x.v;
            bullet_template.origin.y.v = randring2_next16_mod(to_sp(64)) -
                to_sp(32) + bullet_template.origin.y.v;
            bullet_template.patnum = 0;
            bullet_template.group = BG_STACK_AIMED;
            bullet_template.speed.v = to_sp(3);
            reinterpret_cast<uint16_t &>(bullet_template.stack) = 4 | (6 << 8);
            bullet_template.angle = 0;
            bullets_add_regular();
        }
    }
    return (boss.phase_frame == 128);
}

bool near exalice_pattern_diamond_rings(void)
{
    if(boss.phase_frame == 64) {
        boss_statebyte[15] = 1 - boss_statebyte[15];
    }
    if((boss.phase_frame % 8) == 0) {
        bullet_template.spawn_type = 0x03 | 0x10;
        bullet_template.speed.v = to_sp(5.5f);
        bullet_template.angle = boss_statebyte[15]
            ? bullet_template.angle + 3 : bullet_template.angle - 3;
        bullet_template.group = BG_RING;
        exalice_set_spread(22, 8);
        bullet_template.patnum = 52;
        bullets_add_regular();
        snd_se_play(3);
    }
    return (boss.phase_frame == 128);
}
