// Complete natural Shinki wing transition; unchanged maintained algorithm.
#pragma option -zCB6_WING_TEXT -zPmain_03
#include "src/main/boss/shinki/wing_preparation.hpp"
#pragma codeseg B6_WING_TEXT main_03
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
