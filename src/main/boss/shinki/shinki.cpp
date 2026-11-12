// Natural source: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
// Original source-level optimization-barrier calls are preserved in the shared update body.
/// Stage 6 Boss - Shinki
/// ---------------------

#pragma option -zCB6_BALLS_TEXT -zPmain_03
#include "src/main/boss/shinki/shinki.hpp"
#include "src/main/boss/shinki/scratch.hpp"
#include "src/main/boss/shinki/final_spiral_timing.hpp"
#pragma codeseg B6_BALLS_TEXT main_03


// Constants
// ---------

static const int PHASE_2_3_PATTERN_START_FRAME = 32;

#include "src/main/boss/shinki/hp.inl"
// ---------

// Coordinates
// -----------

#include "src/main/boss/shinki/wing_coordinates.inl"
// -----------

// State
// -----

#define phase_2_3_pattern shinki_phase_2_3_pattern
#define wing_pattern shinki_wing_pattern
extern pattern_oneshot_func_t phase_2_3_pattern;
extern pattern_loop_func_t wing_pattern;
// -----

// Rendering
// ---------

// Renderer remains foreign; its real frame is declared in shinki.hpp.
// ---------

// Game logic
// ----------


// (#included from th05/main/boss/b6.cpp, due to alignment reasons.)


void near b6balls_add(void)
{
	subpixel_t speed = playperf_speedtune(b6ball_template.speed);
	b6ball_t near *p;
	int i;
	for((p = b6balls, i = 1); i < (1 + B6BALL_COUNT); (i++, p++)) {
		if(p->flag != B6BF_FREE) {
			continue;
		}
		p->flag = B6BF_CLOUD;
		p->pos.cur = b6ball_template.origin;
		vector2_near(p->pos.velocity, b6ball_template.angle, speed);
		p->patnum_tiny = b6ball_template.patnum_tiny;
		p->cloud_radius.v = to_sp(48.0f);
		return;
	}
}

#include "src/main/boss/shinki/balls_update_body.inl"

// The complete natural ball updater now matches the original 220-byte
// function and leads directly into the following accepted pattern group.
#pragma codeseg B6_PATTERN_A_TEXT main_03
bool near pattern_curved_rings(void)
{
	#define delta_angle boss_statebyte[15]

	if(boss.phase_frame == PHASE_2_3_PATTERN_START_FRAME) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_OUTLINED_BALL_BLUE;
		bullet_template.speed.v = sara_to_sp8(2.0f);
		bullet_template.group = BG_RING;
		bullet_template.special_motion = BSM_EXACT_LINEAR;
		bullet_template.angle = randring2_next16();
		bullet_template.spread = 16;
		delta_angle = randring2_next16_and(1) ? 0x02 : -0x02;
		bullet_template_tune();
		snd_se_play(15);
	}
	if((boss.phase_frame % 4) == 0) {
		bullets_add_special();
		bullet_template.speed.v = (bullet_template.speed.v + sara_to_sp8(0.5f));
		bullet_template.angle += delta_angle;
	}
	return (boss.phase_frame == (PHASE_2_3_PATTERN_START_FRAME + 28));

	#undef delta_angle
}

bool near pattern_dualspeed_rings(void)
{
	#define interval boss_statebyte[15]

	if(boss.phase_frame == PHASE_2_3_PATTERN_START_FRAME) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE;
		bullet_template.group = BG_RING;
		bullet_template.angle = randring2_next16();
		bullet_template.spread = 16;
		interval = select_for_rank(16, 12, 8, 4);
	}
	if((boss.phase_frame % interval) == 0) {
		vector2_at(
			bullet_template.origin,
			boss.pos.cur.x,
			boss.pos.cur.y,
			randring2_next16_mod(to_sp(32.0f)),
			bullet_template.angle
		);
		bullet_template.speed.v = sara_to_sp8(2.0f);
		bullets_add_regular();

		bullet_template.speed.v = sara_to_sp8(4.0f);
		bullet_template.angle += 0x08;
		bullets_add_regular();

		snd_se_play(3);
	}
	return (boss.phase_frame == (PHASE_2_3_PATTERN_START_FRAME + 64));

	#undef interval
}

