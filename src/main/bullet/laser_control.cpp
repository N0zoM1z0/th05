// Laser spawning and control: shoot-out lasers, fixed lasers with timed or
// script-controlled growth, and stopping. Same as the corresponding functions
// in ReC98's th05/main/bullet/laser.cpp.
#pragma option -zCLASER_SC_TEXT -zPmain_03 -G
#include "src/main/bullet/laser.hpp"

void near lasers_shootout_add(void)
{
	Laser near *laser;
	int i;
	subpixel_t speed = playperf_speedtune(laser_template.shootout_speed.v);

	for((laser = lasers, i = 0); i < LASER_COUNT; (i++, laser++)) {
		if(laser->flag != LF_FREE) {
			continue;
		}
		laser->flag = LF_SHOOTOUT;
		laser->coords.starts_at_distance.v = LASER_DISTANCE_MIN;
		laser->coords.ends_at_distance.v = LASER_DISTANCE_MIN;
		laser->age = 0;
		laser->active_at_age = laser_template.active_at_age;
		laser->col = laser_template.col;
		laser->shootout_speed.v = speed;
		laser->grow_to_width = 6;
		laser->coords.width.nonshrink = 6;
		laser->coords.angle = laser_template.coords.angle;
		vector2_at(
			laser->coords.origin,
			laser_template.coords.origin.x.v,
			laser_template.coords.origin.y.v,
			(LASER_DISTANCE_MIN / 2),
			laser_template.coords.angle
		);
		snd_se_play(5); // laser sound
		return;
	}
}

// Fixed lasers occupy the [slot] chosen by the script, and are not spawned if
// that slot is in use.
void pascal near laser_fixed_spawn(int slot)
{
	Laser near &laser = lasers[slot];
	if(laser.flag != LF_FREE) {
		return;
	}
	laser.fixed_init(laser_template.coords.origin);
	laser.active_at_age.grow = laser_template.active_at_age.grow;
	laser.shrink_at_age = laser_template.shrink_at_age;
	laser.col = laser_template.col;
	laser.grow_to_width = laser_template.coords.width.nonshrink;
	laser.coords.width.nonshrink = 1;
	laser.coords.angle = laser_template.coords.angle;
	snd_se_play(5);
}

// Like laser_fixed_spawn(), but the laser only grows and shrinks when told to
// by laser_manual_grow() and laser_stop().
void pascal near laser_manual_fixed_spawn(int slot)
{
	Laser near &laser = lasers[slot];
	if(laser.flag != LF_FREE) {
		return;
	}
	laser.fixed_init(laser_template.coords.origin);
	laser.active_at_age.grow = -1;
	laser.shrink_at_age = -1;
	laser.col = laser_template.col;
	laser.coords.width.nonshrink = 1;
	laser.grow_to_width = laser_template.coords.width.nonshrink;
	laser.coords.angle = laser_template.coords.angle;
	snd_se_play(5);
}

void pascal near laser_manual_grow(int slot)
{
	if(lasers[slot].flag != LF_FIXED_WAIT_TO_GROW) {
		return;
	}
	lasers[slot].flag = LF_FIXED_GROW;
	snd_se_play(6); // laser growth sound
}

// Active fixed lasers start shrinking and shoot-out lasers start decaying.
// Lasers already in LF_FIXED_SHRINK or LF_SHOOTOUT_DECAY are left alone; all
// others are removed immediately.
void pascal near laser_stop(int slot)
{
	if(lasers[slot].flag == LF_FIXED_ACTIVE) {
		lasers[slot].flag = LF_FIXED_SHRINK;
	} else if (lasers[slot].flag == LF_SHOOTOUT) {
		lasers[slot].flag = LF_SHOOTOUT_DECAY;
	} else if (
		(lasers[slot].flag != LF_FIXED_SHRINK) &&
		(lasers[slot].flag != LF_SHOOTOUT_DECAY)
	) {
		lasers[slot].flag = LF_FREE;
	}
}
