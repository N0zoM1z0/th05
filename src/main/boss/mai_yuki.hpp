// Natural stage-four flight interfaces and actual sprite indices.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_HPP
#include "src/main/boss/movement.hpp"
extern boss_stuff_t boss2;
extern y_direction_t mai_flystep_random_next_y_direction;
extern y_direction_t yuki_flystep_random_next_y_direction;
#define BOSS_W 64
#define PLAYFIELD_W 384
// th05/sprites/main_pat.h: the stage sprite bank starts at 180.
static const int PAT_B4_STILL = 180;
static const int PAT_B4_RIGHT = 181;
static const int PAT_B4_LEFT = 182;
// Shared boss implementation macros.

#define flystep_random_for( \
	boss, \
	next_y_direction, \
	speed, \
	frames, \
	clamp_left, \
	clamp_right, \
	clamp_top, \
	clamp_bottom, \
	sprite_left, \
	sprite_right, \
	sprite_still, \
	frame \
) { \
	if(frame == 0) { \
		if(boss.pos.cur.x.v < BOSS_FLYSTEP_RANDOM_FIELD_LEFT) { \
			boss.angle = randring2_next8_ge_lt(-0x30, +0x30); \
		} else if(boss.pos.cur.x.v > BOSS_FLYSTEP_RANDOM_FIELD_RIGHT) { \
			boss.angle = randring2_next8_and_ge_lt(+0x30, +0x91); \
		} else { \
			boss.angle = randring2_next16(); \
		} \
		if( \
			(next_y_direction == Y_UP  ) && (boss.angle <  0x80) || \
			(next_y_direction == Y_DOWN) && (boss.angle >= 0x80) \
		) { \
			boss.angle = -boss.angle; \
		} \
		next_y_direction = Y_ANY; \
	} \
	if(frame >= 0) { \
		vector2_near( \
			boss.pos.velocity, boss.angle, (to_sp(speed) - (frame * 2)) \
		); \
		boss.pos.cur.x.v += boss.pos.velocity.x.v; \
		boss.pos.cur.y.v += boss.pos.velocity.y.v; \
		if(boss.pos.velocity.x.v < 0) { \
			boss.sprite = sprite_left; \
		} else { \
			boss.sprite = sprite_right; \
		} \
		if(boss.pos.cur.y.v < clamp_top) { \
			boss.pos.cur.y.v = clamp_top; \
			next_y_direction = Y_DOWN; \
		} else if(boss.pos.cur.y.v > clamp_bottom) { \
			boss.pos.cur.y.v = clamp_bottom; \
			next_y_direction = Y_UP; \
		} \
		if(boss.pos.cur.x.v < clamp_left) { \
			boss.pos.cur.x.v = clamp_left; \
		} else if(boss.pos.cur.x.v > clamp_right) { \
			boss.pos.cur.x.v = clamp_right; \
		} \
		if(frame >= frames) { \
			boss.sprite = sprite_still; \
			return true; \
		} \
	} \
	return false; \
}

#endif