// Begin at the original even function boundary so the later semantic switch
// table keeps its genuine compiler alignment phase without inserted bytes.
#pragma codeseg B6_UPDATE_TEXT main_03
static void near phase_2_3_with_pattern(void)
{
	if(boss.phase_frame < PHASE_2_3_PATTERN_START_FRAME) {
		gather_add_only_3stack((boss.phase_frame - 16), 7, 6);
		if(boss.phase_frame == 2) {
			boss.sprite = PAT_SHINKI_CAST;

			// ZUN bloat: What's this, part of an unused pattern? Actually,
			// it's just copy-pasted from a similar function in Yumeko's fight,
			// which does fire bullets based on that template.
			bullet_template.spawn_type = (
				BST_CLOUD_BACKWARDS | BST_NO_DECELERATE
			);
			bullet_template.patnum = PAT_BULLET16_N_BALL_RED;
			bullet_template.group = BG_RING;
			bullet_template.speed.v = sara_to_sp8(3.75f);
			bullet_template.spread = 16;
			bullet_template_tune();
			snd_se_play(8);
		}
	} else if(phase_2_3_pattern()) {
		boss.sprite = PAT_SHINKI_STILL;
		boss.phase_frame = 0;
		boss.mode = 0;
	}
}

bool near pattern_random_directional_and_kunai(void)
{
	if(boss.phase_frame == PHASE_2_3_PATTERN_START_FRAME) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.speed.v = sara_to_sp8(1.75f);
		bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
		bullet_template.spread = 3;
		bullet_template_tune();
		snd_se_play(15);
	}
	if((boss.phase_frame % 2) == 0) {
		bullet_template.patnum = PAT_BULLET16_D_BLUE;
		bullet_template.origin.x.v -= to_sp((BOSS_W / 4.0f));
		bullets_add_regular();

		bullet_template.patnum = PAT_BULLET16_V_BLUE;
		bullet_template.origin.x.v += to_sp(((BOSS_W / 4.0f) * 2.0f));
		bullets_add_regular();
	}
	return boss_flystep_random(
		boss.phase_frame - PHASE_2_3_PATTERN_START_FRAME - 32
	);
}

bool near pattern_dense_blue_stacks(void)
{
	if(boss.phase_frame == PHASE_2_3_PATTERN_START_FRAME) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE;
		bullet_template.group = BG_SPREAD_STACK_AIMED;
		bullet_template.angle = 0x00;
		sara_set_spread(2, 0x04);
		shinki_set_stack_for_rank(
			5, 0.75f,
			6, 0.75f,
			6, 0.8125f,
			7, 0.8125f
		);
		bullet_template.speed.v = sara_to_sp8(2.0f);
	}
	if((boss.phase_frame % 4) == 0) {
		bullets_add_regular();
		snd_se_play(15);
	}
	return boss_flystep_random(
		boss.phase_frame - PHASE_2_3_PATTERN_START_FRAME - 32
	);
}

