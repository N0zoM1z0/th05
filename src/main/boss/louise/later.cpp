// Four complete natural patterns immediately before the original Louise update.
#include "src/main/boss/louise/later.hpp"

void near louise_pattern_mirrored_fans(void)
{
    int i;
    unsigned char saved_angle;
    if((boss.phase_frame % 32) == 0) {
        bullet_template.spawn_type = LOUISE_SPAWN_CLOUD_BACKWARDS;
        bullet_template.group = BG_SINGLE;
        bullet_template.patnum = 0;
        bullet_template_tune();
        bullet_template.speed.v = louise_speed(3.0f);
        if((boss.phase_frame % 64) == 0) {
            bullet_template.angle = 0x24;
            for(i = 0; i < 8; i++) {
                saved_angle = bullet_template.angle;
                bullets_add_regular();
                bullet_template.angle += 0x80;
                bullets_add_regular();
                bullet_template.angle = 0x40 - bullet_template.angle;
                bullets_add_regular();
                bullet_template.angle += 0x80;
                bullets_add_regular();
                bullet_template.angle = saved_angle;
                bullet_template.speed.v = bullet_template.speed.v + static_cast<subpixel_length_8_t>(-louise_speed(0.3125f));
                bullet_template.angle += 8;
            }
        } else {
            bullet_template.angle = 0x64;
            for(i = 0; i < 8; i++) {
                saved_angle = bullet_template.angle;
                bullets_add_regular();
                bullet_template.angle += 0x80;
                bullets_add_regular();
                bullet_template.angle = 0xc0 - bullet_template.angle;
                bullets_add_regular();
                bullet_template.angle += 0x80;
                bullets_add_regular();
                bullet_template.angle = saved_angle;
                bullet_template.speed.v = bullet_template.speed.v + static_cast<subpixel_length_8_t>(-louise_speed(0.3125f));
                bullet_template.angle += 8;
            }
        }
    }
}

void near louise_pattern_sweeping_lasers(void)
{
    switch(louise_charge_update(128)) {
    case LOUISE_CHARGE_INITIALIZE:
        laser_template.coords.origin = boss.pos.cur;
        laser_template.coords.width.nonshrink = 6;
        laser_template.col = 8;
        laser_template.coords.angle = static_cast<unsigned char>(-16);
        laser_template.active_at_age.moveout = 30;
        laser_template.shootout_speed.v = to_sp(6.5f);
        boss_statebyte[15] = randring2_next16_and(1);
        // Initialization also launches at its real even four-frame boundary.
    case LOUISE_CHARGE_FIRE:
        if((laser_template.coords.angle >= 0xf0) ||
           (laser_template.coords.angle <= 0x80)) {
            if((boss.phase_frame % 4) == 0) {
                if(boss_statebyte[15]) {
                    lasers_shootout_add();
                } else {
                    laser_template.coords.angle = 0x80 - laser_template.coords.angle;
                    lasers_shootout_add();
                    laser_template.coords.angle = 0x80 - laser_template.coords.angle;
                }
                laser_template.coords.angle += 10;
            }
        }
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}

void near louise_pattern_turning_rings(void)
{
    switch(louise_charge_update(64)) {
    case LOUISE_CHARGE_INITIALIZE:
        bullet_template.spawn_type =
            LOUISE_SPAWN_CLOUD_FORWARDS | LOUISE_SPAWN_NO_DECELERATE;
        bullet_template.patnum = LOUISE_PAT_V_RED;
        bullet_template.group = BG_RING_STACK_AIMED;
        bullet_template.speed.v = boss_statebyte[10];
        if(boss_statebyte[10] < 0x20) {
            boss_statebyte[10] += 4;
        }
        louise_set_spread_stack(24, 8, 5, 0.5625f);
        bullet_template.angle = 0;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_special.turns_max = 1;
        if(randring2_next16_and(1)) {
            bullet_template_special_angle.turn_by = 0x20;
        } else {
            bullet_template_special_angle.turn_by = static_cast<unsigned char>(-0x20);
        }
        bullet_template_tune();
        snd_se_play(15);
        bullets_add_special();
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}

void near louise_pattern_aimed_pellets(void)
{
    if((boss.phase_frame % 32) == 0) {
        bullet_template.spawn_type =
            LOUISE_SPAWN_CLOUD_FORWARDS | LOUISE_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.patnum = 0;
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        bullet_template.speed.v = louise_speed(2.0f);
        louise_set_spread(32, 2);
        bullet_template_tune();
        if((boss.phase_frame % 64) == 0) {
            bullet_template.angle = 0x1f;
        } else {
            bullet_template.angle = static_cast<unsigned char>(-0x1f);
        }
        bullets_add_special();
        snd_se_play(3);
    }
}
