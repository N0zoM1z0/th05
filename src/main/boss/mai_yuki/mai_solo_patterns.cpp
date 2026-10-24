// Complete natural opening patterns for the surviving Mai boss.
#include "src/main/boss/mai_yuki/mai_solo_patterns.hpp"

bool near mai_solo_widening_fans(void)
{
    int i;
    if(boss.phase_frame == 32) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.patnum = MY_PAT_SMALL_BALL_BLUE;
        bullet_template.spread = 2;
        bullet_template.angle = 0x40;
        boss.sprite = 192;
    } else if(boss.phase_frame > 32) {
        if((boss.phase_frame % 16) == 0) {
            bullet_template.spread_angle_delta = 12;
            bullet_template.speed.v = to_sp(3);
            for(i = 0; i < 8; i++) {
                bullets_add_regular();
                bullet_template.spread_angle_delta =
                    bullet_template.spread_angle_delta + 8;
                bullet_template.speed.v = bullet_template.speed.v + 6;
            }
            snd_se_play(3);
        }
        if(boss.phase_frame == 160) {
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        } else if(boss.phase_state.patterns_seen >= 2 && boss.phase_frame >= 64) {
            boss_flystep_random(boss.phase_frame % 64);
        }
    }
    return false;
}

bool near mai_solo_turning_stacks(void)
{
    if(boss.phase_frame == 32) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_STACK;
        bullet_special.turns_max = 1;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_template.patnum = MY_PAT_V_BLUE;
        bullet_template.stack = rank + 4;
        bullet_template.stack_speed_delta.v = to_sp(1);
        bullet_template.speed.v = to_sp(2);
        boss.sprite = 192;
        boss_statebyte[15] = 0x60;
    } else if(boss.phase_frame > 32) {
        if((boss.phase_frame % 16) == 0) {
            if((boss.phase_frame % 32) == 0) {
                bullet_template.angle = boss_statebyte[15];
                bullet_template_special_angle.turn_by =
                    static_cast<unsigned char>(-0x40);
            } else {
                bullet_template.angle = 0x80 - boss_statebyte[15];
                bullet_template_special_angle.turn_by = 0x40;
            }
            bullets_add_special_fixedspeed();
            boss_statebyte[15] = boss_statebyte[15] + 9;
            snd_se_play(3);
        }
        if(boss.phase_frame == 192) {
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        } else if(boss.phase_state.patterns_seen >= 2 && boss.phase_frame >= 64) {
            boss_flystep_random(boss.phase_frame % 64);
        }
    }
    return false;
}

void near mai_solo_rotating_fans(void)
{
    int frame = (boss.phase_frame - 32) % 256;
    if(frame == 0) {
        bullet_template.spawn_type =
            MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_template.patnum = MY_PAT_V_BLUE;
        mai_yuki_set_spread(3, 12);
        bullet_template.speed.v = to_sp(3);
        bullet_template.angle = 0;
        bullet_template_tune();
    }
    if(frame <= 128 && (frame % 4) == 0) {
        bullets_add_regular();
        bullet_template.angle = bullet_template.angle + 6;
    }
}
