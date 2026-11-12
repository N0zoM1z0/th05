// Shared physical Alice charge/firing functions: one source for both
// the standalone 499-byte charge owner and the full 939-byte Boss context.
// The sequence is intentionally source-inline (no additional runtime call).
#define ALICE_CHARGE_GATHER_SPRITE() { \
    gather_add_only_3stack( \
        boss.phase_frame - ALICE_CHARGE_GATHER_START_FRAME, \
        ALICE_CHARGE_GATHER_FIRST_COLOR, ALICE_CHARGE_GATHER_OTHER_COLOR); \
    boss.sprite = ALICE_CHARGE_SPRITE; \
}
#define ALICE_CHARGE_SOUND_AT_START() { \
    if(boss.phase_frame == ALICE_CHARGE_GATHER_START_FRAME) { \
        snd_se_play(ALICE_CHARGE_START_SOUND); \
    } \
}
#define ALICE_CHARGE_FINISH_REPOSITION() { \
    if(boss.phase_frame == ALICE_CHARGE_FINISH_FRAME) { \
        boss.phase_frame = 0; \
        boss.mode = ALICE_CHARGE_REPOSITION_MODE; \
    } \
}

void near alice_pattern_laser_fan(void)
{
    if(boss.phase_frame < ALICE_CHARGE_GATHER_UNTIL_FRAME) {
        ALICE_CHARGE_GATHER_SPRITE();
        ALICE_CHARGE_SOUND_AT_START();
        return;
    }
    if(boss.phase_frame == ALICE_CHARGE_FIRE_FRAME) {
        laser_template.col = ALICE_LASER_FAN_COLOR;
        laser_template.coords.width.nonshrink = ALICE_LASER_FAN_WIDTH;
        laser_template.coords.origin = bullet_template.origin;
        laser_template.active_at_age.moveout = ALICE_LASER_FAN_MOVEOUT_AGE;
        laser_template.shootout_speed.v = to_sp(ALICE_LASER_FAN_SPEED_PX);
        laser_template.coords.angle = iatan2(
            player_pos.cur.y.v - laser_template.coords.origin.y.v,
            player_pos.cur.x.v - laser_template.coords.origin.x.v);
        lasers_shootout_add();
        laser_template.coords.angle += ALICE_LASER_FAN_ANGLE_STEP;
        lasers_shootout_add();
        laser_template.coords.angle -= ALICE_LASER_FAN_ANGLE_RESET;
        lasers_shootout_add();

        bullet_template.spawn_type = (
            ALICE_CHARGE_CLOUD_FORWARDS | ALICE_CHARGE_NO_DECELERATE);
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.patnum = ALICE_LASER_FAN_RANDOM_BULLET_PATNUM;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = ALICE_LASER_FAN_RANDOM_BULLET_COUNT | (ALICE_LASER_FAN_RANDOM_SPEED_DELTA << 8);
        bullet_template.speed.v = to_sp(1) + 8;
        bullet_template.angle = 0;
        bullet_template_tune();
        bullets_add_regular();
        boss.sprite = ALICE_ATTACK_SPRITE;
        return;
    }
    ALICE_CHARGE_FINISH_REPOSITION();
}

void near alice_pattern_paired_stacks(void)
{
    if(boss.phase_frame < ALICE_CHARGE_GATHER_UNTIL_FRAME) {
        ALICE_CHARGE_GATHER_SPRITE();
        alice_scratch.charge_angle = ALICE_PAIRED_STACK_INITIAL_ANGLE;
        ALICE_CHARGE_SOUND_AT_START();
        return;
    }
    if((boss.phase_frame % ALICE_PAIRED_STACK_INTERVAL) == 0) {
        bullet_template.spawn_type = (
            ALICE_CHARGE_CLOUD_FORWARDS | ALICE_CHARGE_NO_DECELERATE);
        bullet_template.group = BG_STACK_AIMED;
        bullet_template.patnum = ALICE_PAIRED_STACK_BULLET_PATNUM;
        reinterpret_cast<uint16_t &>(bullet_template.stack) = ALICE_PAIRED_STACK_BULLET_COUNT | (ALICE_PAIRED_STACK_SPEED_STEP << 8);
        bullet_template.speed.v = to_sp(1) + 8;
        bullet_template_tune();
        bullet_template.angle = alice_scratch.charge_angle;
        bullets_add_regular();
        bullet_template.angle = -bullet_template.angle;
        bullets_add_regular();
        alice_scratch.charge_angle += ALICE_PAIRED_STACK_ROTATION_STEP;
        boss.sprite = ALICE_ATTACK_SPRITE;
        snd_se_play(ALICE_PAIRED_STACK_SOUND);
    }
    ALICE_CHARGE_FINISH_REPOSITION();
}

void near alice_pattern_rotating_ring(void)
{
    if(boss.phase_frame < ALICE_CHARGE_GATHER_UNTIL_FRAME) {
        ALICE_CHARGE_GATHER_SPRITE();
        alice_scratch.charge_angle = ALICE_RING_INITIAL_ANGLE;
        ALICE_CHARGE_SOUND_AT_START();
        return;
    }
    if((boss.phase_frame % ALICE_RING_INTERVAL) == 0) {
        bullet_template.spawn_type = (
            ALICE_CHARGE_CLOUD_FORWARDS | ALICE_CHARGE_NO_DECELERATE);
        bullet_template.group = BG_RING;
        bullet_template.patnum = ALICE_RING_PATNUM;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = ALICE_RING_BULLET_COUNT | (ALICE_RING_SPEED_STEP << 8);
        bullet_template.speed.v = to_sp(2) + 8;
        bullet_template_tune();
        bullet_template.angle = alice_scratch.charge_angle;
        bullets_add_regular();
        alice_scratch.charge_angle += ALICE_RING_ROTATION_STEP;
        boss.sprite = ALICE_ATTACK_SPRITE;
        snd_se_play(ALICE_RING_SHOT_SOUND);
    }
    ALICE_CHARGE_FINISH_REPOSITION();
}

#undef ALICE_CHARGE_FINISH_REPOSITION
#undef ALICE_CHARGE_SOUND_AT_START
#undef ALICE_CHARGE_GATHER_SPRITE
