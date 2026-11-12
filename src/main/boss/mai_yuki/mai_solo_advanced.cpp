// Three complete late Mai patterns: turning fans, revenge snow and fixed lasers.
#pragma option -zCMAI_ADV_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/mai_solo_advanced.hpp"
#include "src/main/boss/mai_yuki/solo_scratch.hpp"

// All three late attacks exit by restoring the real Boss phase clock and
// movement mode together. This is the original successful pattern result.
#define MAI_LATE_ATTACK_COMPLETE() { \
    boss.phase_frame = 0; \
    boss.mode = 0; \
    return true; \
}

// The opening laser remains at its initial angle; each remaining slot
// advances by the same signed random delta before actual fixed spawning.
#define MAI_LASER_NEXT_SLOT(slot) { \
    laser_template.coords.angle += angle_delta; \
    laser_fixed_spawn(slot); \
}

bool near mai_solo_turning_fans(void)
{
    if(boss.phase_frame == 32) {
        bullet_template.spawn_type = 0x10;
        bullet_template.group = BG_SPREAD_STACK;
        bullet_special.turns_max = 1;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_template.patnum = MY_PAT_V_BLUE;
        reinterpret_cast<uint32_t &>(bullet_template.spread) =
            2UL | (8UL << 8) | (2UL << 16) | (8UL << 24);
        bullet_template.speed.v = to_sp(3);
        boss.sprite = 192;
        bullet_template_special_angle.turn_by = static_cast<unsigned char>(-0x4A);
    } else if(boss.phase_frame > 32) {
        if((boss.phase_frame % 16) == 0) {
            bullet_template.angle = 0x80;
            bullets_add_special_fixedspeed();
            bullet_template_special_angle.turn_by = -bullet_template_special_angle.turn_by;
            bullet_template.angle = 0;
            bullets_add_special_fixedspeed();
            bullet_template_special_angle.turn_by = -bullet_template_special_angle.turn_by + 8;
            snd_se_play(3);
        }
        if(boss.phase_frame == 192) {
            MAI_LATE_ATTACK_COMPLETE();
        }
        if(boss.phase_state.patterns_seen >= 2 && boss.phase_frame >= 64) {
            boss_flystep_random(boss.phase_frame % 64);
        }
    }
    return false;
}

bool near mai_solo_revenge_snow(void)
{
    if(boss.phase_frame == 32) {
        boss.sprite = 192;
        b4ball_template.speed.v = to_sp(1.75f);
        b4ball_template.hp = 6;
        b4ball_template.revenge = true;
        b4ball_template.angle = 0x80;
        b4ball_template.patnum_tiny_base = MAI_SOLO_SNOW_SPRITE;
    } else if(boss.phase_frame > 32) {
        if(boss.phase_frame <= 128) {
            bullet_template.spawn_type = 0x10;
            bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
            bullet_template.patnum = MY_PAT_SMALL_BALL_BLUE;
            bullet_template.spread = 8;
            bullet_template.speed.v = to_sp(1.5f);
            if((boss.phase_frame % 4) == 0) {
                b4ball_template.angle = mai_solo_scratch.revenge_snow_angle;
                b4balls_add();
                mai_solo_scratch.revenge_snow_angle += mai_solo_scratch.revenge_snow_step;
                snd_se_play(3);
            }
        } else {
            mai_solo_scratch.revenge_snow_step = -mai_solo_scratch.revenge_snow_step;
            if(mai_solo_scratch.revenge_snow_step < 0x7F) {
                mai_solo_scratch.revenge_snow_angle = 0;
            } else {
                mai_solo_scratch.revenge_snow_angle = 0x80;
            }
            MAI_LATE_ATTACK_COMPLETE();
        }
    }
    return false;
}

bool near mai_solo_laser_bounce(void)
{
    int angle_delta;
    if(boss.phase_frame == 16) {
        boss.sprite = 192;
        angle_delta = randring2_next16_and(0x0F) + 0x10;
        laser_template.active_at_age.grow = 32;
        laser_template.shrink_at_age = 90;
        laser_template.coords.angle = 64 - angle_delta - (angle_delta / 2);
        laser_fixed_spawn(0);
        MAI_LASER_NEXT_SLOT(1);
        MAI_LASER_NEXT_SLOT(2);
        MAI_LASER_NEXT_SLOT(3);
        mai_solo_scratch.laser_bounce_angle = static_cast<unsigned char>(-8);
    } else if(boss.phase_frame > 32) {
        if(boss.phase_frame <= 128) {
            if((boss.phase_frame % 8) == 0) {
                bullet_template.spawn_type = 0x10;
                bullet_template.group = BG_STACK;
                bullet_template.patnum = MY_PAT_V_BLUE;
                reinterpret_cast<uint16_t &>(bullet_template.stack) = 8 | (6 << 8);
                bullet_template.speed.v = to_sp(1.5f);
                bullet_template.special_motion = BSM_BOUNCE_LEFT_RIGHT_TOP;
                bullet_special.turns_max = 1;
                bullet_template.angle = mai_solo_scratch.laser_bounce_angle;
                bullets_add_special();
                bullet_template.angle = 0x80 - mai_solo_scratch.laser_bounce_angle;
                bullets_add_special();
                mai_solo_scratch.laser_bounce_angle += 8;
                if(mai_solo_scratch.laser_bounce_angle > 0x30) {
                    mai_solo_scratch.laser_bounce_angle = static_cast<unsigned char>(-8);
                }
                snd_se_play(3);
            }
            bullet_template.spawn_type = 0x10;
            bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
            bullet_template.patnum = MY_PAT_SMALL_BALL_BLUE;
            bullet_template.spread = 6;
            bullet_template.speed.v = to_sp(1.5f);
        } else {
            MAI_LATE_ATTACK_COMPLETE();
        }
    }
    return false;
}

#undef MAI_LASER_NEXT_SLOT
#undef MAI_LATE_ATTACK_COMPLETE
