#include "src/main/boss/mai_yuki/paired_attack_rules.hpp"
#include "src/main/boss/mai_yuki/solo_scratch.hpp"
// All seven Yuki small-ball/ring families fire from the same real muzzle:
// the second Boss position with its original positive Y offset. Keep this
// assignment in-place before each attack's distinct spread/speed settings.
#define MY_YUKI_MUZZLE() \
    bullet_template.origin.x = boss2.pos.cur.x; \
    bullet_template.origin.y.v = boss2.pos.cur.y.v + to_sp(MYR_RING_MUZZLE_Y_PX)

// Both late Cheeto attackers share the same real aiming, spawn and sound
// sequence after their character-dependent origin/side decisions.
#define MY_FIRE_AIMED_CHEETO() \
    cheeto_template.angle = player_angle_from( \
        cheeto_template.origin.x, cheeto_template.origin.y, angle); \
    cheetos_add(); \
    snd_se_play(MYR_CHEETO_SOUND)

// The paired Yuki stack volleys share the same real setup and launch;
// the small and large balls use distinct sprites, counts and spread steps.
#define MY_YUKI_STACK_BURST(sprite_id, ball_count, stack_step) { \
    bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE; \
    bullet_template.group = BG_STACK_AIMED; \
    bullet_template.angle = 0; \
    bullet_template.patnum = sprite_id; \
    MY_YUKI_MUZZLE(); \
    mai_yuki_set_stack(ball_count, stack_step); \
    bullet_template.speed.v = mai_yuki_speed(MYR_STACK_SPEED_PX); \
    bullet_template_tune(); \
    bullets_add_regular(); \
}

// Both characters prepare their actual position, tint and speed before
// choosing opposite aiming offsets in separate character-specific branches.
#define MY_PREPARE_CHEETO(position, tint) { \
    cheeto_template.origin = position; \
    cheeto_template.col = tint; \
    cheeto_template.speed.v = mai_yuki_speed(MYR_CHEETO_SPEED_PX); \
}

bool near mai_pattern_reversing_rings(void)
{
    if(boss.phase_frame == MYR_RING_START_FRAME) {
        mai_yuki_pattern_scratch.pattern_byte15.mai_shared_reversing_ring_angle = MYR_RING_MAI_ANGLE;
        mai_yuki_pattern_scratch.mai_reversing_ring_step = static_cast<unsigned char>(MYR_RING_MAI_STEP);
    }
    if((boss.phase_frame % MYR_RING_FOUR_FRAME) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.angle = mai_yuki_pattern_scratch.pattern_byte15.mai_shared_reversing_ring_angle;
        mai_yuki_pattern_scratch.pattern_byte15.mai_shared_reversing_ring_angle += mai_yuki_pattern_scratch.mai_reversing_ring_step;
        bullet_template.patnum = MY_PAT_SMALL_BALL_BLUE;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(MYR_RING_MUZZLE_Y_PX);
        bullet_template.spread = MYR_RING_COUNT;
        bullet_template.speed.v = mai_yuki_speed(MYR_RING_SPEED_PX);
        bullet_template_tune();
        bullets_add_regular();
        if((boss.phase_frame % MYR_RING_TURN_FRAME) == 0) {
            mai_yuki_pattern_scratch.pattern_byte15.mai_shared_reversing_ring_angle = mai_yuki_pattern_scratch.pattern_byte15.mai_shared_reversing_ring_angle -
                (randring2_next16_and(MYR_RING_JITTER_MASK) + MYR_RING_JITTER_OFFSET);
            mai_yuki_pattern_scratch.mai_reversing_ring_step = -mai_yuki_pattern_scratch.mai_reversing_ring_step;
        }
        snd_se_play(MYR_RING_FIRE_SOUND);
    }
    if(boss.phase_frame == MYR_RING_MAI_FINISH_FRAME) {
        return true;
    }
    return false;
}

bool near yuki_pattern_random_aimed_fan(void)
{
    if((boss.phase_frame % MYR_FAN_REPEAT_FRAMES) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_AIMED;
        bullet_template.angle = randring2_next16_and(MYR_FAN_ANGLE_MASK) - MYR_FAN_ANGLE_BIAS;
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        MY_YUKI_MUZZLE();
        mai_yuki_set_spread(MYR_FAN_COUNT, MYR_FAN_ANGLE_STEP);
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        bullet_template.speed.v = randring2_next16_and(MYR_FAN_SPEED_MASK) + to_sp(MYR_FAN_SPEED_MIN_PX);
        bullet_template_tune();
        bullets_add_special();
    }
    return false;
}

bool near yuki_pattern_random_rings(void)
{
    if((boss.phase_frame % MYR_FAN_REPEAT_FRAMES) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.angle = randring2_next16();
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        MY_YUKI_MUZZLE();
        bullet_template.spread = MYR_RANDOM_RING_COUNT;
        bullet_template.speed.v = mai_yuki_speed(MYR_RANDOM_RING_SPEED_PX);
        bullet_template_tune();
        bullets_add_regular();
    }
    return false;
}

