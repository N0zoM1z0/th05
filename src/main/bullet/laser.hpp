// Semantic reference: ReC98 b6ba5b0a th05/main/bullet/laser.hpp.
#ifndef TH05_MAIN_BULLET_LASER_HPP
#define TH05_MAIN_BULLET_LASER_HPP
#include "src/shared/geometry.hpp"
typedef unsigned char vc_t;
typedef signed char pixel_delta_8_t;
#define to_sp(value) static_cast<subpixel_t>((value) * 16)

#define LASER_DISTANCE_MIN to_sp(16.0f)
#define LASER_DISTANCE_MAX to_sp(550.0f) // Far away enough?

static const pixel_t LASER_SHOOTOUT_DECAY_WIDTH = 6;
static const pixel_t LASER_SHOOTOUT_DECAY_WIDTH_MAX = 28;

enum laser_flag_t {
	LF_FREE = 0,
	LF_SHOOTOUT = 1,
	LF_FIXED_WAIT_TO_GROW = 2,
	LF_FIXED_GROW = 3,

	// Fixed laser has reached its target width and will now actually kill the
	// player on contact.
	LF_FIXED_ACTIVE = 4,

	// Fixed laser will shrink to a width of 1 and then either be removed
	// (LF_FIXED_SHRINK) or go back to LF_FIXED_WAIT_TO_GROW with its [age]
	// reset to 0 (LF_FIXED_SHRINK_AND_WAIT_TO_GROW).
	LF_FIXED_SHRINK = 5,
	LF_FIXED_SHRINK_AND_WAIT_TO_GROW = 6,

	// Shootout laser is reduced to the two edges parallel to its moving
	// direction, which are drawn as 1-pixel lines. The laser "grows" until its
	// width reaches LASER_SHOOTOUT_DECAY_WIDTH_MAX, at which it's removed.
	LF_SHOOTOUT_DECAY = 7,

	_laser_flag_t_FORCE_UINT8 = 0xFF
};

struct laser_coords_t {
	PlayfieldPoint origin;

	// Start and end point on the infinite [angle]° line starting at [origin]
	// that make up the actually rendered (and damaging) laser.
	Subpixel starts_at_distance;
	Subpixel ends_at_distance;

	unsigned char angle;

	union {
		// ZUN landmine: LF_FIXED_SHRINK and LF_FIXED_SHRINK_AND_WAIT_TO_GROW
		// are effectively limited to a maximum width of 127 pixels due to an
		// implementation convenience in their update code. For larger values,
		// their shrink animation wouldn't play, and the laser will transition
		// to its next flag immediately.
		pixel_delta_8_t shrink;

		// Other types have no limit besides the 8-bit one inherent to the
		// type. Shootout lasers should probably still be kept below
		// LASER_SHOOTOUT_DECAY_WIDTH_MAX though, as any larger value would
		// skip the decay animation.
		pixel_length_8_t nonshrink;
	} width;
};

struct Laser {
	laser_flag_t flag;
	vc_t col;
	laser_coords_t coords;

	// Truncated to 8 bits by the spawn function! Should have therefore rather
	// been a SubpixelLength8.
	Subpixel shootout_speed;

	int age;
	union {
		// [age] at which a fixed laser should transition from
		// LF_FIXED_WAIT_TO_GROW to LF_FIXED_GROW.
		int grow;
		// [age] at which a shoot-out laser should stop growing and start
		// moving along the infinite [angle]° line.
		int moveout;
	} active_at_age;

	// [age] at which a fixed laser should transition from LF_FIXED_ACTIVE to
	// LF_FIXED_SHRINK.
	int shrink_at_age;

	// [width] (in pixels) at which a fixed laser should transition from
	// LF_FIXED_GROW to LF_FIXED_ACTIVE.
	pixel_length_8_t grow_to_width;

	uint8_t padding[3];

	void fixed_init(const PlayfieldPoint &origin) {
		flag = LF_FIXED_WAIT_TO_GROW;
		coords.origin = origin;
		coords.starts_at_distance.v = LASER_DISTANCE_MIN;
		coords.ends_at_distance.v = LASER_DISTANCE_MAX;
		age = 0;
	}
};

#define LASER_COUNT 32

extern Laser lasers[LASER_COUNT];
extern Laser laser_template;


#pragma codeseg LASER_SC_TEXT main_03
void near lasers_shootout_add(void);
void pascal near laser_fixed_spawn(int slot);
void pascal near laser_manual_fixed_spawn(int slot);
void pascal near laser_manual_grow(int slot);
void pascal near laser_stop(int slot);
#pragma codeseg
extern "C" unsigned char __fastcall near playperf_speedtune(unsigned char speed);
extern "C" void pascal far vector2_at(SPPoint near &ret, subpixel_t origin_x,
    subpixel_t origin_y, subpixel_t length, int angle);
extern "C" void pascal far snd_se_play(int sound);

typedef char laser_coords_is_10[(sizeof(laser_coords_t) == 10) ? 1 : -1];
typedef char laser_is_24[(sizeof(Laser) == 24) ? 1 : -1];
typedef char laser_coords_at_2[(offsetof(Laser, coords) == 2) ? 1 : -1];
typedef char laser_speed_at_12[(offsetof(Laser, shootout_speed) == 12) ? 1 : -1];
typedef char laser_age_at_14[(offsetof(Laser, age) == 14) ? 1 : -1];
typedef char laser_active_at_16[(offsetof(Laser, active_at_age) == 16) ? 1 : -1];
typedef char laser_shrink_at_18[(offsetof(Laser, shrink_at_age) == 18) ? 1 : -1];
typedef char laser_target_width_at_20[(offsetof(Laser, grow_to_width) == 20) ? 1 : -1];
#endif