bool near pattern_wing_preparation(void)
{
	enum {
		LASERS_USED = 6,
	};
	#define tone      	boss_statebyte[14]
	#define wing_frame	boss_statebyte[15]

	int i;

	if(boss.phase_frame == 16) {
		// Still assumed to be set to this value by Yumeko. Original gameplay
		// relies on this value to be < 8 to ensure that the lasers will kill
		// the player if they move to the side of the wings. (Lasers only kill
		// if they finished growing, they grow by 2 pixels every 2 frames, and
		// the ones in this pattern are kept alive for 8 frames.)
		// MODDERS: Uncomment to clearly define the original behavior.
		// laser_template.coords.width = 6;
		laser_template.coords.angle = 0x50;	laser_manual_fixed_spawn(0);
		laser_template.coords.angle = 0x48;	laser_manual_fixed_spawn(1);
		laser_template.coords.angle = 0x40;	laser_manual_fixed_spawn(2);
		laser_template.coords.angle = 0x40;	laser_manual_fixed_spawn(3);
		laser_template.coords.angle = 0x38;	laser_manual_fixed_spawn(4);
		laser_template.coords.angle = 0x30;	laser_manual_fixed_spawn(5);
		snd_se_play(8);
		boss.sprite = PAT_SHINKI_CAST;
		wing_frame = 0;
		tone = 100;
	}
	if(boss.phase_frame <= 16) {
		return false;
	}
	if(lasers[2].coords.angle < 0x80) {
		if(stage_frame_mod2) {
			lasers[0].coords.angle += 0x01;
			lasers[1].coords.angle += 0x01;
			lasers[2].coords.angle += 0x01;
			lasers[3].coords.angle -= 0x01;
			lasers[4].coords.angle -= 0x01;
			lasers[5].coords.angle -= 0x01;
			palette_settone_deferred(tone);
			tone++;
		}
		return false;
	}
	if(wing_frame == 0) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE;
		bullet_template.group = BG_SINGLE;
		bullet_template_tune();
		for(i = 0; i < 50; i++) {
			bullet_template.origin.x.v = shinki_wing_random_x();
			bullet_template.origin.y.v = shinki_wing_random_y();
			bullet_template.angle = randring2_next8_mod_ge_lt(0x10, 0x70);
			bullet_template.speed.v = sara_rand_speed(1.5f, 5.5f);
			bullets_add_regular();
		}
		boss.sprite = PAT_SHINKI_WINGS_WHITE;
		for(i = 0; i < LASERS_USED; i++) {
			laser_manual_grow(i);
		}
		snd_se_play(15);
		playfield_shake_anim_time = 8;
	} else {
		if(stage_frame_mod2) {
			palette_settone_deferred(150);
		} else {
			palette_settone_deferred(100);
		}
		if(wing_frame >= 8) {
			palette_settone_deferred(100);
			for(i = 0; i < LASERS_USED; i++) {
				laser_stop(i);
			}
			return true;
		}
	}
	wing_frame++;
	return false;

	#undef wing_frame
	#undef tone
}

void near pattern_random_rain_and_spreads_from_wings(void)
{
	if(boss.phase_frame <= 128) {
		return;
	}
	if((boss.phase_frame % 8) == 0) {
		b6ball_template.origin.x.v = randring2_next16_mod(to_sp(PLAYFIELD_W));
		b6ball_template.origin.y.v = shinki_rand_speed16(
			((2 / 23.0f) * PLAYFIELD_H), ((6 / 23.0f) * PLAYFIELD_H)
		);
		b6ball_template.angle = 0x40;
		b6ball_template.speed.v = sara_rand_speed(3.0f, 5.0f);
		b6ball_template.patnum_tiny = PAT_B6BALL_BLUE_1;
		b6balls_add();
		snd_se_play(3);
	}
	if((boss.phase_frame % 24) == 0) {
		bullet_template.origin.x.v = shinki_wing_random_x();
		bullet_template.origin.y.v = (
			boss.pos.cur.y.v - randring2_next16_mod(to_sp(BOSS_H))
		);
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE;
		bullet_template.group = BG_SPREAD_AIMED;
		bullet_template.spread = 5;
		bullet_template.spread_angle_delta = select_for_rank(
			0x10, 0x0C, 0x0A, 0x08
		);
		bullet_template.angle = 0x00;
		bullet_template.speed.v = sara_to_sp8(3.0f);
		bullet_template_tune();
		bullets_add_regular();
	}
}

#include "src/main/boss/shinki/cheeto_walls.inl"

