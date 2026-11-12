// Natural source: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
/// Stage 1 Boss - Sara
/// -------------------

#pragma option -zCB1_UPDATE_TEXT -zPmain_03
#include "src/main/boss/sara/sara.hpp"
#include "src/main/boss/sara/projectile_rules.hpp"
#include "src/main/boss/sara/combat_wave_settings.hpp"


// Constants
// ---------

static const int PHASE_2_PATTERN_START_FRAME = 16;
static const int PHASE_3_PATTERN_START_FRAME = 32;

// The real five-entry compiler switch has ordinary phases 0..4.
// The initial two phase names live in the shared Boss ABI header.
static const unsigned char SARA_PHASE_BLUE_RED_WAVES = 2;
static const unsigned char SARA_PHASE_SPINNING_RINGS = 3;
static const unsigned char SARA_PHASE_LASER_CORRIDOR = 4;
static const unsigned char SARA_MODE_REPOSITION = 0;
static const unsigned char SARA_MODE_FIRST_PATTERN = 1;

// Pattern selection counts and the terminal laser-corridor timeout.
static const unsigned char SARA_WAVE_2_PATTERN_LIMIT = 32;
static const unsigned char SARA_WAVE_3_PATTERN_LIMIT = 24;
static const int SARA_LASER_CORRIDOR_TIMEOUT = 1300;

// Phase-two pursuit shortens in 12-frame steps while its current delay is
// above 12. This is a guard threshold, not a clamped minimum: 16 -> 4 is
// part of the original transition protocol.
static const int SARA_WAVE_2_FLY_DELAY_INITIAL = 64;
static const int SARA_WAVE_2_FLY_DELAY_GUARD = 12;
static const int SARA_WAVE_2_FLY_DELAY_STEP = 12;

// Phase-three spin and active attack duration are intentionally staircased.
// The final 24-frame increment can exceed the 180-frame guard (176 -> 200).
static const int SARA_WAVE_3_PATTERN_FRAMES_INITIAL = 80;
static const int SARA_WAVE_3_PATTERN_FRAMES_GUARD = 180;
static const int SARA_WAVE_3_PATTERN_FRAMES_STEP = 24;
static const int SARA_SPIN_FAST_END = 64;
static const int SARA_SPIN_HALF_SPEED_END = 96;
static const int SARA_SPIN_QUARTER_SPEED_END = 128;
static const int SARA_SPIN_EIGHTH_SPEED_END = 160;

// The final laser corridor is built before firing and widened at frame 64.
// Each named angle is a genuine additional delay point for laser rotation.
static const int SARA_LASER_CREATE_FRAME = 32;
static const int SARA_LASER_GROW_FRAME = 64;
static const int SARA_LASER_SLOWDOWN_ANGLE_A = 0x80;
static const int SARA_LASER_SLOWDOWN_ANGLE_B = 0x60;
static const int SARA_LASER_SLOWDOWN_ANGLE_C = 0x58;
static const int SARA_LASER_SLOWDOWN_ANGLE_D = 0x50;
static const int SARA_LASER_RANDOM_COUNT_STEP_FRAMES = 64;
static const int SARA_LASER_RANDOM_COUNT_LIMIT = 8;

enum sara_colors_t {
	COL_GATHER_1 = 9,
	COL_GATHER_2 = 8,
};

// Always denotes the last phase that ends with that amount of HP.
enum sara_hp_t {
	HP_TOTAL = 4650,
	HP_PHASE_2_END = 2550,
	HP_PHASE_3_END = 450,
	HP_PHASE_4_END = 0,
};
// ---------

// State
// -----

union sara_state_t {
	struct {
		/* -------------------- */ int8_t _unused_1[9];
		uint8_t fly_delay;
		uint8_t pattern_prev;
		/* -------------------- */ int8_t _unused_2;
		/* -------------------- */ int8_t _unused_3;
		unsigned char angle_stacks;
		unsigned char angle_clockwise;
		unsigned char angle_counterclockwise;
	} phase_2;

	struct {
		/* -------------------- */ int8_t _unused_1[9];
		uint8_t pattern_frames;
		uint8_t pattern_prev;
		/* -------------------- */ int8_t _unused_2;
		/* -------------------- */ int8_t _unused_3;
		SubpixelLength8 ring_speed;
		unsigned char angle_counterclockwise;
		unsigned char angle_clockwise;
	} phase_3;

