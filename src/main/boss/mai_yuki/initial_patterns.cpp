// Six complete natural charge/attack functions after accepted shared flight.
#include "src/main/boss/mai_yuki/initial_patterns.hpp"

void near mai_pattern_update(void)
{
    if(boss.phase_frame < 48) {
        gather_template.center = boss.pos.cur;
        gather_add_only_3stack(boss.phase_frame - 24, 9, 8);
        boss.sprite = MY_SPRITE_CHARGE;
        if(boss.phase_frame == 32) {
            snd_se_play(8);
        }
        return;
    }
    if(!mai_pattern_current()) {
        boss.sprite = MY_SPRITE_FIRE;
        return;
    }
    boss.phase_frame = 0;
    boss.mode = 0;
    boss.sprite = PAT_B4_STILL;
    boss2.sprite = PAT_B4_STILL;
}

void near yuki_pattern_update(void)
{
    if(boss.phase_frame < 48) {
        gather_template.center = boss2.pos.cur;
        gather_add_only_3stack(boss.phase_frame - 24, 9, 8);
        boss2.sprite = MY_SPRITE_CHARGE;
        return;
    }
    if(!yuki_pattern_current()) {
        boss2.sprite = MY_SPRITE_FIRE;
    }
}

bool near mai_pattern_random_crosses(void)
{
    if((boss.phase_frame % 6) == 0) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_STACK_AIMED;
        bullet_template.angle = randring2_next16_and(0x3f) - 0x20;
        bullet_template.patnum = MY_PAT_CROSS_BLUE;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_stack(2, 0.375f);
        bullet_template.speed.v = randring2_next16_and(0x1f) + to_sp(1.0f);
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(3);
    }
    if(boss.phase_frame == 128) {
        return true;
    }
    return false;
}

bool near mai_pattern_turning_fan(void)
{
    if(boss.phase_frame == 48) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN_AIMED;
        bullet_template.angle = 0;
        bullet_template.patnum = MY_PAT_V_BLUE;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_spread(16, 8);
        bullet_template.speed.v = mai_yuki_speed(3.75f);
        bullet_template_tune();
        bullets_add_special_fixedspeed();
        snd_se_play(3);
    }
    if(boss.phase_frame == 96) {
        return true;
    }
    return false;
}

bool near mai_pattern_sweeping_pellets(void)
{
    if(boss.phase_frame == 48) {
        boss_statebyte[15] = static_cast<unsigned char>(-0x10);
    }
    if((boss.phase_frame % 4) == 0) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = boss_statebyte[15];
        boss_statebyte[15] += 5;
        bullet_template.patnum = 0;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_spread(5, 10);
        bullet_template.speed.v = mai_yuki_speed(3.125f);
        bullet_template_tune();
        bullets_add_regular_fixedspeed();
        snd_se_play(3);
    }
    if(boss.phase_frame == 160) {
        return true;
    }
    return false;
}

bool near mai_pattern_small_ball_fan(void)
{
    if((boss.phase_frame % 8) == 0) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = 0x40;
        bullet_template.patnum = MY_PAT_SMALL_BALL_BLUE;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(-8);
        mai_yuki_set_spread(8, 12);
        bullet_template.speed.v = mai_yuki_speed(4.0f);
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(3);
    }
    if(boss.phase_frame == 128) {
        return true;
    }
    return false;
}
