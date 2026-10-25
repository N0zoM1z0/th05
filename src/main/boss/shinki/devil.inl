void near pattern_devil(void)
{
	enum {
		COLUMN_COUNT = 4,
		SHINKI_TO_LAST_COLUMN_DISTANCE = (
			(SHINKI_WING_W / 2) - (SHINKI_WING_W / 8)
		),
		COLUMN_W = (SHINKI_WING_W / 4),
	};

	// Since the columns are symmetrical, it's only necessary to track the
	// inner and outer angles for spread bullets and lasers.
	#define laser_direction  	boss_statebyte[7]
	#define laser_angle_inner	boss_statebyte[8]
	#define laser_angle_outer	boss_statebyte[9]

	// Careful, collides with [phase_relative] in shinki_update()! *Must* be
	// set to 1 before ending the pattern to ensure that the remaining phases
	// run in their expected order. Guaranteed in the original code by setting
	// HP_PHASE_10_DEVIL_LASER to a much higher value than HP_PHASE_10_END.
	#define lasers_active    	boss_statebyte[10]

	#define bullet_direction 	boss_statebyte[11]
	#define bullet_intro_done	boss_statebyte[12]
	#define b6ball_interval  	boss_statebyte[13]
	#define bullet_angle_inner	boss_statebyte[14]
	#define bullet_angle_outer	boss_statebyte[15]

	#define laser_grow_delay shinki_devil_laser_grow_delay
	extern int laser_grow_delay;

	if(boss.phase_frame < 192) {
		return;
	}

	int phase_frame_minus_startup_delay = (boss.phase_frame - 192);

	// Laser activation
	if((boss.hp <= HP_PHASE_10_DEVIL_LASER) || (boss.phase_frame >= 1800)) {
		if(laser_grow_delay == 0) {
			laser_template.coords.width.nonshrink = 6;
			laser_template.coords.angle = 0x40;
			laser_template.col = 0xE;

			// Assign laser IDs from right to left
			laser_template.coords.origin.x.v += to_sp(SHINKI_TO_LAST_COLUMN_DISTANCE);
			laser_manual_fixed_spawn(0);

			laser_template.coords.origin.x.v -= to_sp(COLUMN_W);
			laser_manual_fixed_spawn(1);

			laser_template.coords.origin.x.v -= to_sp(COLUMN_W);
			laser_manual_fixed_spawn(2);

			laser_template.coords.origin.x.v -= to_sp(COLUMN_W);
			laser_manual_fixed_spawn(3);
			laser_grow_delay++;
			boss_explode_small(ET_CIRCLE);
		}
	}

	// Spread bullets
	if((boss.phase_frame % 4) == 0) {
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
		if((bullet_angle_outer == 0x40) && (bullet_intro_done == 0)) {
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
		bullet_template.angle = bullet_angle_outer;
		bullets_add_regular_fixedspeed();

		bullet_template.origin.x.v -= to_sp(COLUMN_W);
		bullet_template.angle = bullet_angle_inner;
		bullets_add_regular_fixedspeed();

		bullet_template.origin.x.v -= to_sp(COLUMN_W);
		bullet_template.angle = (0x80 - bullet_angle_inner);
		bullets_add_regular_fixedspeed();

		bullet_template.origin.x.v -= to_sp(COLUMN_W);
		bullet_template.angle = (0x80 - bullet_angle_outer);
		bullets_add_regular_fixedspeed();

		if(!bullet_intro_done) {
			bullet_angle_outer += 0x04;
			bullet_angle_inner += 0x02;
		} else {
			// "Decorative" pellets aimed to the top of the playfield
			bullet_template.patnum = 0;
			bullet_template.spawn_type = BST_NO_DECELERATE;
			sara_set_spread(3, 0x30); // technically redundant

			bullet_template.angle = (0x80 + bullet_angle_outer);
			bullet_template.origin.x.v += to_sp((COLUMN_W * (COLUMN_COUNT - 1))),
			bullets_add_regular_fixedspeed();

			bullet_template.origin.x.v -= to_sp(COLUMN_W),
			bullet_template.angle = (0x80 + bullet_angle_inner);
			bullets_add_regular_fixedspeed();

			bullet_template.origin.x.v -= to_sp(COLUMN_W),
			bullet_template.angle = (0x00 - bullet_angle_inner);
			bullets_add_regular_fixedspeed();

			bullet_template.origin.x.v -= to_sp(COLUMN_W),
			bullet_template.angle = (0x00 - bullet_angle_outer);
			bullets_add_regular_fixedspeed();

			if(bullet_direction == CLOCKWISE) {
				bullet_angle_outer -= 0x02;
				bullet_angle_inner--;
				if(bullet_angle_outer == 0x30) {
					bullet_direction++; // = COUNTERCLOCKWISE;
				}
			} else /* if(bullet_direction == COUNTERCLOCKWISE) */ {
				bullet_angle_outer += 0x02;
				bullet_angle_inner++;
				if(bullet_angle_outer == 0x40) {
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
	} else if(laser_grow_delay < 64) {
		laser_grow_delay++;
	} else if(laser_grow_delay == 64) {
		// MODDERS: Turn into a loop
		laser_manual_grow(0);
		laser_manual_grow(1);
		laser_manual_grow(2);
		laser_manual_grow(3);
		laser_grow_delay++;
	} else if(!lasers_active) {
		if(bullet_angle_outer == 0x30) {
			// Pattern can now be safely ended
			lasers_active++;
		}
	} else if((boss.phase_frame % 8) == 0) {
		lasers[0].coords.angle = laser_angle_outer;
		lasers[1].coords.angle = laser_angle_inner;
		lasers[2].coords.angle = (0x80 - lasers[1].coords.angle);
		lasers[3].coords.angle = (0x80 - lasers[0].coords.angle);
		if(laser_direction == CLOCKWISE) {
			laser_angle_outer++;
			laser_angle_inner--;
			if(laser_angle_inner == 0x38) {
				laser_direction++; // = COUNTERCLOCKWISE;
			}
		} else /* if(laser_direction == COUNTERCLOCKWISE) */ {
			laser_angle_outer--;
			laser_angle_inner++;
			if(laser_angle_inner == 0x41) {
				laser_direction--; // = CLOCKWISE;
			}
		}
		if((boss.hp <= HP_PHASE_10_DEVIL_FAST) || (boss.phase_frame >= 2500)) {
			if((laser_grow_delay++) == 65) {
				b6ball_interval = select_for_rank(52, 20, 16, 12);
				boss_explode_small(ET_CIRCLE);
			}
		}
	}

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