	struct {
		/* -------------------- */ int8_t _unused[13];
		uint8_t laser_angle_interval;
		uint8_t random_ball_count;
		unsigned char spread_angle;
	} phase_4;
};

typedef char sara_state_is_16[(sizeof(sara_state_t) == 16) ? 1 : -1];
typedef char sara_fly_delay_at_9[(offsetof(sara_state_t, phase_2.fly_delay) == 9) ? 1 : -1];
typedef char sara_ring_speed_at_13[(offsetof(sara_state_t, phase_3.ring_speed) == 13) ? 1 : -1];
typedef char sara_spread_angle_at_15[(offsetof(sara_state_t, phase_4.spread_angle) == 15) ? 1 : -1];

#define state reinterpret_cast<sara_state_t *>(boss_statebyte)

#define phase_2_3_pattern sara_phase_2_3_pattern
extern pattern_loop_func_t phase_2_3_pattern;
// -----

static void near phase_2_with_pattern(void)
{
	if(boss.phase_frame < PHASE_2_PATTERN_START_FRAME) {
		gather_add_only_3stack(
			(boss.phase_frame - 1), COL_GATHER_1, COL_GATHER_2
		);
		if(boss.phase_frame == 1) {
			snd_se_play(SARA_CHARGE_SOUND);
			state->phase_2.angle_counterclockwise = SARA_BLUE_COUNTERCLOCKWISE_INITIAL_ANGLE;
			state->phase_2.angle_clockwise = SARA_BLUE_CLOCKWISE_INITIAL_ANGLE;
			state->phase_2.angle_stacks = SARA_RED_STACK_INITIAL_ANGLE;
		}
		return;
	}
	if(boss_flystep_random(boss.phase_frame - PHASE_2_PATTERN_START_FRAME)) {
		boss.phase_frame = 0;
		boss.mode = SARA_MODE_REPOSITION;
	}
	phase_2_3_pattern();
}

#define pattern_blue(pattern_angle, angle_delta) { \
	if((boss.phase_frame % SARA_BLUE_VOLLEY_INTERVAL) == 0) { \
		bullet_template.spawn_type = BST_CLOUD_FORWARDS; \
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE; \
		bullet_template.group = BG_SINGLE; \
		bullet_template.angle = pattern_angle; \
		bullet_template.speed.v = sara_to_sp8(SAR_BLUE_SPEED_PX); \
		bullet_template_tune(); \
		bullets_add_regular(); \
		pattern_angle = (pattern_angle + angle_delta); \
	} \
}

void near pattern_blue_curve_counterclockwise(void)
{
	pattern_blue(state->phase_2.angle_counterclockwise, SARA_BLUE_COUNTERCLOCKWISE_STEP);
}

void near pattern_blue_curve_clockwise(void)
{
	pattern_blue(state->phase_2.angle_clockwise, SARA_BLUE_CLOCKWISE_STEP);
}

void near pattern_aimed_red_spread_stack(void)
{
	if(boss.phase_frame == SARA_RED_SPREAD_FIRE_FRAME) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_BALL_RED;
		bullet_template.group = BG_SPREAD_STACK_AIMED;
		bullet_template.angle = 0;
		sara_set_spread_stack(SAR_RED_SPREAD_COUNT, SAR_RED_SPREAD_ANGLE, SAR_RED_SPREAD_STACKS, SAR_RED_SPREAD_SPEED_STEP);
		bullet_template.speed.v = sara_to_sp8(SAR_RED_BASE_SPEED_PX);
		bullet_template_tune();
		bullets_add_regular();
		snd_se_play(SAR_RED_FIRE_SOUND);
	}
}

void near pattern_red_stacks(void)
{
	if((boss.phase_frame % SARA_RED_STACK_INTERVAL) == 0) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_BALL_RED;
		bullet_template.group = BG_STACK;
		bullet_template.angle = (
			boss.angle + state->phase_2.angle_stacks - SAR_RED_STACK_BACK_ANGLE
		);
		sara_set_stack(SAR_RED_STACK_COUNT, SAR_RED_STACK_SPEED_STEP);
		bullet_template.speed.v = sara_to_sp8(SAR_RED_BASE_SPEED_PX);
		bullet_template_tune();
		bullets_add_regular();
		state->phase_2.angle_stacks -= SARA_RED_STACK_ROTATION_STEP;
		snd_se_play(SAR_RED_FIRE_SOUND);
	}
}

