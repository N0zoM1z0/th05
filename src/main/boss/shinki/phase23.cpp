// Complete genuine private Shinki phase helper, retained as natural C++.
#pragma option -zCB6_UPDATE_TEXT -zPmain_03
#include "src/main/boss/shinki/shinki.hpp"
#pragma codeseg B6_UPDATE_TEXT main_03
static const int PHASE_2_3_PATTERN_START_FRAME = 32;
extern pattern_oneshot_func_t shinki_phase_2_3_pattern;
#define phase_2_3_pattern shinki_phase_2_3_pattern

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

#undef phase_2_3_pattern
