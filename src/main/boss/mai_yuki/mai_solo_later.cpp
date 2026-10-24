// Complete rotating rings and snowball algorithms, with actual shared state.
#include "src/main/boss/mai_yuki/mai_solo_later.hpp"

void near mai_solo_rotating_rings(void)
{
    int frame = (boss.phase_frame - 32) % 256;
    if(frame == 0) {
        bullet_template.spawn_type =
            MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_template.patnum = MY_PAT_V_BLUE;
        bullet_template.spread = 24;
        bullet_template.speed.v = to_sp(3);
        bullet_template.angle = 0;
        bullet_template_tune();
    }
    if(frame <= 128 && (frame % 16) == 0) {
        bullets_add_regular();
        bullet_template.angle++;
    }
}

void near mai_solo_snow_rings(void)
{
    int frame = (boss.phase_frame - 32) % 256;
    if(frame == 0) {
        b4ball_template.speed.v = to_sp(3);
        b4ball_template.angle = 0x80;
        b4ball_template.hp = 24;
        b4ball_template.revenge = true;
        b4ball_template.patnum_tiny_base = MAI_SOLO_SNOW_SPRITE;
        bullet_template.spawn_type =
            MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RANDOM_ANGLE;
        bullet_template.patnum = 0;
        bullet_template.spread = 4;
        bullet_template.speed.v = to_sp(2);
        bullet_template_tune();
    }
    if(frame <= 128 && (frame % 16) == 0) {
        b4ball_template.angle = b4ball_template.angle + 0x10;
        b4balls_add();
        b4ball_template.angle = b4ball_template.angle +
            static_cast<unsigned char>(-0x10);
        b4balls_add();
        b4ball_template.angle = b4ball_template.angle +
            static_cast<unsigned char>(-0x10);
        b4balls_add();
        b4ball_template.angle = b4ball_template.angle + 4;
    }
}

bool near mai_solo_fans_and_snow(void)
{
    int i;
    if(boss.phase_frame == 32) {
        boss.sprite = 192;
        b4ball_template.speed.v = to_sp(3);
        b4ball_template.hp = 24;
        b4ball_template.revenge = true;
        b4ball_template.patnum_tiny_base = MAI_SOLO_SNOW_SPRITE;
    } else if(boss.phase_frame > 32) {
        if((boss.phase_frame % 16) == 0) {
            bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
            bullet_template.group = BG_SPREAD;
            bullet_template.patnum = MAI_SOLO_OUTLINED_BALL_BLUE;
            bullet_template.spread = 2;
            bullet_template.angle = 0x40;
            bullet_template.spread_angle_delta = 12;
            bullet_template.speed.v = to_sp(3);
            for(i = 0; i < 8; i++) {
                bullets_add_regular();
                bullet_template.spread_angle_delta =
                    bullet_template.spread_angle_delta + 8;
                bullet_template.speed.v = bullet_template.speed.v + 6;
            }
            snd_se_play(3);
            bullet_template.group = BG_RANDOM_ANGLE;
            bullet_template.patnum = 0;
            bullet_template.spread = 3;
            bullet_template.speed.v = to_sp(2);
            if((boss.phase_frame % 32) == 0) {
                b4ball_template.angle = player_angle_from(
                    b4ball_template.origin.x, b4ball_template.origin.y, 0x20);
                b4balls_add();
                b4ball_template.angle = b4ball_template.angle +
                    static_cast<unsigned char>(-0x20);
                b4balls_add();
                b4ball_template.angle = b4ball_template.angle +
                    static_cast<unsigned char>(-0x20);
                b4balls_add();
            }
        }
        if(boss.phase_frame == 224) {
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        } else if(boss.phase_state.patterns_seen >= 2 && boss.phase_frame >= 64) {
            boss_flystep_random(boss.phase_frame % 64);
        }
    }
    return false;
}
