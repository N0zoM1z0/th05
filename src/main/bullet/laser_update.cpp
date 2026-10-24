// Natural semantic ReC98 b6ba5b0a TH05 laser state machine.
#pragma option -zCLASER_UPDATE_TEXT -zPmain_01 -G
#include "src/main/bullet/update.hpp"
#include "src/main/bullet/laser.hpp"
#pragma codeseg LASER_UPDATE_TEXT main_01
void near lasers_update(void);
void pascal near laser_hittest(Laser near &laser);

// ZUN bloat: Needed to circumvent 16-bit promotion in comparisons.
inline signed char laser_width_min(void) {
	return 1;
}

void near lasers_update(void)
{
	#define shootout_update(laser) { \
		if(laser->coords.starts_at_distance < LASER_DISTANCE_MAX) { \
			laser->coords.ends_at_distance.v += laser->shootout_speed.v; \
		} \
		if(laser->age >= laser->active_at_age.moveout) { \
			laser->coords.starts_at_distance.v += laser->shootout_speed.v; \
		} \
	}

	Laser near *laser;
	int i;
	for((laser = lasers, i = 0); i < LASER_COUNT; (i++, laser++)) {
		if(laser->flag == LF_FREE) {
			continue;
		}

		if(bullet_clear_time || bullet_zap.active) {
			if(laser->flag == LF_SHOOTOUT) {
				laser->flag = LF_SHOOTOUT_DECAY;
				laser->shootout_speed.v /= 2;
			}
		}

		switch(laser->flag) {
		case LF_SHOOTOUT:
			shootout_update(laser);
			laser_hittest(*laser);
			break;

		case LF_FIXED_WAIT_TO_GROW:
			if(laser->active_at_age.grow > 0) {
				if(laser->age >= laser->active_at_age.grow) {
					// laser->flag = LF_FIXED_GROW;
					static_cast<uint8_t>(laser->flag)++;
					snd_se_play(6);
				}
			}
			break;

		case LF_FIXED_GROW:
			if(laser->age & 1) {
				laser->coords.width.nonshrink += 2;
			}
			if(laser->coords.width.nonshrink >= laser->grow_to_width) {
				// laser->flag = LF_FIXED_ACTIVE;
				static_cast<uint8_t>(laser->flag)++;
			}
			break;

		case LF_FIXED_ACTIVE:
			laser_hittest(*laser);
			if(laser->shrink_at_age > 0) {
				if(laser->age >= laser->shrink_at_age) {
					// laser->flag = LF_FIXED_SHRINK;
					static_cast<uint8_t>(laser->flag)++;
				}
			}
			break;

		case LF_FIXED_SHRINK:
			if(laser->age & 1) {
				// MODDERS: The necessary clamp to 0 here is caught by the
				// signed comparison below.
				laser->coords.width.shrink -= 2;
			}
			if(laser->coords.width.shrink < laser_width_min()) {
				laser->flag = LF_FREE;
			}
			break;

		case LF_FIXED_SHRINK_AND_WAIT_TO_GROW:
			if(laser->age & 1) {
				// MODDERS: See above… except that the signed comparison
				// wouldn't even have been needed here, as the condition is
				// `true` for both 1 and 0.
				laser->coords.width.shrink -= 2;
			}
			if(laser->coords.width.shrink <= laser_width_min()) {
				laser->flag = LF_FIXED_WAIT_TO_GROW;
				laser->age = 0;
			}
			break;

		case LF_SHOOTOUT_DECAY:
			shootout_update(laser);
			laser->coords.width.nonshrink += 2;
			if(
				laser->coords.width.nonshrink >=
				LASER_SHOOTOUT_DECAY_WIDTH_MAX
			) {
				laser->flag = LF_FREE;
			}
			break;
		}
		laser->age++;
	}

	#undef shootout_update
}

