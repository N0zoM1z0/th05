// Genuine adjacent Devil, final pattern, float motion and complete updater.
// Only the final callback is proposed for new credit.
#pragma option -zCB6_UPDATE_TEXT -zPmain_03
#pragma codeseg MAIN_0_TEXT main_01
extern "C" int pascal far select_for_rank(int easy, int normal, int hard, int lunatic);
#pragma codeseg B6_UPDATE_TEXT main_03
#include "src/main/boss/shinki/update_standalone.hpp"
#include "src/main/boss/shinki/wing_coordinates.inl"
#pragma codeseg B6_UPDATE_TEXT main_03
#include "src/main/boss/shinki/devil.inl"

void near pattern_circles_and_alternating_spirals(void)
{
	#define pellet_angle	 boss_statebyte[14]
	#define red_angle   	 boss_statebyte[15]

	int frame_in_cycle;

	if(boss.phase_frame < 128) {
		return;
	}
	if(boss.phase_frame == 128) {
		b6ball_template.angle = 0x00;
		red_angle = 0x00;
		pellet_angle = 0x00;
	}
	if((boss.phase_frame % 8) == 0) {
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

		b6ball_template.angle += 0x80;
		vector2_at(
			b6ball_template.origin,
			boss.pos.cur.x,
			boss.pos.cur.y,
			to_sp(BOSS_W),
			b6ball_template.angle
		);
		b6balls_add();

		b6ball_template.angle -= 0x78;
		snd_se_play(3);
	}
	if(boss.phase_frame >= 256) {
		frame_in_cycle = (boss.phase_frame % 256);
		if(((boss.phase_frame % 8) == 0) && (frame_in_cycle < 128)) {
			bullet_template.spawn_type = (
				BST_CLOUD_FORWARDS | BST_NO_DECELERATE
			);
			bullet_template.group = BG_RING;
			bullet_template.angle = red_angle;
			bullet_template.patnum = PAT_BULLET16_V_RED;
			bullet_template.speed.v = sara_to_sp8(2.0f);
			bullet_template.spread = 12;
			bullets_add_regular();

			red_angle -= 0x02;
		}
		if(boss.phase_frame >= 512) {
			if(((boss.phase_frame % 8) == 0) && (frame_in_cycle >= 128)) {
				bullet_template.spawn_type = (
					BST_CLOUD_FORWARDS | BST_NO_DECELERATE
				);
				bullet_template.group = BG_RING;
				bullet_template.angle = pellet_angle;
				bullet_template.patnum = 0;
				bullet_template.speed.v = sara_to_sp8(2.0f);
				bullet_template.spread = 12;
				bullets_add_regular();

				pellet_angle += 0x04;
			}
		}
	}
	if(boss.phase_frame >= 720) {
		frame_in_cycle = ((boss.phase_frame - 720) % 128);
		boss_flystep_random(frame_in_cycle - 96);
	}

	#undef red_angle
	#undef pellet_angle
}

