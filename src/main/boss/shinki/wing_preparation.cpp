// Complete natural Shinki wing transition; unchanged maintained algorithm.
#pragma option -zCB6_WING_TEXT -zPmain_03
#include "src/main/boss/shinki/wing_preparation.hpp"
#include "src/main/boss/shinki/scratch.hpp"
#include "src/main/boss/shinki/wing_preparation_rules.hpp"
#pragma codeseg B6_WING_TEXT main_03
bool near pattern_wing_preparation(void)
{
	enum {
		LASERS_USED = SWPREP_LASER_COUNT,
	};
	#define tone      	shinki_wing_scratch.tone.wing_palette_tone
	#define wing_frame	shinki_wing_scratch.frame.wing_animation_frame

	int i;

	if(boss.phase_frame == SWPREP_START_FRAME) {
		// Still assumed to be set to this value by Yumeko. Original gameplay
		// relies on this value to be < 8 to ensure that the lasers will kill
		// the player if they move to the side of the wings. (Lasers only kill
		// if they finished growing, they grow by 2 pixels every 2 frames, and
		// the ones in this pattern are kept alive for 8 frames.)
		// MODDERS: Uncomment to clearly define the original behavior.
		// laser_template.coords.width = 6;
		laser_template.coords.angle = SWPREP_R_OUTER_ANGLE;	laser_manual_fixed_spawn(SWPREP_R_OUTER_LASER);
		laser_template.coords.angle = SWPREP_R_INNER_ANGLE;	laser_manual_fixed_spawn(SWPREP_R_INNER_LASER);
		laser_template.coords.angle = SWPREP_R_CENTER_ANGLE;	laser_manual_fixed_spawn(SWPREP_R_CENTER_LASER);
		laser_template.coords.angle = SWPREP_L_CENTER_ANGLE;	laser_manual_fixed_spawn(SWPREP_L_CENTER_LASER);
		laser_template.coords.angle = SWPREP_L_INNER_ANGLE;	laser_manual_fixed_spawn(SWPREP_L_INNER_LASER);
		laser_template.coords.angle = SWPREP_L_OUTER_ANGLE;	laser_manual_fixed_spawn(SWPREP_L_OUTER_LASER);
		snd_se_play(SWPREP_START_SE);
		boss.sprite = PAT_SHINKI_CAST;
		wing_frame = SWPREP_WING_FIRST_FRAME;
		tone = SWPREP_BASE_TONE;
	}
	if(boss.phase_frame <= SWPREP_START_FRAME) {
		return false;
	}
	if(lasers[SWPREP_SWEEP_TEST_LASER].coords.angle < SWPREP_LASER_SWEEP_LIMIT) {
		if(stage_frame_mod2) {
			lasers[SWPREP_R_OUTER_LASER].coords.angle += 0x01;
			lasers[SWPREP_R_INNER_LASER].coords.angle += 0x01;
			lasers[SWPREP_R_CENTER_LASER].coords.angle += 0x01;
			lasers[SWPREP_L_CENTER_LASER].coords.angle -= 0x01;
			lasers[SWPREP_L_INNER_LASER].coords.angle -= 0x01;
			lasers[SWPREP_L_OUTER_LASER].coords.angle -= 0x01;
			palette_settone_deferred(tone);
			tone++;
		}
		return false;
	}
	if(wing_frame == SWPREP_WING_FIRST_FRAME) {
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_N_BALL_BLUE;
		bullet_template.group = BG_SINGLE;
		bullet_template_tune();
		for(i = 0; i < SWPREP_SPAWN_BULLET_COUNT; i++) {
			bullet_template.origin.x.v = shinki_wing_random_x();
			bullet_template.origin.y.v = shinki_wing_random_y();
			bullet_template.angle = randring2_next8_mod_ge_lt(SWPREP_RAIN_ANGLE_MIN, SWPREP_RAIN_ANGLE_END);
			bullet_template.speed.v = sara_rand_speed(SWPREP_RAIN_SPEED_MIN, SWPREP_RAIN_SPEED_MAX);
			bullets_add_regular();
		}
		boss.sprite = PAT_SHINKI_WINGS_WHITE;
		for(i = 0; i < LASERS_USED; i++) {
			laser_manual_grow(i);
		}
		snd_se_play(SWPREP_RELEASE_SE);
		playfield_shake_anim_time = SWPREP_SCREEN_SHAKE_FRAMES;
	} else {
		if(stage_frame_mod2) {
			palette_settone_deferred(SWPREP_FLASH_TONE);
		} else {
			palette_settone_deferred(SWPREP_BASE_TONE);
		}
		if(wing_frame >= SWPREP_WING_VISIBLE_FRAMES) {
			palette_settone_deferred(SWPREP_BASE_TONE);
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