bool near pattern_wings_to_purple(void)
{
	if(boss.phase_frame < 160) {
		return false;
	} else if(boss.phase_frame < 192) {
		if(boss.phase_frame == 128) {
			snd_se_play(8);
		}
		if(boss.phase_frame & 1) {
			boss.pos.cur.y.v += to_sp(2.0f);
		} else {
			boss.pos.cur.y.v -= to_sp(2.0f);
		}
	} else if(boss.phase_frame == 192) {
		b6ball_template.patnum_tiny = PAT_B6BALL_PURPLE;
		for(int i = 0; i < 16; i++) {
			b6ball_template.origin.x.v = shinki_wing_random_x();
			b6ball_template.origin.y.v = shinki_wing_random_y();
			b6ball_template.angle = randring2_next8_mod_ge_lt(0x20, 0x60);
			b6ball_template.speed.v = sara_rand_speed(2.0f, 6.0f);
			b6balls_add();
		}
		boss.sprite = PAT_SHINKI_WINGS_PURPLE;
		snd_se_play(15);
		playfield_shake_anim_time = 8;
	}
	return (boss.phase_frame == 200);
}

void near pattern_aimed_b6balls_and_symmetric_spreads(void)
{
	#define b6ball_interval boss_statebyte[15]

	if(boss.phase_frame <= 128) {
		return;
	}
	if(boss.phase_frame == 129) {
		b6ball_interval = select_for_rank(96, 32, 28, 24);
	}

	int spread_cycle = (boss.phase_frame % (0x40 * 2));

	if((boss.phase_frame % b6ball_interval) == 0) {
		b6ball_template.angle = player_angle_from(b6ball_template.origin.x, b6ball_template.origin.y);
		b6ball_template.speed.v = sara_to_sp8(4.0f);
		b6ball_template.patnum_tiny = PAT_B6BALL_PURPLE;
		b6balls_add();
	}
	if((boss.phase_frame % 4) == 0) {
		bullet_template.origin.x.v -= to_sp((SHINKI_WING_W / 2));
		bullet_template.group = BG_SPREAD;
		bullet_template.special_motion = BSM_EXACT_LINEAR;
		sara_set_spread(3, 0x02);
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.speed.v = sara_to_sp8(2.5f);
		bullet_template.patnum = PAT_BULLET16_V_RED;
		if(spread_cycle < 0x40) {
			bullet_template.angle = (spread_cycle * 3);
		} else {
			bullet_template.angle = (0x40 - (spread_cycle * 3));
		}
		bullets_add_special();

		bullet_template.angle = (0x80 - bullet_template.angle);
		bullet_template.origin.x.v += to_sp(SHINKI_WING_W);
		bullets_add_special();

		snd_se_play(15);
	}

	#undef b6ball_interval
}

#include "src/main/boss/shinki/devil.inl"

