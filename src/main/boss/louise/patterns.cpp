// Complete natural initial Louise charge and alternating spread/stack patterns.
#include "src/main/boss/louise/patterns.hpp"

louise_charge_state_t pascal near louise_charge_update(int end_frame)
{
    if(boss.phase_frame >= 16) {
        if(boss.phase_frame < 32) {
            boss.sprite = LOUISE_SPRITE_CHARGE;
            gather_add_only_3stack(boss.phase_frame - 16, 9, 8);
            if(boss.phase_frame == 16) {
                snd_se_play(8);
            }
        } else {
            if(boss.phase_frame == 32) {
                boss.sprite = LOUISE_SPRITE_FIRE;
                return LOUISE_CHARGE_INITIALIZE;
            }
            if(boss.phase_frame < end_frame) {
                return LOUISE_CHARGE_FIRE;
            }
            return LOUISE_CHARGE_FINISH;
        }
    }
    return LOUISE_CHARGE_INACTIVE;
}

void near louise_pattern_blue_spreads(void)
{
    switch(louise_charge_update(64)) {
    case LOUISE_CHARGE_INITIALIZE:
        bullet_template.spawn_type = BST_NORMAL;
        bullet_template.patnum = LOUISE_PAT_BALL_BLUE;
        bullet_template.group = BG_SPREAD;
        bullet_template.speed.v = boss_statebyte[10];
        louise_set_spread(5, 6);
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        boss_statebyte[15] = 1 - boss_statebyte[15];
        if(boss_statebyte[15]) {
            bullet_template.angle = 0x20;
        } else {
            bullet_template.angle = 0x60;
        }
        bullet_template_tune();
        snd_se_play(15);
        if(boss_statebyte[10] < 0x24) {
            boss_statebyte[10] += 4;
        }
        // Initialization also emits the first pair on its even frame.
    case LOUISE_CHARGE_FIRE:
        if((boss.phase_frame % 2) == 0) {
            bullets_add_regular();
            bullet_template.angle += 0x80;
            bullets_add_regular();
            if(boss_statebyte[15]) {
                bullet_template.angle += 0x87;
            } else {
                bullet_template.angle += 0x79;
            }
            bullet_template.speed.v += 4;
        }
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}

void near louise_pattern_red_stacks(void)
{
    switch(louise_charge_update(96)) {
    case LOUISE_CHARGE_INITIALIZE:
        bullet_template.spawn_type =
            LOUISE_SPAWN_CLOUD_FORWARDS | LOUISE_SPAWN_NO_DECELERATE;
        bullet_template.patnum = LOUISE_PAT_V_RED;
        bullet_template.group = BG_STACK;
        bullet_template.speed.v = louise_speed(2.0f);
        louise_set_stack_for_rank(10, 0.3125f, 12, 0.3125f,
            12, 0.375f, 14, 0.375f);
        bullet_template.angle = static_cast<unsigned char>(-0x40);
        break;
    case LOUISE_CHARGE_FIRE:
        if((boss.phase_frame % 2) == 0) {
            bullets_add_regular();
            if(boss_statebyte[15]) {
                bullet_template.angle -= 8;
            } else {
                bullet_template.angle += 8;
            }
            snd_se_play(15);
        }
        break;
    case LOUISE_CHARGE_FINISH:
        boss.mode = 0;
        boss.phase_frame = 0;
        boss.sprite = LOUISE_SPRITE_STILL;
        break;
    }
}
