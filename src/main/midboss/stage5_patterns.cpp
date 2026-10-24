// Complete natural movement and pattern prefix, original MAIN16724..168F2.
#include "src/main/midboss/stage5_patterns.hpp"

bool near midboss5_flystep(void)
{
    if(midboss.phase_frame == 1) {
        if((boss_statebyte[15] == 0) || (boss_statebyte[15] == 3)) {
            midboss.pos.velocity.x.v = to_sp(-2);
        } else {
            midboss.pos.velocity.x.v = to_sp(2);
        }
        boss_statebyte[15]++;
        boss_statebyte[15] &= 3;
    }
    midboss.pos.update_seg3();
    if(midboss.phase_frame >= 32) {
        return true;
    }
    return false;
}

void near midboss5_pattern_update(void)
{
    if(midboss.phase_frame < 32) {
        gather_add_only_3stack(midboss.phase_frame - 16, 3, 2);
        if(midboss.phase_frame == 16) {
            snd_se_play(8);
        }
        if((midboss.phase_frame == 20) || (midboss.phase_frame == 24) ||
           (midboss.phase_frame == 28)) {
            midboss.sprite++;
        }
        bullet_template.angle = player_angle_from(
            midboss.pos.cur.x, midboss.pos.cur.y, 0);
        return;
    }
    if((midboss.sprite < MIDBOSS5_SPRITE_SHOOT_LAST) &&
       ((midboss.phase_frame % 4) == 0)) {
        midboss.sprite++;
    }
    if(midboss5_pattern_func()) {
        midboss.phase_frame = 0;
        boss_statebyte[14] = 0;
        midboss.sprite = MIDBOSS5_SPRITE_CHARGE;
    }
}

bool near midboss5_pattern_blue_spread(void)
{
    if((midboss.phase_frame % 4) == 0) {
        bullet_template.spawn_type =
            MIDBOSS5_SPAWN_CLOUD_FORWARDS | MIDBOSS5_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS5_PAT_BULLET_V_BLUE;
        bullet_template.speed.v = midboss5_speed(5.5f);
        bullet_template.group = BG_SPREAD;
        midboss5_set_spread(13, 7);
        bullets_add_regular();
        snd_se_play(3);
    }
    return (midboss.phase_frame >= 96);
}

bool near midboss5_pattern_green_rings(void)
{
    if((midboss.phase_frame % 4) == 0) {
        bullet_template.spawn_type = MIDBOSS5_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS5_PAT_BULLET_D_GREEN;
        bullet_template.speed.v = midboss5_speed(2.0f);
        bullet_template.group = BG_RING;
        bullet_template.spread = 16;
        bullet_template.origin.x.v +=
            randring2_next16_mod(to_sp(64)) - to_sp(32);
        bullet_template.origin.y.v +=
            randring2_next16_mod(to_sp(64)) - to_sp(32);
        bullet_template.angle = randring2_next16();
        bullets_add_regular();
        snd_se_play(3);
    }
    return (midboss.phase_frame >= 96);
}

bool near midboss5_pattern_aimed_stacks(void)
{
    if(midboss.phase_frame == 32) {
        bullet_template.spawn_type =
            MIDBOSS5_SPAWN_CLOUD_FORWARDS | MIDBOSS5_SPAWN_NO_DECELERATE;
        bullet_template.patnum = 0;
        bullet_template.group = BG_SPREAD_STACK_AIMED;
        bullet_template.angle = 0;
        midboss5_set_spread_stack(5, 10, 5, 0.375f);
        bullet_template.speed.v = midboss5_speed(2.0f);
        bullets_add_regular();
        bullet_template.group = BG_RING_STACK_AIMED;
        bullet_template.stack_speed_delta.v = midboss5_speed(0.25f);
        bullet_template.spread = 32;
        bullets_add_regular();
        snd_se_play(15);
    }
    return (midboss.phase_frame >= 64);
}
