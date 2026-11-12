#include "src/main/boss/shinki/devil_ballistics.hpp"
#include "src/main/boss/shinki/devil_float_state.h"
void near pattern_devil(void)
{
	enum {
		COLUMN_COUNT = 4,
		SHINKI_TO_LAST_COLUMN_DISTANCE = (
			(SHINKI_WING_W / 2) - (SHINKI_WING_W / 8)
		),
		COLUMN_W = (SHINKI_WING_W / 4),
		// Devil's staged startup is shared with the whole Shinki controller.
		DEVIL_PATTERN_START_FRAME = 192,
		DEVIL_FORCE_LASER_FRAME = 1800,
		DEVIL_SPREAD_INTERVAL_FRAMES = 4,
		DEVIL_LASER_GROW_FRAMES = 64,
		DEVIL_LASER_TURN_INTERVAL_FRAMES = 8,
		DEVIL_FIRST_LASER_SWEEP_FRAME = 65,
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

	// Careful, collides with [phase_relative] in shinki_update()! *Must* be
	// set to 1 before ending the pattern to ensure that the remaining phases
	// run in their expected order. Guaranteed in the original code by setting
	// HP_PHASE_10_DEVIL_LASER to a much higher value than HP_PHASE_10_END.
	#define lasers_active    	shinki_devil_scratch.lasers_active

	#define bullet_direction 	shinki_devil_scratch.bullet_direction
	#define bullet_intro_done	shinki_devil_scratch.bullet_intro_done
	#define b6ball_interval  	shinki_devil_scratch.b6ball_interval
	#define bullet_angle_inner	shinki_devil_scratch.bullet_angle_inner
	#define bullet_angle_outer	shinki_devil_scratch.bullet_angle_outer

	#define laser_grow_delay shinki_devil_laser_grow_delay

	// One fixed-speed shot per symmetric column; keep each column's real
	// origin shift at the call site and preserve the original firing order.
	#define DEVIL_FIRE_COL(direction) { \
		bullet_template.angle = (direction); \
		bullets_add_regular_fixedspeed(); \
	}

	// Starting with the second fixed laser, each real wing column shifts
	// its launch X before allocating the next slot; A remains the first.
	#define DEVIL_NEXT_FIXED_LASER(slot) { \
		laser_template.coords.origin.x.v -= to_sp(COLUMN_W); \
		laser_manual_fixed_spawn(slot); \
	}

	// Both red and decorative four-column spreads shift to the next column
	// before choosing its separate angle. The first decorative shot instead
	// chooses its angle before moving to its first source position.
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
			laser_template.coords.width.nonshrink = SHINKI_DEVIL_LASER_WIDTH_PX;
			laser_template.coords.angle = SHINKI_DEVIL_LASER_INITIAL_ANGLE;
			laser_template.col = SHINKI_DEVIL_LASER_COLOR;

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
			bullet_angle_inner = SHINKI_DEVIL_INITIAL_INNER_BULLET_ANGLE;
			bullet_angle_outer = SHINKI_DEVIL_INITIAL_OUTER_BULLET_ANGLE;
			b6ball_interval = select_for_rank(
                DEVIL_BALL_START_EASY, DEVIL_BALL_START_NORMAL,
                DEVIL_BALL_START_HARD, DEVIL_BALL_START_LUNATIC);
			bullet_intro_done = false;
			bullet_direction = CLOCKWISE;
			lasers_active = false;
			laser_angle_inner = SHINKI_DEVIL_LASER_INITIAL_ANGLE;
			laser_angle_outer = SHINKI_DEVIL_LASER_INITIAL_ANGLE;
			laser_direction = CLOCKWISE;
		}
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.patnum = PAT_BULLET16_V_RED;
		bullet_template.group = BG_SPREAD;
		if((bullet_angle_outer == DEVIL_SPREAD_OUTER_HIGH) && (bullet_intro_done == 0)) {
			bullet_intro_done++;
		}
		if(!bullet_intro_done) {
			bullet_template.spread = SHINKI_DEVIL_PRELUDE_BULLET_COUNT;
		} else {
			bullet_template.spread = SHINKI_DEVIL_FULL_BULLET_COUNT;
		}
		bullet_template.spread_angle_delta = SHINKI_DEVIL_SPREAD_ARC_ANGLE;
		bullet_template.speed.v = sara_to_sp8(SHINKI_DEVIL_BULLET_SPEED_PX);

		bullet_template.origin.x.v += to_sp(SHINKI_TO_LAST_COLUMN_DISTANCE);
		DEVIL_FIRE_COL(bullet_angle_outer);

		DEVIL_NEXT_FIRE_COL(bullet_angle_inner);

		DEVIL_NEXT_FIRE_COL(SHINKI_DEVIL_MIRROR_ANGLE - bullet_angle_inner);

		DEVIL_NEXT_FIRE_COL(SHINKI_DEVIL_MIRROR_ANGLE - bullet_angle_outer);

		if(!bullet_intro_done) {
			bullet_angle_outer += 0x04;
			bullet_angle_inner += 0x02;
		} else {
			// "Decorative" pellets aimed to the top of the playfield
			bullet_template.patnum = SHINKI_DEVIL_DECORATIVE_PELLET_PATNUM;
			bullet_template.spawn_type = BST_NO_DECELERATE;
			sara_set_spread(3, 0x30); // technically redundant

			// This first decorative shot sets its angle before moving the origin.
			// Later columns shift the origin before selecting their angle.
			bullet_template.angle = (SHINKI_DEVIL_MIRROR_ANGLE + bullet_angle_outer);
			bullet_template.origin.x.v += to_sp((COLUMN_W * (COLUMN_COUNT - 1)));
			bullets_add_regular_fixedspeed();

			DEVIL_NEXT_FIRE_COL(SHINKI_DEVIL_MIRROR_ANGLE + bullet_angle_inner);

			DEVIL_NEXT_FIRE_COL(0x00 - bullet_angle_inner);

			DEVIL_NEXT_FIRE_COL(0x00 - bullet_angle_outer);

			if(bullet_direction == CLOCKWISE) {
				bullet_angle_outer -= 0x02;
				bullet_angle_inner--;
				if(bullet_angle_outer == DEVIL_SPREAD_OUTER_LOW) {
					bullet_direction++; // = COUNTERCLOCKWISE;
				}
			} else /* if(bullet_direction == COUNTERCLOCKWISE) */ {
				bullet_angle_outer += 0x02;
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
			b6ball_template.speed.v = sara_to_sp8(SHINKI_DEVIL_AIMED_BALL_SPEED_PX);
			b6ball_template.patnum_tiny = PAT_B6BALL_PURPLE;
			b6balls_add();
		}

		snd_se_play(SHINKI_DEVIL_VOLLEY_SOUND);
	}

	// Lasers
	if(laser_grow_delay == 0) {
		return;
	} else if(laser_grow_delay < DEVIL_LASER_GROW_FRAMES) {
		laser_grow_delay++;
	} else if(laser_grow_delay == DEVIL_LASER_GROW_FRAMES) {
		// MODDERS: Turn into a loop
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
		if((boss.hp <= HP_PHASE_10_DEVIL_FAST) || (boss.phase_frame >= 2500)) {
			if((laser_grow_delay++) == DEVIL_FIRST_LASER_SWEEP_FRAME) {
				b6ball_interval = select_for_rank(
                    DEVIL_BALL_FAST_EASY, DEVIL_BALL_FAST_NORMAL,
                    DEVIL_BALL_FAST_HARD, DEVIL_BALL_FAST_LUNATIC);
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
