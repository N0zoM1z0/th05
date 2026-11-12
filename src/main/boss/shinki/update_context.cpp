// Genuine adjacent Devil, final pattern, float motion and complete updater.
// Only the final callback is proposed for new credit.
#pragma option -zCB6_UPDATE_TEXT -zPmain_03
#pragma codeseg MAIN_0_TEXT main_01
extern "C" int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
#pragma codeseg B6_UPDATE_TEXT main_03
#include "src/main/boss/shinki/update_standalone.hpp"
#include "src/main/boss/shinki/scratch.hpp"
#include "src/main/boss/shinki/final_spiral_timing.hpp"
#include "src/main/boss/shinki/wing_hitboxes.hpp"
#include "src/main/boss/shinki/wing_attack_rules.hpp"
#include "src/main/boss/shinki/wing_coordinates.inl"
#pragma codeseg B6_UPDATE_TEXT main_03
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
		// Keep this >255 enum value: Borland otherwise narrows the entire
		// enum and changes the parity-index AND from DX to DL.
		SHINKI_WING_TIMEOUT_FRAMES = SHW_WING_PHASE_TIMEOUT_FRAMES,
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
		if(boss.phase_frame == SHINKI_FIRST_HP_FRAME) {
			boss.hp = HP_TOTAL;
			boss.phase_end_hp = HP_PHASE_2_END;
			shinki_gather_template_init();
			boss.sprite = PAT_SHINKI_STILL;

			// Redundant here, only needs to be part of the phase 5to6
			// transition for completeness.
			boss.pos.velocity.y.v = to_sp(SHINKI_RESET_Y_VELOCITY_PX);

			boss_sprite_left = PAT_SHINKI_LEFT;
			boss_sprite_right = PAT_SHINKI_RIGHT;
			boss_sprite_stay = PAT_SHINKI_STILL;
			b6balls_load();
		}
		boss_hittest_shots_invincible();

		// Timeout condition
		if(boss.phase_frame >= (HUD_HP_FILL_FRAMES + SHINKI_HP_FILL_EXTRA_FRAMES)) {
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
			boss.pos.velocity.y.v = to_sp(SHINKI_RESET_Y_VELOCITY_PX);
			boss_custombullets_render = shinki_custombullets_render;
			// How generous for Yuuka players!
			boss_hitbox_radius.x.v = select_for_playchar(
				to_sp(SHINKI_WING_HITBOX_REIMU_PX), to_sp(SHINKI_WING_HITBOX_MARISA_PX),
                to_sp(SHINKI_WING_HITBOX_MIMA_PX), to_sp(SHINKI_WING_HITBOX_YUUKA_PX)
			);
			wing_pattern = pattern_random_rain_and_spreads_from_wings;
			phase_relative = 0;
		}
		break;

	case SHINKI_PHASE_WING_RAIN:
	case SHINKI_PHASE_SPREAD_WALLS:
		if(Palettes[0].c.b < SHINKI_WING_PALETTE_BLUE_LIMIT) {
			if(stage_frame_mod16 == SHINKI_PALETTE_BRIGHTEN_TICK) {
				Palettes[0].c.b++;
			}
			palette_changed = true;
		}
		shinki_move_float();
		wing_pattern();

		// Timeout condition
		if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES) {
			if(boss_hittest_shots()) {
				boss_score_bonus(SHINKI_WING_PATTERN_SCORE);
			} else {
				break;
			}
		}

		// Next phase
		if(phase_relative == SHW_WING_FIRST_PATTERN_INDEX) {
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
			if(stage_frame_mod8 == SHINKI_PALETTE_DARKEN_TICK) {
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
			if(stage_frame_mod8 == SHINKI_PALETTE_DARKEN_TICK) {
				Palettes[0].c.b--;
			}
			palette_changed = true;
		} else if(Palettes[0].c.r < SHINKI_DEVIL_PALETTE_RED_LIMIT) {
			if(stage_frame_mod16 == SHINKI_PALETTE_BRIGHTEN_TICK) {
				Palettes[0].c.r++;
			}
			palette_changed = true;
		}
		shinki_move_float();
		wing_pattern();

		// Timeout condition
		if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES) {
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
			laser_stop(SHINKI_DEVIL_LASER_SLOT_A);
			laser_stop(SHINKI_DEVIL_LASER_SLOT_B);
			laser_stop(SHINKI_DEVIL_LASER_SLOT_C);
			laser_stop(SHINKI_DEVIL_LASER_SLOT_D);
		}
		break;

	case SHINKI_PHASE_DEFEAT_TRANSITION:
		boss_hittest_shots();
		if((boss.phase_frame % 2) == SHINKI_DEFEAT_FLASH_EVEN_FRAME) {
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
		if(boss.phase_frame < SHW_WING_PHASE_TIMEOUT_FRAMES) {
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
		boss_defeat_update(SHINKI_DEFEAT_SCORE_BONUS);
		break;
	}
	b6balls_update();
	cheetos_update();
	hud_hp_update_and_render(boss.hp, HP_TOTAL);

	#undef phase_relative
}
