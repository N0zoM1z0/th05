// Complete recovery/hold callbacks and Alice's early charged bullet patterns.
#pragma option -zCALICE_OPN_TEXT -zPmain_03
#include "src/main/boss/alice/opening_patterns.hpp"

bool pascal near alice_puppet_recover(AlicePuppet near &puppet)
{
    if(puppet.phase_frame >= 96) {
        return true;
    }
    return false;
}

bool pascal near alice_puppet_hold(AlicePuppet near &puppet)
{
    return false;
}

void near alice_pattern_opening(void)
{
    if(boss.phase_frame < 64) {
        gather_add_only_3stack(boss.phase_frame - 40, 9, 8);
        boss.sprite = 184;
        if(boss.phase_frame == 40) {
            snd_se_play(8);
        }
        return;
    }
    if(boss.phase_frame == 64) {
        bullet_template.spawn_type = 0x02;
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.spread = 2;
        bullet_template_tune();
        for(int i = 0; i < 32; i++) {
            bullet_template.patnum = ((i & 1) ? ALICE_OPENING_BALL_BLUE : 0);
            bullet_template.speed.v = randring2_next16_and(0x3F) + to_sp(0.75f);
            bullet_template.origin.x.v = randring2_next16_mod(to_sp(48)) +
                boss.pos.cur.x.v - to_sp(24);
            bullet_template.origin.y.v = randring2_next16_mod(to_sp(48)) +
                boss.pos.cur.y.v - to_sp(32);
            bullets_add_regular();
        }
        boss.sprite = 182;
        snd_se_play(15);
    }
}

void near alice_pattern_opening_cycle(void)
{
    alice_pattern_opening();
    if(boss.phase_frame == 96) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}

void near alice_pattern_ring_stack(void)
{
    if(boss.phase_frame < 64) {
        gather_add_only_3stack(boss.phase_frame - 40, 9, 8);
        boss.sprite = 184;
        if(boss.phase_frame == 40) {
            snd_se_play(8);
        }
        return;
    }
    if(boss.phase_frame == 64) {
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_RING_STACK_AIMED;
        bullet_template.patnum = ALICE_OPENING_BALL_RED;
        reinterpret_cast<uint32_t &>(bullet_template.spread) =
            28UL | (8UL << 8) | (4UL << 16) | (8UL << 24);
        bullet_template.speed.v = to_sp(1.5f);
        bullet_template.angle = 0;
        bullet_template_tune();
        bullets_add_regular();
        boss.sprite = 180;
        snd_se_play(15);
        return;
    }
    if(boss.phase_frame == 96) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}

void near alice_pattern_spread_stack(void)
{
    if(boss.phase_frame < 64) {
        gather_add_only_3stack(boss.phase_frame - 40, 9, 8);
        boss.sprite = 184;
        if(boss.phase_frame == 40) {
            snd_se_play(8);
        }
        return;
    }
    if(boss.phase_frame == 64) {
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_SPREAD_STACK_AIMED;
        bullet_template.patnum = ALICE_OPENING_BALL_BLUE;
        reinterpret_cast<uint32_t &>(bullet_template.spread) =
            7UL | (8UL << 8) | (5UL << 16) | (7UL << 24);
        bullet_template.speed.v = to_sp(1.5f);
        bullet_template.angle = 0;
        bullet_template_tune();
        bullets_add_regular();
        boss.sprite = 180;
        snd_se_play(15);
        return;
    }
    if(boss.phase_frame == 96) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}