static void near phase_3_with_pattern(void)
{
	if(boss.phase_frame < PHASE_3_PATTERN_START_FRAME) {
		gather_add_only_3stack(
			(boss.phase_frame - 16), COL_GATHER_1, COL_GATHER_2
		);
		if(boss.phase_frame == SARA_PHASE_THREE_GATHER_FIRE_FRAME) {
			snd_se_play(SARA_CHARGE_SOUND);
			boss.sprite = PAT_SARA_SPIN;
			state->phase_3.angle_clockwise = (SARA_SPIN_CENTER_ANGLE - SARA_SPIN_SIDE_ANGLE_DELTA);
			state->phase_3.angle_counterclockwise = (SARA_SPIN_CENTER_ANGLE + SARA_SPIN_SIDE_ANGLE_DELTA);
			state->phase_3.ring_speed.v = sara_to_sp8(SAR_BLUE_SPEED_PX);
		}
		return;
	}

	if(boss.phase_frame < SARA_SPIN_FAST_END) {
		boss.sprite++;
	} else if(boss.phase_frame < SARA_SPIN_HALF_SPEED_END) {
		if((boss.phase_frame % SARA_SPIN_HALF_INTERVAL) == 0) {
			boss.sprite++;
		}
	} else if(boss.phase_frame < SARA_SPIN_QUARTER_SPEED_END) {
		if((boss.phase_frame % SARA_SPIN_QUARTER_INTERVAL) == 0) {
			boss.sprite++;
		}
	} else if((boss.phase_frame < SARA_SPIN_EIGHTH_SPEED_END)) {
		if((boss.phase_frame % SARA_SPIN_EIGHTH_INTERVAL) == 0) {
			boss.sprite++;
		}
	}

	if(boss.sprite >= (PAT_SARA_SPIN_last + 1)) {
		boss.sprite = PAT_SARA_SPIN;
	}
	phase_2_3_pattern();
	if(boss.phase_frame >= state->phase_3.pattern_frames) {
		boss.phase_frame = 0;
		boss.mode = SARA_MODE_REPOSITION;
		boss.sprite = PAT_SARA_STAY;
	}
}

void near pattern_pellet_arcs_at_expanding_random_angles(void)
{
	if((boss.phase_frame % SARA_PELLET_ARCS_FIRE_INTERVAL) == 0) {
		bullet_template.spawn_type = BST_NO_DECELERATE;
		bullet_template.patnum = 0;
		bullet_template.group = BG_SPREAD;
		bullet_template.angle = (
			randring2_next16_mod(boss.phase_frame * SAR_PELLET_RANDOM_ANGLE_SCALE) - boss.phase_frame + SAR_PELLET_CENTER_ANGLE
		);
		sara_set_spread(SAR_PELLET_SPREAD_COUNT, SAR_PELLET_SPREAD_ANGLE_STEP);
		bullet_template.special_motion = BSM_EXACT_LINEAR;
		bullet_template.speed.v = sara_rand_speed(SAR_PELLET_MIN_SPEED_PX, SAR_PELLET_MAX_SPEED_PX);
		bullet_template_tune();
		bullets_add_special();

		bullet_template.spawn_type = BST_CLOUD_BACKWARDS;
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE;
		bullet_template.group = BG_SINGLE;
		bullet_template.angle = (
			randring2_next16_mod(boss.phase_frame * SAR_PELLET_RANDOM_ANGLE_SCALE) - boss.phase_frame + SAR_PELLET_CENTER_ANGLE
		);
		bullet_template.speed.v = sara_rand_speed(SAR_BALL_MIN_SPEED_PX, SAR_BALL_MAX_SPEED_PX);
		bullet_template_tune();
		bullets_add_regular();

		snd_se_play(SARA_BULLET_SOUND);
	}
}

void near pattern_random_red_rings(void)
{
	if((boss.phase_frame % SARA_RED_RING_FIRE_INTERVAL) == 0) {
		bullet_template.spawn_type = BST_CLOUD_FORWARDS;
		bullet_template.patnum = PAT_BULLET16_N_BALL_RED;
		bullet_template.group = BG_RING;
		bullet_template.angle = randring2_next16();
		bullet_template.speed.v = sara_to_sp8(SAR_RED_RING_SPEED_PX);
		bullet_template.spread = SARA_RED_RING_PROJECTILE_COUNT;
		bullet_template_tune();
		bullets_add_regular();
		snd_se_play(SARA_BULLET_SOUND);
	}
}

