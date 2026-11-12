// Alice's real paired-puppet beam geometry and attack/score schedule.
// All values are compile-time: the original puppet/Boss storage is untouched.
#ifndef TH05_ALICE_BEAM_WEAPON_RULES_HPP
#define TH05_ALICE_BEAM_WEAPON_RULES_HPP

// The original Boss setup initializes this charge window; the near leaf
// increments it at the start of each laser cycle and compares it modulo 256.
static const int ALICE_BEAM_BURST_INITIAL_WINDOW = 160;
static const int ALICE_BEAM_ATTACK_TIMEOUT = 600;
static const int ALICE_BEAM_WAVE_BONUS = 5;

#define ABW_GATHER_RADIUS_INITIAL 64
#define ABW_SPRITE_OFFSET_INITIAL (-60)
#define ABW_WINDOW_EXTENSION 32
#define ABW_GATHER_CONTRACTION 2
#define ABW_SPRITE_FRAME_FIRST 71
#define ABW_SPRITE_FRAME_SECOND 79
#define ABW_SPRITE_STEP 2
#define ABW_BEAM_SPRITE_SE 8
#define ABW_CLOUD_FORWARD_FLAG 0x02
#define ABW_NO_DECELERATION_FLAG 0x10
#define ABW_LASER_BULLET_PATNUM 0
#define ABW_LASER_BULLET_SPEED_SUBPX (1 * 16 + 8)
#define ABW_LASER_SHOT_RADIUS_X_PX 56
#define ABW_LASER_SHOT_RADIUS_Y_PX 8
#define ABW_BEAM_CENTER_OFFSET_PX 64
#define ABW_LASER_HIT_SE 9
#define ABW_PLAYER_HIT_WIDTH_PX 128
#define ABW_PLAYER_HIT_Y_LEAD_PX 4
#define ABW_PLAYER_HIT_HEIGHT_PX 8
#define ABW_BURST_INTERVAL_FRAMES 16
#define ABW_BURST_PERIOD_FRAMES 256
#define ABW_AIMED_BULLET_PATNUM 44
#define ABW_AIMED_BULLET_BOSS_Y_OFFSET_PX (-8)
#define ABW_AIMED_BULLET_COUNT 8
#define ABW_AIMED_BULLET_SPEED_STEP 6
#define ABW_AIMED_BULLET_SPEED_PX 2
#define ABW_AIMED_BULLET_SE 3

#endif