void near pattern_circles_and_alternating_spirals(void)
{
	#define pellet_angle	 shinki_scratch.spiral_pellet_angle
	#define red_angle   	 shinki_scratch.spiral_red_angle

	int frame_in_cycle;

	if(boss.phase_frame < SHINKI_SPIRAL_ARM_FRAME) {
		return;
	}
	if(boss.phase_frame == SHINKI_SPIRAL_ARM_FRAME) {
		b6ball_template.angle = SHINKI_SPIRAL_INITIAL_ANGLE;
		red_angle = SHINKI_SPIRAL_INITIAL_ANGLE;
		pellet_angle = SHINKI_SPIRAL_INITIAL_ANGLE;
	}
	if((boss.phase_frame % SHINKI_SPIRAL_VOLLEY_INTERVAL) == 0) {
		// Still assumed to be set to this value from pattern_devil().
		// MODDERS: Uncomment.
		// b6ball_template.speed.v = sara_to_sp8(3.75f);
		b6ball_template.patnum_tiny = PAT_B6BALL_BLUE_1;
		vector2_at(
			b6ball_template.origin,
			boss.pos.cur.x,
			boss.pos.cur.y,
			to_sp(BOSS_W),
			b6ball_template.angle
		);
		b6balls_add();

		b6ball_template.angle += SHINKI_SPIRAL_OPPOSITE_BALL_ANGLE;
		vector2_at(
			b6ball_template.origin,
			boss.pos.cur.x,
			boss.pos.cur.y,
			to_sp(BOSS_W),
			b6ball_template.angle
		);
		b6balls_add();

		b6ball_template.angle -= SHINKI_SPIRAL_BALL_ROTATE_BACK;
		snd_se_play(SHINKI_SPIRAL_VOLLEY_SE);
	}
	if(boss.phase_frame >= SHINKI_SPIRAL_RED_RINGS_BEGIN) {
		frame_in_cycle = (boss.phase_frame % SHINKI_SPIRAL_WAVE_PERIOD);
		if(((boss.phase_frame % SHINKI_SPIRAL_VOLLEY_INTERVAL) == 0) && (frame_in_cycle < SHINKI_SPIRAL_WAVE_HALF)) {
			bullet_template.spawn_type = (
				BST_CLOUD_FORWARDS | BST_NO_DECELERATE
			);
			bullet_template.group = BG_RING;
			bullet_template.angle = red_angle;
			bullet_template.patnum = PAT_BULLET16_V_RED;
			bullet_template.speed.v = sara_to_sp8(2.0f);
			bullet_template.spread = SHINKI_SPIRAL_RING_SPREAD;
			bullets_add_regular();

			red_angle -= SHINKI_SPIRAL_RED_RING_STEP;
		}
		if(boss.phase_frame >= SHINKI_SPIRAL_PELLET_RINGS_BEGIN) {
			if(((boss.phase_frame % SHINKI_SPIRAL_VOLLEY_INTERVAL) == 0) && (frame_in_cycle >= SHINKI_SPIRAL_WAVE_HALF)) {
				bullet_template.spawn_type = (
					BST_CLOUD_FORWARDS | BST_NO_DECELERATE
				);
				bullet_template.group = BG_RING;
				bullet_template.angle = pellet_angle;
				bullet_template.patnum = SHINKI_SPIRAL_PELLET_PATNUM;
				bullet_template.speed.v = sara_to_sp8(2.0f);
				bullet_template.spread = SHINKI_SPIRAL_RING_SPREAD;
				bullets_add_regular();

				pellet_angle += SHINKI_SPIRAL_PELLET_RING_STEP;
			}
		}
	}
	if(boss.phase_frame >= SHINKI_SPIRAL_FLYSTEP_BEGIN) {
		frame_in_cycle = ((boss.phase_frame - SHINKI_SPIRAL_FLYSTEP_BEGIN) % SHINKI_SPIRAL_FLYSTEP_PERIOD);
		boss_flystep_random(frame_in_cycle - SHINKI_SPIRAL_FLYSTEP_LEAD);
	}

	#undef red_angle
	#undef pellet_angle
}

void near shinki_move_float(void)
{
	#define float_direction shinki_float_direction
	extern bool float_direction;

	if(stage_frame_mod4 != SHINKI_FLOAT_UPDATE_FRAME_MOD4) {
		return;
	}
	if(float_direction == SHINKI_FLOAT_DOWNWARD) {
		boss.pos.velocity.y.v += to_sp(SHINKI_FLOAT_ACCELERATION_PX);
		if(boss.pos.velocity.y.v >= to_sp(SHINKI_FLOAT_SPEED_LIMIT_PX)) {
			float_direction++;
		}
	} else {
		boss.pos.velocity.y.v -= to_sp(SHINKI_FLOAT_ACCELERATION_PX);
		if(boss.pos.velocity.y.v <= to_sp(-SHINKI_FLOAT_SPEED_LIMIT_PX)) {
			float_direction--;
		}
	}
	boss.pos.cur.y.v += boss.pos.velocity.y.v;

	#undef float_direction
}

#pragma option -a2

