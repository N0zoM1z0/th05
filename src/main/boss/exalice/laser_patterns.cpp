// Four complete patterns: bouncing bullets, fixed lasers and moving fans.
#pragma option -zCEXALICE_LSR_TEXT -zPmain_03
#include "src/main/boss/exalice/laser_patterns.hpp"

bool near exalice_pattern_bouncing_rings(void)
{
    if(boss.phase_frame == 64) {
        bullet_template.spread = 8;
    }
    if((boss.phase_frame % 16) == 0) {
        bullet_template.patnum = 52;
        bullet_template.spawn_type = 0x03 | 0x10;
        bullet_template.speed.v = to_sp(2);
        bullet_template.group = BG_RING;
        bullet_template.special_motion = BSM_BOUNCE_LEFT_RIGHT_TOP;
        if((boss.phase_frame % 128) == 0 && bullet_template.spread < 14) {
            bullet_template.spread++;
        }
        bullet_special.turns_max = 1;
        bullet_template.angle += 2;
        bullets_add_special();
        snd_se_play(3);
    }
    return false;
}

bool near exalice_pattern_fixed_laser_fan(void)
{
    int frame_in_cycle = boss.phase_frame % 16;
    laser_template.col = 3;
    laser_template.coords.width.nonshrink = 8;
    laser_template.active_at_age.grow = 47;
    laser_template.shrink_at_age = 80;
    if(boss.phase_frame < 144) {
        if(frame_in_cycle == 0) {
            laser_template.coords.angle = player_angle_from(
                laser_template.coords.origin.x, laser_template.coords.origin.y, 0x30);
            laser_fixed_spawn(exalice_laser_slot++);
            bullet_template.spawn_type = 0x10;
            bullet_template.patnum = 68;
            bullet_template.group = BG_RING;
            bullet_template.angle = randring2_next16();
            bullet_template.speed.v = to_sp(4);
            exalice_set_spread(32, 10);
            bullets_add_regular();
        } else if(frame_in_cycle == 8) {
            laser_template.coords.angle = player_angle_from(
                laser_template.coords.origin.x, laser_template.coords.origin.y,
                static_cast<unsigned char>(-0x30));
            laser_fixed_spawn(exalice_laser_slot++);
        }
    }
    exalice_laser_slot &= 0x0F;
    for(int i = 0; i < 16; i++) {
        if(lasers[i].flag == LF_FIXED_WAIT_TO_GROW) {
            lasers[i].coords.angle = (i & 1)
                ? lasers[i].coords.angle + 1 : lasers[i].coords.angle - 1;
        }
    }
    if(boss.phase_frame == 208) {
        exalice_laser_slot = 0;
        return true;
    }
    return false;
}

bool near exalice_pattern_speedup_fans(void)
{
    if((boss.phase_frame % 2) == 0) {
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.special_motion = BSM_SPEEDUP;
        bullet_special.speed_delta.v = 2;
        bullet_template.speed.v = to_sp(4);
        exalice_set_spread(7, 9);
        bullet_template.patnum = 68;
        bullet_template.origin.x.v = randring2_next16_mod(to_sp(48)) -
            to_sp(24) + bullet_template.origin.x.v;
        bullet_template.angle = 0;
        bullets_add_special();
        snd_se_play(3);
    }
    boss_flystep_random(boss.phase_frame - 100);
    return (boss.phase_frame == 128);
}

bool near exalice_pattern_sweeping_lasers(void)
{
    if(boss.phase_frame == 64) {
        laser_template.col = 2;
        laser_template.coords.width.nonshrink = 6;
        laser_template.coords.angle = 0;
        laser_template.active_at_age.grow = 30;
        laser_template.shootout_speed.v = to_sp(5.5f);
        boss_statebyte[15] = 0;
    }
    if((boss.phase_frame % 4) == 0) {
        if(boss_statebyte[15] == 0) {
            laser_template.coords.angle += 8;
            if(laser_template.coords.angle >= 128) {
                boss_statebyte[15] = 1;
            }
            lasers_shootout_add();
        } else if(boss_statebyte[15] == 1) {
            laser_template.coords.angle -= 8;
            if(laser_template.coords.angle == 0) {
                boss_statebyte[15] = 0;
            }
            lasers_shootout_add();
        }
    }
    if(boss.phase_frame >= 256) {
        boss_flystep_random((boss.phase_frame & 0x3F) - 32);
        if(boss.phase_frame >= 512 && (boss.phase_frame % 16) == 0) {
            bullet_template.spawn_type = 0x10;
            bullet_template.group = BG_RING_AIMED;
            bullet_template.angle = 0;
            bullet_template.speed.v = to_sp(4);
            exalice_set_spread(32, 10);
            bullet_template.patnum = 68;
            bullets_add_regular();
        }
    }
    return false;
}