void near shinki_move_float(void)
{
	#define float_direction shinki_float_direction
	extern bool float_direction;

	if(stage_frame_mod4 != 0) {
		return;
	}
	if(float_direction == 0) {
		boss.pos.velocity.y.v += to_sp(0.0625f);
		if(boss.pos.velocity.y.v >= to_sp(1.0f)) {
			float_direction++;
		}
	} else {
		boss.pos.velocity.y.v -= to_sp(0.0625f);
		if(boss.pos.velocity.y.v <= to_sp(-1.0f)) {
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
	#define phase_relative boss_statebyte[10]

	enum {
		PHASE_11_FRAMES = 16,
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
			snd_se_play(13);
			bg_render_bombing_func = shinki_bg_render;
		}
		break;

	case PHASE_BOSS_ENTRANCE_BB:
		boss_hittest_shots_invincible();
		if(boss.phase_frame == (
			ENTRANCE_BB_FRAMES_PER_CEL * (TILES_BB_CELS / 2)
		)) {
			Palettes[0].set(0x0, 0x0, 0x0);
			palette_changed = true;
		}

		// Timeout condition
		if(boss.phase_frame >= (ENTRANCE_BB_FRAMES_PER_CEL * TILES_BB_CELS)) {
			// Next phase
			boss.phase++;
			boss.mode = 1;
			boss.phase_frame = 0;
			phase_2_3_pattern = pattern_curved_rings;
			phase_relative = 0;
		}
		break;

	case 2:
	case 3:
		switch(boss.mode) {
		case 0:
			if(boss_flystep_random(
				boss.phase_frame - PHASE_2_3_PATTERN_START_FRAME
			)) {
				#define PATTERNS SHINKI_PATTERNS_PHASE_2_3
				extern const pattern_oneshot_func_t PATTERNS[2][2];

				boss.phase_frame = 0;
				boss.phase_state.patterns_seen++;
				boss.mode++;
				phase_2_3_pattern = PATTERNS[phase_relative][
					boss.phase_state.patterns_seen & 1
				];

				// Timeout condition
				if(boss.phase_state.patterns_seen >= 16) {
					goto phase_2_3_timed_out;
				}

				#undef PATTERNS
			}
			break;
		case 1:
			phase_2_3_with_pattern();
			break;
		}
		if(!boss_hittest_shots()) {
			break;
		}
		boss_score_bonus(10);

	phase_2_3_timed_out:
		// Next phase
		if(phase_relative == 0) {
			boss_phase_next(ET_NW_SE, HP_PHASE_3_END);
			boss.mode = 1;
			phase_2_3_pattern = pattern_random_directional_and_kunai;
		} else {
			boss_phase_next(ET_NW_SE, HP_PHASE_6_END);
		}
		phase_relative++;
		break;

	case 4:
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

	case 5:
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

	case 6:
	case 7:
		if(Palettes[0].c.b < 0x80) {
			if(stage_frame_mod16 == 0) {
				Palettes[0].c.b++;
			}
			palette_changed = true;
		}
		shinki_move_float();
		wing_pattern();

		// Timeout condition
		if(boss.phase_frame < 3000) {
			if(boss_hittest_shots()) {
				boss_score_bonus(25);
			} else {
				break;
			}
		}

		// Next phase
		if(phase_relative == 0) {
			boss_phase_next(ET_SW_NE, HP_PHASE_7_END);
			wing_pattern = pattern_cheetos_within_spread_walls;
			boss.phase_frame = 0; // redundant
			phase_relative++;
		} else {
			boss_phase_next(ET_HORIZONTAL, HP_PHASE_9_END);
		}
		break;

	case 8:
		if(Palettes[0].c.b > 0x00) {
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

	case 9:
	case 10:
		if(Palettes[0].c.b > 0x00) {
			if(stage_frame_mod8 == 0) {
				Palettes[0].c.b--;
			}
			palette_changed = true;
		} else if(Palettes[0].c.r < 0x80) {
			if(stage_frame_mod16 == 0) {
				Palettes[0].c.r++;
			}
			palette_changed = true;
		}
		shinki_move_float();
		wing_pattern();

		// Timeout condition
		if(boss.phase_frame < 3000) {
			phase_done = boss_hittest_shots();
			// Reduce per-frame damage to 1 HP during bombs
			if(bombing) {
				boss.hp += (boss.damage_this_frame - 1);
				phase_done = false;
			}
			if(!phase_done) {
				break;
			}
			boss_score_bonus(25);
		}

		// Next phase
		if(phase_relative == 0) {
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

	case 11:
		boss_hittest_shots();
		if((boss.phase_frame % 2) == 0) {
			palette_settone_deferred(150);
		} else {
			palette_settone_deferred(100);
		}

		// Timeout condition
		if(boss.phase_frame > PHASE_11_FRAMES) {
			// Next phase
			boss.phase++;
			boss.sprite = PAT_SHINKI_STILL;
			boss_hitbox_radius.x.v = to_sp(BOSS_HITBOX_DEFAULT_W);
			Palettes[0].c.r = 0x60;
			Palettes[0].c.b = 0x00;
			snd_se_play(13);
		}
		break;

	case 12:
		pattern_circles_and_alternating_spirals();
		// Timeout condition
		if(boss.phase_frame < 3000) {
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
