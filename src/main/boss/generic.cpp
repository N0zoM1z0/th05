// Natural generic TH05 boss behavior, specialized to the pinned original.
#pragma option -zCBOSS_TEXT

#include "src/main/boss/generic.hpp"

// Processes any collision between the player and boss sprites.
#pragma codeseg BOSS_COLLISION_TEXT main_03
void near boss_hittest_player(void);
#pragma codeseg BOSS_TEXT main_03

int pascal near boss_hittest_shots_damage(
	subpixel_t radius_x, subpixel_t radius_y, int se_on_hit
)
{
	shots_hittest_against_boss = true;
	int ret = shots_hittest(boss.pos.cur, radius_x, radius_y);
	if(ret) {
		snd_se_play(se_on_hit);
	}
	shots_hittest_against_boss = false;
	boss_hittest_player();
	return ret;
}

// Probably only here because the code is largely identical to the boss
// version.
int pascal near midboss_hittest_shots_damage(
	subpixel_t radius_x, subpixel_t radius_y, int se_on_hit
)
{
	shots_hittest_against_boss = true;
	// MODDERS: Just call the inline function.
	shot_hitbox_radius.x.v = radius_x;
	shot_hitbox_radius.y.v = radius_y;
	shot_hitbox_center.x.v = midboss.pos.cur.x.v;
	shot_hitbox_center.y.v = midboss.pos.cur.y.v;
	int ret = shots_hittest();
	if(ret) {
		snd_se_play(se_on_hit);
	}
	shots_hittest_against_boss = false;
	return ret;
}

bool near boss_hittest_shots(void)
{
	boss.damage_this_frame = boss_hittest_shots_damage(
		boss_hitbox_radius.x, boss_hitbox_radius.y, 4
	);
	boss.hp -= boss.damage_this_frame;
	if(boss.hp <= boss.phase_end_hp) {
		return true;
	}
	return false;
}

void near boss_hittest_shots_invincible(void)
{
	boss_hittest_shots_damage(boss_hitbox_radius.x, boss_hitbox_radius.y, 10);
}

void near boss_items_drop(void)
{
	enum {
		DROP_COUNT = 5,
		DROP_AREA_W = TO_SP(BOSS_W * 2),
		DROP_AREA_H = TO_SP(BOSS_H * 2),
	};
	enum drop_set_t {
		DS_POWER,
		DS_POINT,
		DS_COUNT,

		_drop_set_t_FORCE_INT16 = 0x7FFF
	};

	static const item_type_t BOSS_ITEM_DROPS[DS_COUNT][DROP_COUNT] = {
		// DS_POWER
		{ IT_POWER, IT_POWER, IT_BIGPOWER, IT_POWER, IT_POWER },
		// DS_POINT
		{ IT_POINT, IT_POINT,    IT_POINT, IT_POINT, IT_POINT },
	};

	int i;
	drop_set_t set;
	if(power < POWER_MAX) {
		set = DS_POWER;
	} else {
		set = DS_POINT;
	}
	subpixel_t left = (boss.pos.cur.x - (DROP_AREA_W / 2));
	subpixel_t top  = (boss.pos.cur.y - (DROP_AREA_H / 2));

	for(i = 0; i < DROP_COUNT; i++) {
		items_add(
			(left + randring2_next16_mod(DROP_AREA_W)),
			(top  + randring2_next16_mod(DROP_AREA_H)),
			BOSS_ITEM_DROPS[set][i]
		);
	}
}

void pascal near boss_phase_next(
	explosion_type_t explosion_type, int next_end_hp
)
{
	if(explosion_type != ET_NONE) {
		boss_explode_small(explosion_type);
		if(!boss_phase_timed_out) {
			bullets_clear();
			boss_items_drop();
		}
	}
	boss_phase_timed_out = true;
	boss.phase++;
	boss.phase_frame = 0;
	boss.mode = 0;
	boss.phase_state.patterns_seen = 0;
	boss.hp = boss.phase_end_hp;
	boss.phase_end_hp = next_end_hp;
}