void pascal shinki_update(void)
{
	// A completely unnecessary variable to differentiate between multiple
	// phases that share the same `switch` body, because [boss.phase] itself
	// is not good enough?
	// Careful, collides with [lasers_active] in pattern_devil()!
	// MODDERS: Just use [boss.phase].
	#define phase_relative shinki_scratch.wave_relative_index

	enum {
		PHASE_11_FRAMES = 16,
		SHINKI_PHASE_CURVED_RINGS = 2,
		SHINKI_PHASE_RANDOM_KUNAI = 3,
		SHINKI_PHASE_APPROACH_WINGS = 4,
		SHINKI_PHASE_WING_PREPARATION = 5,
		SHINKI_PHASE_WING_RAIN = 6,
		SHINKI_PHASE_SPREAD_WALLS = 7,
		SHINKI_PHASE_PURPLE_TRANSITION = 8,
		SHINKI_PHASE_SYMMETRIC_SPREADS = 9,
		SHINKI_PHASE_DEVIL = 10,
		SHINKI_PHASE_DEFEAT_TRANSITION = 11,
		SHINKI_PHASE_FINAL_CIRCLES = 12,
		// The two pattern dispatch states are values of the original Boss mode.
		SHINKI_MODE_FLYSTEP = 0,
		SHINKI_MODE_PATTERN = 1,
		SHINKI_FIRST_SHARED_WAVE = 0,
		SHINKI_WAVE_PATTERN_LIMIT = 16,
		SHINKI_WING_TIMEOUT_FRAMES = 3000,
		SHINKI_ALTERNATING_PATTERN_MASK = 1,
		// Palette progression follows the wing phases into the red Devil phase.
		SHINKI_WING_PALETTE_BLUE_LIMIT = 0x80,
		SHINKI_DEVIL_PALETTE_RED_LIMIT = 0x80,
		SHINKI_PALETTE_ZERO = 0,
		SHINKI_FINAL_CIRCLES_RED = 0x60,
		// Flash tone toggles on alternate frames of the defeat transition.
		SHINKI_DEFEAT_TONE_BRIGHT = 150,
		SHINKI_DEFEAT_TONE_DIM = 100,
		SHINKI_BOMB_DAMAGE_PER_FRAME = 1,
		SHINKI_PHASE_TRANSITION_SE = 13,
		SHINKI_EARLY_PATTERN_SCORE = 10,
		SHINKI_WING_PATTERN_SCORE = 25
	};

	bool16 phase_done;

	homing_target = boss.pos.cur;
	bullet_template.origin = boss.pos.cur;
	gather_template.center = boss.pos.cur;
	laser_template.coords.origin = boss.pos.cur;
	b6ball_template.origin = boss.pos.cur;

	boss.phase_frame++;

	switch(boss.phase) {
	case PHASE_HP_FILL:
		if(boss.phase_frame == 1) {
			boss.hp = HP_TOTAL;
			boss.phase_end_hp = HP_PHASE_2_END;
			shinki_gather_template_init();
			boss.sprite = PAT_SHINKI_STILL;

			// Redundant here, only needs to be part of the phase 5to6
			// transition for completeness.
			boss.pos.velocity.y.v = to_sp(0.0f);

			boss_sprite_left = PAT_SHINKI_LEFT;
			boss_sprite_right = PAT_SHINKI_RIGHT;
			boss_sprite_stay = PAT_SHINKI_STILL;
			b6balls_load();
		}
		boss_hittest_shots_invincible();

		// Timeout condition
		if(boss.phase_frame >= (HUD_HP_FILL_FRAMES + 64)) {
			// Next phase
			boss.phase_frame = 0;
			boss.phase++;
			snd_se_play(SHINKI_PHASE_TRANSITION_SE);
			bg_render_bombing_func = shinki_bg_render;
		}
		break;

	case PHASE_BOSS_ENTRANCE_BB:
		boss_hittest_shots_invincible();
		if(boss.phase_frame == (
			ENTRANCE_BB_FRAMES_PER_CEL * (TILES_BB_CELS / 2)
		)) {
			Palettes[0].set(SHINKI_PALETTE_ZERO, SHINKI_PALETTE_ZERO, SHINKI_PALETTE_ZERO);
			palette_changed = true;
		}

		// Timeout condition
		if(boss.phase_frame >= (ENTRANCE_BB_FRAMES_PER_CEL * TILES_BB_CELS)) {
			// Next phase
			boss.phase++;
			boss.mode = SHINKI_MODE_PATTERN;
			boss.phase_frame = 0;
			phase_2_3_pattern = pattern_curved_rings;
			phase_relative = 0;
		}
		break;

	case SHINKI_PHASE_CURVED_RINGS:
	case SHINKI_PHASE_RANDOM_KUNAI:
		switch(boss.mode) {
		case SHINKI_MODE_FLYSTEP:
			if(boss_flystep_random(
				boss.phase_frame - PHASE_2_3_PATTERN_START_FRAME
			)) {
				#define PATTERNS SHINKI_PATTERNS_PHASE_2_3
				extern const pattern_oneshot_func_t PATTERNS[2][2];

				boss.phase_frame = 0;
				boss.phase_state.patterns_seen++;
				boss.mode++;
				phase_2_3_pattern = PATTERNS[phase_relative][
					boss.phase_state.patterns_seen & SHINKI_ALTERNATING_PATTERN_MASK
				];

				// Timeout condition
				if(boss.phase_state.patterns_seen >= SHINKI_WAVE_PATTERN_LIMIT) {
					goto phase_2_3_timed_out;
				}

				#undef PATTERNS
			}
			break;
		case SHINKI_MODE_PATTERN:
			phase_2_3_with_pattern();
			break;
		}
		if(!boss_hittest_shots()) {
			break;
		}
		boss_score_bonus(SHINKI_EARLY_PATTERN_SCORE);

	phase_2_3_timed_out:
		// Next phase
		if(phase_relative == SHINKI_FIRST_SHARED_WAVE) {
			boss_phase_next(ET_NW_SE, HP_PHASE_3_END);
			boss.mode = SHINKI_MODE_PATTERN;
			phase_2_3_pattern = pattern_random_directional_and_kunai;
		} else {
			boss_phase_next(ET_NW_SE, HP_PHASE_6_END);
		}
		phase_relative++;
		break;

	case SHINKI_PHASE_APPROACH_WINGS:
		boss_hittest_shots();

		// Timeout condition
		if(boss_flystep_towards(
			to_sp(PLAYFIELD_W / 2), to_sp(shinki_playfield_fraction_y(5 / 23.0f))
		)) {
			// Next phase
			boss.phase++;
			boss.phase_frame = 0;
		}
		break;

	case SHINKI_PHASE_WING_PREPARATION:
		boss_hittest_shots();

		// Timeout condition
		if(pattern_wing_preparation()) {
			// Next phase
			boss.phase++;
			boss.phase_frame = 0;
			boss.pos.velocity.y.v = to_sp(0.0f);
			boss_custombullets_render = shinki_custombullets_render;
			// How generous for Yuuka players!
			boss_hitbox_radius.x.v = select_for_playchar(
				to_sp(50.0f), to_sp(35.0f), to_sp(45.0f), to_sp(50.0f)
			);
			wing_pattern = pattern_random_rain_and_spreads_from_wings;
			phase_relative = 0;
		}
		break;

	case SHINKI_PHASE_WING_RAIN:
	case SHINKI_PHASE_SPREAD_WALLS:
		if(Palettes[0].c.b < SHINKI_WING_PALETTE_BLUE_LIMIT) {
			if(stage_frame_mod16 == 0) {
				Palettes[0].c.b++;
			}
			palette_changed = true;
		}
		shinki_move_float();
		wing_pattern();

		// Timeout condition
		if(boss.phase_frame < SHINKI_WING_TIMEOUT_FRAMES) {
			if(boss_hittest_shots()) {
				boss_score_bonus(SHINKI_WING_PATTERN_SCORE);
			} else {
				break;
			}
		}

		// Next phase
		if(phase_relative == SHINKI_FIRST_SHARED_WAVE) {
			boss_phase_next(ET_SW_NE, HP_PHASE_7_END);
			wing_pattern = pattern_cheetos_within_spread_walls;
			boss.phase_frame = 0; // redundant
			phase_relative++;
		} else {
			boss_phase_next(ET_HORIZONTAL, HP_PHASE_9_END);
		}
		break;

	case SHINKI_PHASE_PURPLE_TRANSITION:
		if(Palettes[0].c.b > SHINKI_PALETTE_ZERO) {
			if(stage_frame_mod8 == 0) {
				Palettes[0].c.b--;
			}
			palette_changed = true;
		}
		boss_hittest_shots();

		// Timeout condition
		if(pattern_wings_to_purple()) {
			// Next phase
			boss.phase++;
			boss.phase_frame = 0;
			wing_pattern = pattern_aimed_b6balls_and_symmetric_spreads;
			phase_relative = 0;
		}
		break;

	case SHINKI_PHASE_SYMMETRIC_SPREADS:
	case SHINKI_PHASE_DEVIL:
		if(Palettes[0].c.b > SHINKI_PALETTE_ZERO) {
			if(stage_frame_mod8 == 0) {
				Palettes[0].c.b--;
			}
			palette_changed = true;
		} else if(Palettes[0].c.r < SHINKI_DEVIL_PALETTE_RED_LIMIT) {
			if(stage_frame_mod16 == 0) {
				Palettes[0].c.r++;
			}
			palette_changed = true;
		}
		shinki_move_float();
		wing_pattern();

		// Timeout condition
		if(boss.phase_frame < SHINKI_WING_TIMEOUT_FRAMES) {
			phase_done = boss_hittest_shots();
			// Reduce per-frame damage to 1 HP during bombs
			if(bombing) {
				boss.hp += (boss.damage_this_frame - SHINKI_BOMB_DAMAGE_PER_FRAME);
				phase_done = false;
			}
			if(!phase_done) {
				break;
			}
			boss_score_bonus(SHINKI_WING_PATTERN_SCORE);
		}

		// Next phase
		if(phase_relative == SHINKI_FIRST_SHARED_WAVE) {
			boss_phase_next(ET_SW_NE, HP_PHASE_10_END);
			shinki_wing_pattern = pattern_devil;
			boss.phase_frame = 0; // redundant
			phase_relative++;
		} else {
			boss_phase_next(ET_HORIZONTAL, HP_PHASE_12_END);
			playfield_shake_anim_time = PHASE_11_FRAMES;
			// The pattern_devil() lasers. Should ideally be stopped inside the
			// pattern, but since it's a looping one without a clear end,
			// there's no easy way with the original architecture.
			laser_stop(0);
			laser_stop(1);
			laser_stop(2);
			laser_stop(3);
		}
		break;

	case SHINKI_PHASE_DEFEAT_TRANSITION:
		boss_hittest_shots();
		if((boss.phase_frame % 2) == 0) {
			palette_settone_deferred(SHINKI_DEFEAT_TONE_BRIGHT);
		} else {
			palette_settone_deferred(SHINKI_DEFEAT_TONE_DIM);
		}

		// Timeout condition
		if(boss.phase_frame > PHASE_11_FRAMES) {
			// Next phase
			boss.phase++;
			boss.sprite = PAT_SHINKI_STILL;
			boss_hitbox_radius.x.v = to_sp(BOSS_HITBOX_DEFAULT_W);
			Palettes[0].c.r = SHINKI_FINAL_CIRCLES_RED;
			Palettes[0].c.b = 0x00;
			snd_se_play(SHINKI_PHASE_TRANSITION_SE);
		}
		break;

	case SHINKI_PHASE_FINAL_CIRCLES:
		pattern_circles_and_alternating_spirals();
		// Timeout condition
		if(boss.phase_frame < SHINKI_WING_TIMEOUT_FRAMES) {
			// Boss defeated?
			if(!boss_hittest_shots()) {
				break;
			}
			boss.phase_state.defeat_bonus = true;
		}
		// Boss defeated
		boss_explode_small(ET_VERTICAL);
		boss.phase_frame = 0;
		boss.phase = PHASE_BOSS_EXPLODE_SMALL;
		break;

	default:
		boss_defeat_update(65);
		break;
	}
	b6balls_update();
	cheetos_update();
	hud_hp_update_and_render(boss.hp, HP_TOTAL);

	#undef phase_relative
}
// ----------