#define pattern_accelerating_rings(pattern_angle, angle_delta) { \
	if((boss.phase_frame % SARA_SPIRAL_FIRE_INTERVAL) == 0) { \
		bullet_template.spawn_type = BST_NORMAL; \
		bullet_template.group = BG_RING; \
		bullet_template.spread = SARA_SPIRAL_BULLET_COUNT; \
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE; \
		bullet_template.angle = pattern_angle; \
		bullet_template.speed = state->phase_3.ring_speed; \
		if((boss.phase_frame % SARA_SPIRAL_EVERY_SECOND_FIRE) == 0) { \
			bullet_template.speed.v /= 2; \
		} \
		bullet_template_tune(); \
		bullets_add_regular(); \
		snd_se_play(SARA_BULLET_SOUND); \
		\
		pattern_angle += angle_delta; \
		state->phase_3.ring_speed.v += to_sp(SARA_SPIRAL_SPEED_INCREMENT_PX); \
	} \
}

void near pattern_accelerating_spirals_clockwise(void)
{
	pattern_accelerating_rings(state->phase_3.angle_clockwise, +0x06);
}

void near pattern_accelerating_spirals_counterclockwise(void)
{
	pattern_accelerating_rings(state->phase_3.angle_counterclockwise, -0x06);
}

void near pattern_dense_spreads_and_random_balls_within_laser_walls(void)
{
	enum {
		CORRIDOR_ANGLE = SARA_LASER_CORRIDOR_ANGLE_WIDTH, // centered around 0x40
	};

	if(boss.phase_frame == 1) {
		boss.sprite = PAT_SARA_SPIN;
	}

	if(boss.phase_frame == SARA_LASER_CREATE_FRAME) {
		laser_template.coords.origin = boss.pos.cur;
		laser_template.coords.angle = (-SARA_LASER_CORRIDOR_CENTER_ANGLE + SARA_LASER_OFFSET_ANGLE);
		laser_template.col = SARA_LASER_COLOR;
		laser_template.coords.width.nonshrink = SARA_LASER_WIDTH;
		laser_manual_fixed_spawn(X_RIGHT);

		laser_template.coords.angle = (-SARA_LASER_CORRIDOR_CENTER_ANGLE - SARA_LASER_OFFSET_ANGLE);
		laser_manual_fixed_spawn(X_LEFT);
		state->phase_4.spread_angle = SARA_LASER_INITIAL_SPREAD_ANGLE;
		state->phase_4.random_ball_count = SARA_LASER_INITIAL_BALL_COUNT;
		state->phase_4.laser_angle_interval = SARA_LASER_INITIAL_TURN_INTERVAL;
		return;
	}
	if(boss.phase_frame <= SARA_LASER_CREATE_FRAME) {
		return;
	}

	if(boss.phase_frame == SARA_LASER_GROW_FRAME) {
		laser_manual_grow(X_RIGHT);
		laser_manual_grow(X_LEFT);
	}

	if(
		((boss.phase_frame % state->phase_4.laser_angle_interval) == 0) &&
		(lasers[X_LEFT].coords.angle > (SAR_CORRIDOR_CENTER_ANGLE + (CORRIDOR_ANGLE / 2)))
	) {
		lasers[X_RIGHT].coords.angle += 0x01;
		lasers[X_LEFT].coords.angle -= 0x01;
		if(
			(lasers[X_LEFT].coords.angle == SARA_LASER_SLOWDOWN_ANGLE_A) ||
			(lasers[X_LEFT].coords.angle == SARA_LASER_SLOWDOWN_ANGLE_B) ||
			(lasers[X_LEFT].coords.angle == SARA_LASER_SLOWDOWN_ANGLE_C) ||
			(lasers[X_LEFT].coords.angle == SARA_LASER_SLOWDOWN_ANGLE_D)
		) {
			state->phase_4.laser_angle_interval++;
		}
	}

	if(stage_frame_mod16 == SAR_CORRIDOR_FIRE_TICK) {
		bullet_template.spawn_type = BST_NO_DECELERATE;
		bullet_template.angle = state->phase_4.spread_angle;
		bullet_template.group = BG_SPREAD;
		bullet_template.special_motion = BSM_EXACT_LINEAR;
		sara_set_spread_for_rank(
			SAR_CORRIDOR_SPREAD_EASY, SAR_CORRIDOR_SPREAD_STEP,
			SAR_CORRIDOR_SPREAD_NORMAL, SAR_CORRIDOR_SPREAD_STEP,
			SAR_CORRIDOR_SPREAD_HARD, SAR_CORRIDOR_SPREAD_STEP,
			SAR_CORRIDOR_SPREAD_LUNATIC, SAR_CORRIDOR_SPREAD_STEP
		);
		bullet_template.speed.v = sara_to_sp8(SAR_CORRIDOR_SPREAD_SPEED_PX);
		bullet_template.patnum = 0;
		bullets_add_special();

		bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
		bullet_template.speed.v = sara_to_sp8(SAR_CORRIDOR_BALL_SPEED_PX);
		bullet_template.spread = state->phase_4.random_ball_count;
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE;
		bullets_add_regular();

		state->phase_4.spread_angle += 0x0E;
	}

	if(
		((boss.phase_frame % SARA_LASER_RANDOM_COUNT_STEP_FRAMES) == 0) &&
		(state->phase_4.random_ball_count < SARA_LASER_RANDOM_COUNT_LIMIT)
	) {
		state->phase_4.random_ball_count++;
	}
}