bool near yuki_pattern_small_ball_stacks(void)
{
    if((boss.phase_frame % MYR_FAN_REPEAT_FRAMES) == 0) {
        MY_YUKI_STACK_BURST(MY_PAT_SMALL_BALL_RED, MYR_SMALL_STACK_COUNT, MYR_SMALL_STACK_STEP);
    }
    return false;
}

bool near yuki_pattern_small_ball_fan(void)
{
    if((boss.phase_frame % MYR_SMALL_FAN_INTERVAL) == 0) {
        bullet_template.spawn_type = MY_SPAWN_CLOUD_FORWARDS | MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = MYR_SMALL_FAN_ANGLE;
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        MY_YUKI_MUZZLE();
        mai_yuki_set_spread(MYR_SMALL_FAN_COUNT, MYR_SMALL_FAN_STEP);
        bullet_template.speed.v = mai_yuki_speed(MYR_SMALL_FAN_SPEED_PX);
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(MYR_SMALL_FAN_SOUND);
    }
    return false;
}

bool near yuki_pattern_ball_stacks(void)
{
    if((boss.phase_frame % MYR_BIG_STACK_INTERVAL) == 0) {
        MY_YUKI_STACK_BURST(MY_PAT_BALL_RED, MYR_BIG_STACK_COUNT, MYR_BIG_STACK_STEP);
    }
    return false;
}

bool near yuki_pattern_random_pellets(void)
{
    if((boss.phase_frame % MYR_RANDOM_PELLET_INTERVAL) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_SPREAD;
        bullet_template.angle = randring2_next16();
        bullet_template.patnum = MYR_RANDOM_PELLET_PATNUM;
        MY_YUKI_MUZZLE();
        mai_yuki_set_spread(MYR_RANDOM_PELLET_COUNT, MYR_RANDOM_PELLET_STEP);
        bullet_template.speed.v = randring2_next16_and(MYR_FAN_SPEED_MASK) + to_sp(MYR_RANDOM_PELLET_SPEED_PX);
        bullet_template_tune();
        bullets_add_regular();
    }
    return false;
}

bool near yuki_pattern_reversing_rings(void)
{
    if(boss.phase_frame == MYR_RING_START_FRAME) {
        mai_yuki_pattern_scratch.yuki_reversing_ring_angle = MYR_RING_YUKI_ANGLE;
        mai_yuki_pattern_scratch.yuki_reversing_ring_step = MYR_RING_YUKI_STEP;
    }
    if((boss.phase_frame % MYR_RING_FOUR_FRAME) == 0) {
        bullet_template.spawn_type = MY_SPAWN_NO_DECELERATE;
        bullet_template.group = BG_RING;
        bullet_template.angle = mai_yuki_pattern_scratch.yuki_reversing_ring_angle;
        mai_yuki_pattern_scratch.yuki_reversing_ring_angle += mai_yuki_pattern_scratch.yuki_reversing_ring_step;
        bullet_template.patnum = MY_PAT_SMALL_BALL_RED;
        MY_YUKI_MUZZLE();
        bullet_template.spread = MYR_RING_COUNT;
        bullet_template.speed.v = mai_yuki_speed(MYR_RING_SPEED_PX);
        bullet_template_tune();
        bullets_add_regular();
        if((boss.phase_frame % MYR_RING_TURN_FRAME) == 0) {
            mai_yuki_pattern_scratch.yuki_reversing_ring_angle = randring2_next16_and(MYR_RING_JITTER_MASK) + mai_yuki_pattern_scratch.yuki_reversing_ring_angle + MYR_RING_JITTER_OFFSET;
            mai_yuki_pattern_scratch.yuki_reversing_ring_step = -mai_yuki_pattern_scratch.yuki_reversing_ring_step;
        }
    }
    return false;
}

bool near yuki_pattern_cheetos(void)
{
    unsigned char angle;
    if((boss.phase_frame == MYR_CHEETO_FIRST_FRAME) || (boss.phase_frame == MYR_CHEETO_SECOND_FRAME)) {
        MY_PREPARE_CHEETO(boss2.pos.cur, MYR_CHEETO_YUKI_COLOR);
        if(boss.pos.cur.x.v >= boss2.pos.cur.x.v) {
            angle = MYR_CHEETO_HALF_TURN;
        } else {
            angle = static_cast<unsigned char>(MYR_CHEETO_REVERSE_TURN);
        }
        MY_FIRE_AIMED_CHEETO();
    }
    return false;
}

bool near mai_pattern_cheetos(void)
{
    unsigned char angle;
    if((boss.phase_frame == MYR_CHEETO_FIRST_FRAME) || (boss.phase_frame == MYR_CHEETO_SECOND_FRAME)) {
        MY_PREPARE_CHEETO(boss.pos.cur, MYR_CHEETO_MAI_COLOR);
        if(boss.pos.cur.x.v < boss2.pos.cur.x.v) {
            angle = MYR_CHEETO_HALF_TURN;
        } else {
            angle = static_cast<unsigned char>(MYR_CHEETO_REVERSE_TURN);
        }
        MY_FIRE_AIMED_CHEETO();
    }
    return (boss.phase_frame == MYR_CHEETO_END_FRAME);
}

#undef MY_FIRE_AIMED_CHEETO
#undef MY_YUKI_MUZZLE

#undef MY_PREPARE_CHEETO
#undef MY_YUKI_STACK_BURST