// Separate complete natural contribution; the observed 408-byte function
// remains inexact against the full original 414-byte defeat function.
#pragma codeseg BOSS_DEFEAT_TEXT main_03
void pascal near boss_defeat_update(unsigned int bonus_units)
{
	if(boss.phase == PHASE_BOSS_EXPLODE_SMALL) {
		if(boss.phase_frame == BDF_SMALL_1) {
			boss.damage_this_frame = 0;
			boss_explode_small(ET_CIRCLE);
			snd_se_play(13);
		}
		if(boss.phase_frame == BDF_SMALL_2) {
			boss_explode_small(ET_VERTICAL);
		}
		if(boss.phase_frame == BDF_BIG) {
			boss_defeat_explode_big(ET_CIRCLE, bonus_units);
			player_invincibility_time = BOSS_DEFEAT_INVINCIBILITY_FRAMES;
		}
		homing_target.x.v = HOMING_TARGET_NONE;
		homing_target.y.v = HOMING_TARGET_NONE;
		return;
	} else if(boss.phase == PHASE_BOSS_EXPLODE_BIG) {
		if(boss.phase_frame < 12) {
			playfield_shake_x = (stage_frame_mod2 == 0) ? -4 : +4;
			playfield_shake_y = (stage_frame_mod4 <= 1) ? -4 : +4;
		}
		bg_render_bombing_func = tiles_render_all;
		slowdown_factor = 2;
		if((boss.phase_frame % 8) == 0) {
			boss.sprite++;
			if(boss.sprite >= (PAT_ENEMY_KILL_last + 1)) {
				boss.phase++; // = PHASE_NONE
				boss.phase_frame = 0;
				bombing_disabled = true;
				boss_fg_render = nullfunc_near;
			}
		}
		return;
	} // else if(boss.phase == PHASE_NONE) {
	palette_settone_deferred(60);
	if(boss.phase_frame == BDF_DIALOG) {
		resident->graze += stage_graze;
		if(stage_id != (MAIN_STAGE_COUNT - 1)) {
			dialog_animate();
			if(stage_id != STAGE_EXTRA) {
				stage_clear_bonus();
			} else {
				stage_allclear_bonus();
			}
		} else {
			stage_allclear_bonus();
		}
	} else if(boss.phase_frame == BDF_FADEOUT) {
		// This pinned original TH05 build proceeds directly to stage-score
		// storage here. The reference-only score_delta_commit call is absent.

		if(stage_id < STAGE_EXTRA) {
			for(int i = 0; i < SCORE_DIGITS; i++) {
				resident->stage_score[stage_id].digits[i] = score.digits[i];
			}
		}
		if(stage_id == (MAIN_STAGE_COUNT - 1)) {
			end_game();
		} else if(stage_id == STAGE_EXTRA) {
			end_extra();
		}
		overlay_stage_leave();
		snd_kaja_func(KAJA_SONG_FADE, 10);
	} else if(boss.phase_frame == BDF_NEXT_STAGE) {
		resident->stage++;
		quit = Q_NEXT_STAGE;
		frame_delay(1);
	}
	homing_target.x.v = HOMING_TARGET_NONE;
	homing_target.y.v = HOMING_TARGET_NONE;
}

// This whole natural 46-byte function remains unaccepted against original43.
#pragma codeseg BOSS_COLLISION_TEXT main_03
void near boss_hittest_player(void)
{
	subpixel_t delta_x = boss.pos.cur.x.v;
	subpixel_t delta_y = boss.pos.cur.y.v;
	delta_x -= player_pos.cur.x.v;
	delta_y -= player_pos.cur.y.v;

	// You probably wouldn't swap X and Y in sane code.
	if(overlap_wh_inplace_fast(
		delta_y, delta_x, to_sp(BOSS_H / 2), to_sp(BOSS_W / 2)
	)) {
		player_is_hit = true;
	}

}