extern const pattern_loop_func_t SARA_PATTERNS_PHASE_2_3[2][4];

#define phase_2_3_wait_fly_and_select_pattern( \
	pattern_prev, phase, fly_delay, patterns_max, timeout_label \
) { \
	if(boss_flystep_random(boss.phase_frame - fly_delay)) { \
		boss.phase_frame = 0; \
		boss.phase_state.patterns_seen++; \
		\
		/* Timeout condition */ \
		if(boss.phase_state.patterns_seen >= patterns_max) { \
			goto timeout_label; \
		} \
		do { \
			boss.mode = randring2_next8_mod_ge_lt(1, 5); \
		} while(boss.mode == pattern_prev); \
		pattern_prev = boss.mode; \
		phase_2_3_pattern = SARA_PATTERNS_PHASE_2_3[phase - SARA_PHASE_BLUE_RED_WAVES][boss.mode - SARA_MODE_FIRST_PATTERN]; \
	} \
}

#pragma option -a2

void pascal sara_update(void)
{
	homing_target.x = boss.pos.cur.x;
	homing_target.y = boss.pos.cur.y;
	boss.phase_frame++;
	bullet_template.spawn_type = BST_NORMAL; // ZUN bloat
	bullet_template.origin = boss.pos.cur;
	gather_template.center = boss.pos.cur;

	switch(boss.phase) {
	case PHASE_HP_FILL:
		enum {
			KEYFRAME_GATHER_SPAWN_START = (HUD_HP_FILL_FRAMES + SAR_HP_GATHER_EXTRA_DELAY),
			KEYFRAME_GATHER_SPAWN_END = (KEYFRAME_GATHER_SPAWN_START + SAR_HP_GATHER_SPAN),
		};

		if(boss.phase_frame == SAR_HP_FILL_FIRST_FRAME) {
			boss.hp = HP_TOTAL;
			boss.phase_end_hp = HP_PHASE_2_END;
		}
		boss_hittest_shots_invincible();
		if(boss.phase_frame >= KEYFRAME_GATHER_SPAWN_START) {
			if(boss.phase_frame == KEYFRAME_GATHER_SPAWN_START) {
				gather_template.center.x = boss.pos.cur.x;
				gather_template.center.y = boss.pos.cur.y;
				gather_template.radius.v = to_sp(RES_X / SAR_HP_GATHER_RADIUS_DIVISOR);
				gather_template.ring_points = SAR_HP_GATHER_POINTS;
				gather_template.angle_delta = SAR_HP_GATHER_ANGLE_STEP;
				gather_template.col = COL_GATHER_1;
			}
			if((boss.phase_frame & SAR_HP_GATHER_TICK_MASK) == 0) {
				gather_add_only();
			}
			if(boss.phase_frame == KEYFRAME_GATHER_SPAWN_START) {
				gather_template.col = COL_GATHER_2;
			}
		}

		// Timeout condition
		if(boss.phase_frame >= KEYFRAME_GATHER_SPAWN_END) {
			// Next phase
			gather_template.radius.v = to_sp(BOSS_W / SAR_POST_HP_RADIUS_DIVISOR);
			gather_template.angle_delta = SAR_POST_HP_RING_ANGLE_STEP;
			gather_template.ring_points = SAR_POST_HP_RING_POINTS;
			boss.phase++;
			boss.phase_frame = 0;
			snd_se_play(SARA_FINAL_ENTRANCE_SOUND);
			bg_render_bombing_func = sara_bg_render;
		}
		break;

	case PHASE_BOSS_ENTRANCE_BB:
		boss_hittest_shots_invincible();

		// Timeout condition
		if(boss.phase_frame >= (
			ENTRANCE_BB_TRANSITION_FRAMES_PER_CEL * TILES_BB_CELS
		)) {
			// Next phase
			boss.phase++;
			boss.phase_frame = 0;
			boss.mode = SARA_MODE_REPOSITION;
			boss.phase_state.patterns_seen = 0;
			state->phase_2.pattern_prev = -1;
			state->phase_2.fly_delay = SARA_WAVE_2_FLY_DELAY_INITIAL;

			// ZUN bloat: Already set at the end of the previous phase, and
			// it's not set at any other place.
			bg_render_bombing_func = sara_bg_render;
		}
		break;

	case SARA_PHASE_BLUE_RED_WAVES:
		switch(boss.mode) {
		case SARA_MODE_REPOSITION:
			phase_2_3_wait_fly_and_select_pattern(
				state->phase_2.pattern_prev,
				SARA_PHASE_BLUE_RED_WAVES,
				state->phase_2.fly_delay,
				SARA_WAVE_2_PATTERN_LIMIT,
				phase_2_timed_out
			);
			break;

		default:
			phase_2_with_pattern();
			if((boss.phase_frame == 0) && (state->phase_2.fly_delay > SARA_WAVE_2_FLY_DELAY_GUARD)) {
				state->phase_2.fly_delay -= SARA_WAVE_2_FLY_DELAY_STEP;
			}
			break;
		}
		if(!boss_hittest_shots()) {
			break;
		}

		// Next phase
		boss_score_bonus(SARA_PATTERN_SCORE_BONUS);
	phase_2_timed_out:
		boss_phase_next(ET_NW_SE, HP_PHASE_3_END);
		state->phase_3.pattern_frames = SARA_WAVE_3_PATTERN_FRAMES_INITIAL;
		break;

	case SARA_PHASE_SPINNING_RINGS:
		switch(boss.mode) {
		case SARA_MODE_REPOSITION:
			phase_2_3_wait_fly_and_select_pattern(
				state->phase_3.pattern_prev, SARA_PHASE_SPINNING_RINGS, 16,
				SARA_WAVE_3_PATTERN_LIMIT, phase_3_timed_out
			);
			break;

		default:
			phase_3_with_pattern();
			if(
				(boss.phase_frame == 0) &&
				(state->phase_3.pattern_frames < SARA_WAVE_3_PATTERN_FRAMES_GUARD)
			) {
				state->phase_3.pattern_frames += SARA_WAVE_3_PATTERN_FRAMES_STEP;
			}
			break;
		}
		if(!boss_hittest_shots()) {
			break;
		}

		// Next phase
		boss_score_bonus(SARA_PATTERN_SCORE_BONUS);
	phase_3_timed_out:
		boss_phase_next(ET_SW_NE, HP_PHASE_4_END);
		break;

	case SARA_PHASE_LASER_CORRIDOR:
		pattern_dense_spreads_and_random_balls_within_laser_walls();

		// Timeout condition
		if(boss.phase_frame >= SARA_LASER_CORRIDOR_TIMEOUT) {
			boss.phase_state.defeat_bonus = false;
		} else {
			// Boss defeated?
			if(!boss_hittest_shots()) {
				break;
			}
			boss.phase_state.defeat_bonus = true;
		}

		// Boss defeated
		laser_stop(SARA_LASER_STOP_RIGHT);
		laser_stop(SARA_LASER_STOP_LEFT);
		boss.phase_frame = 0;
		boss.phase = PHASE_BOSS_EXPLODE_SMALL;
		break;

	default:
		boss_defeat_update(SARA_DEFEAT_SCORE_BONUS);
		break;
	}
	hud_hp_update_and_render(boss.hp, HP_TOTAL);
}
