// Shinki's Devil attack: four columns of red spreads and decorative pellets
// from her wings, aimed purple balls, and four lasers that start turning once
// her HP drops to 5600 or at frame 1800 at the latest.
#include "src/main/boss/shinki/wing_hitboxes.hpp"
#include "src/main/boss/shinki/devil_float_state.h"
void near pattern_devil(void)
{
	enum {
		COLUMN_COUNT = 4,
		SHINKI_TO_LAST_COLUMN_DISTANCE = (
			(SHINKI_WING_W / 2) - (SHINKI_WING_W / 8)
		),
		COLUMN_W = (SHINKI_WING_W / 4),
		DEVIL_PATTERN_START_FRAME = 192,
		DEVIL_FORCE_LASER_FRAME = 1800,
		DEVIL_SPREAD_INTERVAL_FRAMES = 4,
		DEVIL_LASER_GROW_FRAMES = 64,
		DEVIL_LASER_TURN_INTERVAL_FRAMES = 8,
		DEVIL_FAST_DELAY_SENTINEL = 65,
		DEVIL_FAST_STAGE_FRAME = 2500,
		DEVIL_DECORATIVE_SPREAD_COUNT = 3,
		DEVIL_ANGLE_ZERO = 0x00,
		DEVIL_PRELUDE_OUTER_STEP = 0x04,
		DEVIL_PRELUDE_INNER_STEP = 0x02,
		DEVIL_TURN_OUTER_STEP = 0x02,
		// These angles close the clockwise/anti-clockwise turn-arounds.
		DEVIL_SPREAD_OUTER_LOW = 0x30,
		DEVIL_SPREAD_OUTER_HIGH = 0x40,
		DEVIL_LASER_INNER_LOW = 0x38,
		DEVIL_LASER_INNER_HIGH = 0x41,
	};

	// Since the columns are symmetrical, it's only necessary to track the
	// inner and outer angles for spread bullets and lasers.
	#define laser_direction  	shinki_devil_scratch.laser_direction
	#define laser_angle_inner	shinki_devil_scratch.laser_angle_inner
	#define laser_angle_outer	shinki_devil_scratch.laser_angle_outer

	// Shares its byte with the shared-wave index of shinki_update(), which
	// only lets the phase end once this flag is set again. This happens after
	// the lasers have grown and the outer bullet angle has returned to 0x30,
	// at most 127 frames after the lasers were spawned. The 2800 HP between
	// the laser trigger and the end of the phase are more than the player can
	// deal in that time.
	#define lasers_active    	shinki_devil_scratch.wave_or_laser.devil_lasers_active

	#define bullet_direction 	shinki_devil_scratch.bullet_direction
	#define bullet_intro_done	shinki_devil_scratch.bullet_intro_done
	#define b6ball_interval  	shinki_devil_scratch.b6ball_interval
	#define bullet_angle_inner	shinki_devil_scratch.spiral_or_devil_inner_angle.devil_bullet_angle_inner
	#define bullet_angle_outer	shinki_devil_scratch.spiral_or_devil_outer_angle.devil_bullet_angle_outer

	#define laser_grow_delay shinki_devil_laser_grow_delay

	// Fires the current spread from the current column.
	#define DEVIL_FIRE_COL(direction) { \
		bullet_template.angle = (direction); \
		bullets_add_regular_fixedspeed(); \
	}

	// Moves one column to the left and spawns the next laser there.
	#define DEVIL_NEXT_FIXED_LASER(slot) { \
		laser_template.coords.origin.x.v -= to_sp(COLUMN_W); \
		laser_manual_fixed_spawn(slot); \
	}

	// Moves one column to the left and fires the current spread there.
	#define DEVIL_NEXT_FIRE_COL(direction) { \
		bullet_template.origin.x.v -= to_sp(COLUMN_W); \
		DEVIL_FIRE_COL(direction); \
	}

	if(boss.phase_frame < DEVIL_PATTERN_START_FRAME) {
		return;
	}

	int phase_frame_minus_startup_delay = (boss.phase_frame - DEVIL_PATTERN_START_FRAME);

	// Laser activation
	if((boss.hp <= HP_PHASE_10_DEVIL_LASER) || (boss.phase_frame >= DEVIL_FORCE_LASER_FRAME)) {
		if(laser_grow_delay == 0) {
			laser_template.coords.width.nonshrink = 6;
			laser_template.coords.angle = 0x40;
			laser_template.col = 0x0E;

			// Assign laser IDs from right to left
			laser_template.coords.origin.x.v += to_sp(SHINKI_TO_LAST_COLUMN_DISTANCE);
			laser_manual_fixed_spawn(SHINKI_DEVIL_LASER_SLOT_A);

			DEVIL_NEXT_FIXED_LASER(SHINKI_DEVIL_LASER_SLOT_B);

			DEVIL_NEXT_FIXED_LASER(SHINKI_DEVIL_LASER_SLOT_C);

			DEVIL_NEXT_FIXED_LASER(SHINKI_DEVIL_LASER_SLOT_D);
			laser_grow_delay++;
			boss_explode_small(ET_CIRCLE);
		}
	}

	// Spread bullets
	if((boss.phase_frame % DEVIL_SPREAD_INTERVAL_FRAMES) == 0) {
		if(phase_frame_minus_startup_delay == 0) {
			bullet_angle_inner = 0x20;
			bullet_angle_outer = 0x00;
			b6ball_interval = select_for_rank(64, 40, 32, 28);
			bullet_intro_done = false;
			bullet_direction = CLOCKWISE;
			lasers_active = false;
			laser_angle_inner = 0x40;
			laser_angle_outer = 0x40;
			laser_direction = CLOCKWISE;
		}
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_V_RED;
		bullet_template.group = BG_SPREAD;
		if((bullet_angle_outer == DEVIL_SPREAD_OUTER_HIGH) && (bullet_intro_done == 0)) {
			bullet_intro_done++;
		}
		if(!bullet_intro_done) {
			bullet_template.spread = 1;
		} else {
			bullet_template.spread = 3;
		}
		bullet_template.spread_angle_delta = 0x30;
		bullet_template.speed.v = sara_to_sp8(7.0f);

		bullet_template.origin.x.v += to_sp(SHINKI_TO_LAST_COLUMN_DISTANCE);
		DEVIL_FIRE_COL(bullet_angle_outer);

		DEVIL_NEXT_FIRE_COL(bullet_angle_inner);

		DEVIL_NEXT_FIRE_COL(0x80 - bullet_angle_inner);

		DEVIL_NEXT_FIRE_COL(0x80 - bullet_angle_outer);

		if(!bullet_intro_done) {
			bullet_angle_outer += DEVIL_PRELUDE_OUTER_STEP;
			bullet_angle_inner += DEVIL_PRELUDE_INNER_STEP;
		} else {
			// "Decorative" pellets aimed to the top of the playfield
			bullet_template.patnum = 0;
			bullet_template.spawn_type = BST_NO_DECELERATE;
			sara_set_spread(DEVIL_DECORATIVE_SPREAD_COUNT, 0x30); // technically redundant

			bullet_template.angle = (0x80 + bullet_angle_outer);
			bullet_template.origin.x.v += to_sp((COLUMN_W * (COLUMN_COUNT - 1)));
			bullets_add_regular_fixedspeed();

			DEVIL_NEXT_FIRE_COL(0x80 + bullet_angle_inner);

			DEVIL_NEXT_FIRE_COL(DEVIL_ANGLE_ZERO - bullet_angle_inner);

			DEVIL_NEXT_FIRE_COL(DEVIL_ANGLE_ZERO - bullet_angle_outer);

			if(bullet_direction == CLOCKWISE) {
				bullet_angle_outer -= DEVIL_TURN_OUTER_STEP;
				bullet_angle_inner--;
				if(bullet_angle_outer == DEVIL_SPREAD_OUTER_LOW) {
					bullet_direction++; // = COUNTERCLOCKWISE;
				}
			} else /* if(bullet_direction == COUNTERCLOCKWISE) */ {
				bullet_angle_outer += DEVIL_TURN_OUTER_STEP;
				bullet_angle_inner++;
				if(bullet_angle_outer == DEVIL_SPREAD_OUTER_HIGH) {
					bullet_direction--; // = CLOCKWISE;
				}
			}
		}

		// Aimed 32x32 balls
		if(bullet_intro_done && ((boss.phase_frame % b6ball_interval) == 0)) {
			b6ball_template.origin.x.v = shinki_wing_random_x();
			b6ball_template.origin.y.v = shinki_wing_random_y();
			b6ball_template.angle = player_angle_from(b6ball_template.origin.x, b6ball_template.origin.y);
			b6ball_template.speed.v = sara_to_sp8(3.75f);
			b6ball_template.patnum_tiny = PAT_B6BALL_PURPLE;
			b6balls_add();
		}

		snd_se_play(3);
	}

	// Lasers
	if(laser_grow_delay == 0) {
		return;
	} else if(laser_grow_delay < DEVIL_LASER_GROW_FRAMES) {
		laser_grow_delay++;
	} else if(laser_grow_delay == DEVIL_LASER_GROW_FRAMES) {
		// Four separate calls rather than a loop, as in ZUN's code.
		laser_manual_grow(SHINKI_DEVIL_LASER_SLOT_A);
		laser_manual_grow(SHINKI_DEVIL_LASER_SLOT_B);
		laser_manual_grow(SHINKI_DEVIL_LASER_SLOT_C);
		laser_manual_grow(SHINKI_DEVIL_LASER_SLOT_D);
		laser_grow_delay++;
	} else if(!lasers_active) {
		if(bullet_angle_outer == DEVIL_SPREAD_OUTER_LOW) {
			// Pattern can now be safely ended
			lasers_active++;
		}
	} else if((boss.phase_frame % DEVIL_LASER_TURN_INTERVAL_FRAMES) == 0) {
		lasers[0].coords.angle = laser_angle_outer;
		lasers[1].coords.angle = laser_angle_inner;
		lasers[2].coords.angle = (0x80 - lasers[1].coords.angle);
		lasers[3].coords.angle = (0x80 - lasers[0].coords.angle);
		if(laser_direction == CLOCKWISE) {
			laser_angle_outer++;
			laser_angle_inner--;
			if(laser_angle_inner == DEVIL_LASER_INNER_LOW) {
				laser_direction++; // = COUNTERCLOCKWISE;
			}
		} else /* if(laser_direction == COUNTERCLOCKWISE) */ {
			laser_angle_outer--;
			laser_angle_inner++;
			if(laser_angle_inner == DEVIL_LASER_INNER_HIGH) {
				laser_direction--; // = CLOCKWISE;
			}
		}
		if((boss.hp <= HP_PHASE_10_DEVIL_FAST) || (boss.phase_frame >= DEVIL_FAST_STAGE_FRAME)) {
			// [laser_grow_delay] is 65 after the lasers have grown, so this
			// only speeds up the balls once.
			if((laser_grow_delay++) == DEVIL_FAST_DELAY_SENTINEL) {
				b6ball_interval = select_for_rank(52, 20, 16, 12);
				boss_explode_small(ET_CIRCLE);
			}
		}
	}

	#undef DEVIL_NEXT_FIRE_COL
	#undef DEVIL_NEXT_FIXED_LASER
	#undef DEVIL_FIRE_COL
	#undef laser_grow_delay
	#undef bullet_angle_outer
	#undef bullet_angle_inner
	#undef b6ball_interval
	#undef bullet_intro_done
	#undef bullet_direction
	#undef lasers_active
	#undef laser_angle_outer
	#undef laser_angle_inner
	#undef laser_direction
}
