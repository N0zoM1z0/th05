// Natural animation, movement and patterns immediately before Stage3 update.
#include "src/main/midboss/stage3_patterns.hpp"

void near midboss3_reposition(void)
{
    if((midboss.phase_frame & 3) == 0) {
        if(boss_statebyte[15] == 0) {
            midboss.sprite++;
            if(midboss.sprite >= 220) {
                midboss.sprite = 219;
                midboss.pos.cur.y.v += to_sp(12);
                midboss.pos.cur.x = player_pos.cur.x;
                if(midboss.pos.cur.x.v < to_sp(64)) {
                    midboss.pos.cur.x.v = to_sp(64);
                } else if(midboss.pos.cur.x.v > to_sp(320)) {
                    midboss.pos.cur.x.v = to_sp(320);
                }
                boss_statebyte[15]++;
            }
        } else {
            midboss.sprite--;
            if(midboss.sprite < 212) {
                midboss.sprite = 208;
                boss_statebyte[15] = 0;
                midboss.phase_frame = 0;
                boss_statebyte[14] = 0;
            }
        }
    }
}

void near midboss3_gather_charge(void)
{
    gather_add_only_3stack(midboss.phase_frame - 1, 11, 10);
    if(midboss.phase_frame == 1) {
        snd_se_play(8);
        midboss.sprite = 210;
        return;
    }
    if(midboss.phase_frame == 16) {
        midboss.sprite = 211;
    }
}

void near midboss3_pattern_1(void)
{
    if(midboss.phase_frame < 32) {
        midboss3_gather_charge();
        return;
    }
    if(midboss.phase_frame == 32) {
        bullet_template.spawn_type = MIDBOSS3_SPAWN_CLOUD_FORWARDS;
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        bullet_template.speed.v = midboss3_speed(1.5f);
        bullet_template.group = BG_SPREAD_STACK;
        midboss3_set_spread_stack(3, 16, 4, 0.5f);
        bullet_template.angle = 0x40;
    fire:
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(15);
        midboss.pos.prev.y = midboss.pos.cur.y;
        midboss.pos.cur.y.v -= to_sp(4);
        return;
    }
    if(midboss.phase_frame == 48) {
        bullet_template.patnum = MIDBOSS3_PAT_BALL_RED;
        bullet_template.speed.v = midboss3_speed(3.0f);
        midboss3_set_spread_stack(4, 5, 4, 0.5f);
        goto fire;
    }
    if(midboss.phase_frame == 64) {
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        bullet_template.speed.v = midboss3_speed(2.0f);
        midboss3_set_spread_stack(7, 10, 4, 0.5f);
        goto fire;
    }
    if(midboss.phase_frame >= 96) {
        midboss3_reposition();
    }
}

void near midboss3_pattern_2(void)
{
    if(midboss.phase_frame < 32) {
        midboss3_gather_charge();
        return;
    }
    if(midboss.phase_frame == 32) {
        bullet_template.spawn_type =
            MIDBOSS3_SPAWN_CLOUD_FORWARDS | MIDBOSS3_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        bullet_template.speed.v = midboss3_speed(1.5f);
        bullet_template.group = BG_STACK_AIMED;
        midboss3_set_stack(8, 0.5f);
        bullet_template.angle = 0;
        goto fire;
    }
    if(midboss.phase_frame == 48) {
        bullet_template.group = BG_SPREAD_STACK_AIMED;
        bullet_template.patnum = MIDBOSS3_PAT_BALL_RED;
        midboss3_set_spread_for_rank(1, 1, 2, 4, 3, 3, 4, 4);
    stack:
        midboss3_set_stack(8, 0.5f);
    fire:
        bullets_add_regular();
        snd_se_play(15);
        midboss.pos.prev.y = midboss.pos.cur.y;
        midboss.pos.cur.y.v -= to_sp(4);
        return;
    }
    if(midboss.phase_frame == 64) {
        bullet_template.patnum = MIDBOSS3_PAT_BALL_BLUE;
        midboss3_set_spread_for_rank(1, 1, 3, 5, 4, 5, 5, 4);
        goto stack;
    }
    if(midboss.phase_frame >= 96) {
        midboss3_reposition();
    }
}

void near midboss3_pattern_3(void)
{
    if(midboss.phase_frame < 32) {
        midboss3_gather_charge();
        return;
    }
    if(midboss.phase_frame == 32) {
        bullet_template.spawn_type =
            MIDBOSS3_SPAWN_CLOUD_FORWARDS | MIDBOSS3_SPAWN_NO_DECELERATE;
        bullet_template.patnum = MIDBOSS3_PAT_DIAMOND_BLUE;
        bullet_template.speed.v = midboss3_speed(3.0f);
        bullet_template.group = BG_SPREAD;
        bullet_template.spread = 16;
        bullet_template.spread_angle_delta = 8;
        bullet_template.angle = 0x40;
    fire:
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(15);
        midboss.pos.prev.y = midboss.pos.cur.y;
        midboss.pos.cur.y.v -= to_sp(4);
        return;
    }
    if(midboss.phase_frame == 48) {
        bullet_template.speed.v = midboss3_speed(3.0f);
        bullet_template.spread = 21;
        bullet_template.spread_angle_delta = 4;
        goto fire;
    }
    if(midboss.phase_frame == 64) {
        bullet_template.spread = 16;
        bullet_template.spread_angle_delta = 8;
        goto fire;
    }
    if(midboss.phase_frame >= 96) {
        midboss3_reposition();
    }
}
