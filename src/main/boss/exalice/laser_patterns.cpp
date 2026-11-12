// Four complete patterns: bouncing bullets, fixed lasers and moving fans.
#pragma option -zCEXALICE_LSR_TEXT -zPmain_03
#include "src/main/boss/exalice/laser_patterns.hpp"
#include "src/main/boss/exalice/laser_attack_rules.hpp"

bool near exalice_pattern_bouncing_rings(void)
{
    if(boss.phase_frame == XLR_BOUNCE_START_FRAME) {
        bullet_template.spread = XLR_BOUNCE_INITIAL_COUNT;
    }
    if((boss.phase_frame % XLR_BOUNCE_FIRE_INTERVAL) == 0) {
        bullet_template.patnum = XLR_BOUNCE_BULLET_PATNUM;
        bullet_template.spawn_type = 0x03 | 0x10;
        bullet_template.speed.v = to_sp(XLR_BOUNCE_SPEED_PX);
        bullet_template.group = BG_RING;
        bullet_template.special_motion = BSM_BOUNCE_LEFT_RIGHT_TOP;
        if((boss.phase_frame % XLR_BOUNCE_INCREMENT_PERIOD) == 0 && bullet_template.spread < XLR_BOUNCE_MAX_COUNT) {
            bullet_template.spread++;
        }
        bullet_special.turns_max = XLR_BOUNCE_MAX_TURNS;
        bullet_template.angle += XLR_BOUNCE_ANGLE_STEP;
        bullets_add_special();
        snd_se_play(XLR_FIRE_SE);
    }
    return false;
}

bool near exalice_pattern_fixed_laser_fan(void)
{
    int frame_in_cycle = boss.phase_frame % XLR_FIXED_CYCLE_FRAMES;
    laser_template.col = XLR_FIXED_COLOR;
    laser_template.coords.width.nonshrink = XLR_FIXED_WIDTH_PX;
    laser_template.active_at_age.grow = XLR_FIXED_GROW_AGE;
    laser_template.shrink_at_age = XLR_FIXED_SHRINK_AGE;
    if(boss.phase_frame < XLR_FIXED_ACTIVE_END_FRAME) {
        if(frame_in_cycle == 0) {
            laser_template.coords.angle = player_angle_from(
                laser_template.coords.origin.x, laser_template.coords.origin.y, XLR_FIXED_ORIGIN_AIM);
            laser_fixed_spawn(exalice_laser_slot++);
            bullet_template.spawn_type = 0x10;
            bullet_template.patnum = XLR_FIXED_RING_PATNUM;
            bullet_template.group = BG_RING;
            bullet_template.angle = randring2_next16();
            bullet_template.speed.v = to_sp(XLR_FIXED_RING_SPEED_PX);
            exalice_set_spread(XLR_FIXED_RING_COUNT, XLR_FIXED_RING_STEP);
            bullets_add_regular();
        } else if(frame_in_cycle == XLR_FIXED_HALF_CYCLE) {
            laser_template.coords.angle = player_angle_from(
                laser_template.coords.origin.x, laser_template.coords.origin.y,
                static_cast<unsigned char>(XLR_FIXED_ORIGIN_AIM_LEFT));
            laser_fixed_spawn(exalice_laser_slot++);
        }
    }
    exalice_laser_slot &= XLR_FIXED_LASER_SLOT_MASK;
    for(int i = 0; i < XLR_FIXED_LASER_SLOT_COUNT; i++) {
        if(lasers[i].flag == LF_FIXED_WAIT_TO_GROW) {
            lasers[i].coords.angle = (i & 1)
                ? lasers[i].coords.angle + XLR_FIXED_TURN_STEP : lasers[i].coords.angle - XLR_FIXED_TURN_STEP;
        }
    }
    if(boss.phase_frame == XLR_FIXED_FINISH_FRAME) {
        exalice_laser_slot = 0;
        return true;
    }
    return false;
}

bool near exalice_pattern_speedup_fans(void)
{
    if((boss.phase_frame % XLR_SPEEDUP_FIRE_INTERVAL) == 0) {
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.special_motion = BSM_SPEEDUP;
        bullet_special.speed_delta.v = XLR_SPEEDUP_BULLET_STEP;
        bullet_template.speed.v = to_sp(XLR_SPEEDUP_SHOT_SPEED_PX);
        exalice_set_spread(XLR_SPEEDUP_SPREAD_COUNT, XLR_SPEEDUP_SPREAD_STEP);
        bullet_template.patnum = XLR_SPEEDUP_SPREAD_PATNUM;
        bullet_template.origin.x.v = randring2_next16_mod(to_sp(XLR_SPEEDUP_RANDOM_X_PX)) -
            to_sp(XLR_SPEEDUP_X_BIAS_PX) + bullet_template.origin.x.v;
        bullet_template.angle = 0;
        bullets_add_special();
        snd_se_play(XLR_FIRE_SE);
    }
    boss_flystep_random(boss.phase_frame - XLR_SPEEDUP_FLYSTEP_LEAD);
    return (boss.phase_frame == XLR_SPEEDUP_DONE_FRAME);
}

bool near exalice_pattern_sweeping_lasers(void)
{
    if(boss.phase_frame == XLR_SWEEP_ARM_FRAME) {
        laser_template.col = XLR_SWEEP_COLOR;
        laser_template.coords.width.nonshrink = XLR_SWEEP_WIDTH_PX;
        laser_template.coords.angle = XLR_SWEEP_ORIGIN_ANGLE;
        laser_template.active_at_age.grow = XLR_SWEEP_GROW_AGE;
        laser_template.shootout_speed.v = to_sp(XLR_SWEEP_SPEED_PX);
        boss_statebyte[15] = XLR_SWEEP_FIRST_DIRECTION;
    }
    if((boss.phase_frame % XLR_SWEEP_FIRE_INTERVAL) == 0) {
        if(boss_statebyte[15] == XLR_SWEEP_FIRST_DIRECTION) {
            laser_template.coords.angle += XLR_SWEEP_TURN_STEP;
            if(laser_template.coords.angle >= XLR_SWEEP_LIMIT_ANGLE) {
                boss_statebyte[15] = XLR_SWEEP_SECOND_DIRECTION;
            }
            lasers_shootout_add();
        } else if(boss_statebyte[15] == XLR_SWEEP_SECOND_DIRECTION) {
            laser_template.coords.angle -= XLR_SWEEP_TURN_STEP;
            if(laser_template.coords.angle == 0) {
                boss_statebyte[15] = XLR_SWEEP_FIRST_DIRECTION;
            }
            lasers_shootout_add();
        }
    }
    if(boss.phase_frame >= XLR_SWEEP_MOVE_START_FRAME) {
        boss_flystep_random((boss.phase_frame & XLR_SWEEP_MOVE_CYCLE_MASK) - XLR_SWEEP_MOVE_LEAD);
        if(boss.phase_frame >= XLR_SWEEP_RING_START_FRAME && (boss.phase_frame % XLR_SWEEP_RING_INTERVAL) == 0) {
            bullet_template.spawn_type = 0x10;
            bullet_template.group = BG_RING_AIMED;
            bullet_template.angle = 0;
            bullet_template.speed.v = to_sp(XLR_SWEEP_RING_SPEED_PX);
            exalice_set_spread(XLR_SWEEP_RING_COUNT, XLR_SWEEP_RING_SPREAD);
            bullet_template.patnum = XLR_SWEEP_RING_PATNUM;
            bullets_add_regular();
        }
    }
    return false;
}
