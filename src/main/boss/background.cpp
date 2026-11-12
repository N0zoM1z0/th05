// Boss background algorithms adapted from natural C++ in nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/main/boss/render.cpp.
// Exact original-order compiler context for all 19 Boss background functions.
// The signed-zero particle clip retains ReC98's original symbolic operand.
#pragma option -zCBOSS_BG_TEXT -zPmain_01
#include <dos.h>
#include "src/main/boss/background.hpp"
#include "src/main/boss/exalice/hexagram_rules.hpp"
#include "src/main/boss/shinki/background_rules.h"

void pascal near sara_bg_render(void)
{
	boss_bg_render_entrance_bb_transition_and_backdrop(
		tiles_render_after_custom(boss.phase_frame),
		SARA_BACKDROP_LEFT,
		SARA_BACKDROP_TOP,
		0
	);
}

void pascal near louise_bg_render(void)
{
	boss_bg_render_entrance_bb_opaque_and_backdrop(
		tiles_render_after_custom(boss.phase_frame),
		int,
		ENTRANCE_BB_FRAMES_PER_CEL,
		LOUISE_BACKDROP_LEFT,
		LOUISE_BACKDROP_TOP,
		1,
		louise_backdrop_colorfill,
		0
	);
}

void pascal near alice_bg_render(void)
{
	boss_bg_render_entrance_bb_opaque_and_backdrop(
		tiles_render_after_custom(boss.phase_frame),
		int,
		ENTRANCE_BB_FRAMES_PER_CEL,
		ALICE_BACKDROP_LEFT,
		ALICE_BACKDROP_TOP,
		1,
		alice_backdrop_colorfill,
		V_WHITE
	);
}

void pascal near mai_yuki_bg_render(void)
{
	boss_bg_render_entrance_bb_opaque_and_backdrop(
		tiles_render_after_custom(boss.phase_frame),
		unsigned char,
		ENTRANCE_BB_FRAMES_PER_CEL,
		MAI_YUKI_BACKDROP_LEFT,
		MAI_YUKI_BACKDROP_TOP,
		1,
		mai_yuki_backdrop_colorfill,
		9
	);
}

void pascal near yumeko_bg_render(void)
{
	boss_bg_render_entrance_bb_opaque_and_backdrop(
		tiles_render_all(),
		unsigned char,
		ENTRANCE_BB_FRAMES_PER_CEL,
		YUMEKO_BACKDROP_LEFT,
		YUMEKO_BACKDROP_TOP,
		1,
		yumeko_backdrop_colorfill,
		V_WHITE
	);
}

/// Stage 6 - Shinki
/// ----------------

static const pixel_t SHINKI_SPINLINE_MOVE_W = (PLAYFIELD_W / 6);
static const subpixel_t SHINKI_SPINLINE_MOVE_SPEED = (TO_SP(1) / 4);
#define SHINKI_SPINLINE_TOP to_sp(80.0f)
#define SHINKI_SPINLINE_BOTTOM to_sp(PLAYFIELD_H - 64)
static const unsigned int SHINKI_SPINLINE_MOVE_FRAMES = (
	SHINKI_SPINLINE_MOVE_W * SHINKI_SPINLINE_MOVE_SPEED
);

static const int SHINKI_LINESET_COUNT = 2;
static const int PARTICLES_UNINITIALIZED = SHB_PARTICLES_UNINITIALIZED;

// Maps one of Shinki's four visible lines to its index in a line set.
static const int SHINKI_LINE_MAIN = (0 * 6);
static const int SHINKI_LINE_2 = (1 * 6);
static const int SHINKI_LINE_3 = (2 * 6);
static const int SHINKI_LINE_4 = (3 * 6);

// All five physical Shinki background globals have C-linkage owners.

#define shinki_spinline_x_and_angle(set, delta) \
	if(set->radius[SHINKI_LINE_MAIN] > to_sp(96.0f)) { \
		set->radius[SHINKI_LINE_MAIN].v -= to_sp(0.125f); \
	} \
	if( \
		(shinki_bg_spinline_frame % (SHINKI_SPINLINE_MOVE_FRAMES * 2)) < \
		SHINKI_SPINLINE_MOVE_FRAMES \
	) { \
		set->center[SHINKI_LINE_MAIN].x.v += delta; \
	} else { \
		set->center[SHINKI_LINE_MAIN].x.v -= delta; \
	} \
	set->angle[SHINKI_LINE_MAIN] += (delta / 2);

#define shinki_spinline_y_formation_top(set, delta, set_i, line_i) \
	delta = (SHINKI_SPINLINE_TOP - set->center[SHINKI_LINE_MAIN].y); \
	set_i = 0; \
	while(set_i < SHINKI_LINESET_COUNT) { \
		for(line_i = SHINKI_LINE_4; line_i >= 0; line_i--) { \
			set->center[line_i].y.v += delta; \
		} \
		set_i++; \
		set++; \
	}

#define shinki_spinline_y_formation_bottom(set, delta, set_i, line_i) \
	delta = (set->center[SHINKI_LINE_MAIN].y - SHINKI_SPINLINE_BOTTOM); \
	set_i = 0; \
	while(set_i < SHINKI_LINESET_COUNT) { \
		for(line_i = SHINKI_LINE_4; line_i >= 0; line_i--) { \
			set->center[line_i].y.v -= delta; \
		} \
		set_i++; \
		set++; \
	}

// Original signed top clip uses the source-level symbolic zero preserved by
// ReC98: a near address at DGROUP:0000 forces the actual CMP AX,0000.
template <class T> inline T keep_0(T x) {
    if(x == 0) {
        extern void *near address_0;
        return reinterpret_cast<T>(&address_0);
    }
    return x;
}

void near shinki_bg_particles_render(void)
{
	_ES = SEG_PLANE_B;
	boss_particle_t near *particle = boss_particles;
	int patnum;
	screen_x_t left_;
	int i = 0;
	while(i < BOSS_PARTICLE_COUNT) {
		if(particle->pos.x.v != (static_cast<subpixel_t>(SHB_PARTICLE_INACTIVE_X_PX * 16))) {
			particle->pos.x.v += particle->velocity.x.v;
			particle->pos.y.v += particle->velocity.y.v;
			if(particle->patnum == 0) {
				patnum = (particle->age / 8);
				if(patnum >= PARTICLE_CELS) {
					patnum = (PARTICLE_CELS - 1);
				}
				patnum += PAT_PARTICLE;
			} else {
				patnum = particle->patnum;
			}

			#define left	static_cast<pixel_t>(_CX)
			#define top 	static_cast<pixel_t>(_AX)

			// Lol, is this only not directly assigned to _CX because ZUN was
			// scared that the _AX assignment might overwrite _CX?
			left_ = (PLAYFIELD_LEFT + (particle->pos.x.v >> 4) - (PARTICLE_W / 2));
			top = (PLAYFIELD_TOP + (particle->pos.y.v >> 4) - (PARTICLE_H / 2));
			left = left_;
			if(!(
				(left > (PLAYFIELD_LEFT - PARTICLE_W)) &&
				(left < PLAYFIELD_RIGHT) &&
				(top > keep_0(static_cast<int>(0))) &&
				(top < PLAYFIELD_BOTTOM)
			)) {
				particle->pos = particle->origin;
				particle->age = SHB_PARTICLE_INITIAL_AGE;
			} else {
				z_super_roll_put_16x16_mono(left, top, patnum);
				particle->age++;
			}

			#undef top
			#undef left
		}
		i++;
		particle++;
	}
}

// The complete Shinki particle renderer and following backgrounds stay in
// the same native CODE contribution. Nothing is reserved between functions.

void near shinki_bg_type_a_update_part1(void)
{
	boss_particle_t near *particle;
	int i;
	unsigned int angle;
	int line_i;
	lineset_t near *set;

	if(shinki_bg_type_a_particles_alive == PARTICLES_UNINITIALIZED) {
		set = linesets;
		i = 0;
		angle = SHB_LINESET_INITIAL_ANGLE;
		while(i < SHINKI_LINESET_COUNT) {
			for(line_i = 0; line_i < LINESET_LINE_COUNT; line_i++) {
				set->center[line_i].x.v = to_sp(PLAYFIELD_W / 2);
				set->center[line_i].y.v = to_sp(PLAYFIELD_H / 2);
				set->radius[line_i].v = to_sp(1.0f);
				set->angle[line_i] = angle;
			}
			i++;
			set++;
			angle -= SHB_LINESET_OPPOSITE_ANGLE;
		}

		particle = boss_particles;
		i = 0;
		while(i < BOSS_PARTICLE_COUNT) {
			particle->pos.x.v = (static_cast<subpixel_t>(SHB_PARTICLE_INACTIVE_X_PX * 16));
			particle->patnum = 0;
			i++;
			particle++;
		}
		shinki_bg_type_a_particles_alive = 0;
	}
	if(shinki_bg_type_a_particles_alive < BOSS_PARTICLE_COUNT) {
		if(((boss.phase_frame % SHB_PARTICLE_SPAWN_EVERY) == 0) == true) {
			particle = &boss_particles[shinki_bg_type_a_particles_alive];
			particle->pos.x.v = to_sp(PLAYFIELD_W / 2);
			particle->pos.y.v = to_sp(PLAYFIELD_H / 2);
			particle->origin.x.v = to_sp(PLAYFIELD_W / 2);
			particle->origin.y.v = to_sp(PLAYFIELD_H / 2);
			particle->angle = randring1_next16();
			particle->age = SHB_PARTICLE_INITIAL_AGE;
			vector2_at(
				particle->velocity,
				0.0f, 0.0f,
				background_random_sp(SHB_PARTICLE_MIN_SPEED_PX, SHB_PARTICLE_MAX_SPEED_PX),
				particle->angle
			);
			shinki_bg_type_a_particles_alive++;
		}
	}
	if(boss.phase == SHB_PHASE_A_SPIN) {
		if((shinki_bg_linesets_zoomed_out % (SHINKI_LINESET_COUNT * 2)) < 2) {
			linesets[0].angle[0] += SHB_LINES_SPIN_ANGLE;
			linesets[1].angle[0] += SHB_LINES_SPIN_ANGLE;
		} else {
			linesets[0].angle[0] -= SHB_LINES_SPIN_ANGLE;
			linesets[1].angle[0] -= SHB_LINES_SPIN_ANGLE;
		}
	}
}

// Draws the given line out of [set] with the current GRCG tile and color.
void pascal near grcg_lineset_line_put(lineset_t near &set, int i)
{
	vector2_at(drawpoint,
		set.center[i].x, set.center[i].y, set.radius[i], set.angle[i]
	);
	screen_x_t x1 = (PLAYFIELD_LEFT + (drawpoint.x.v >> 4));
	screen_y_t y1 = (PLAYFIELD_TOP + (drawpoint.y.v >> 4));

	vector2_at(drawpoint,
		set.center[i].x, set.center[i].y, set.radius[i], (set.angle[i] + 0x80)
	);
	screen_x_t x2 = (PLAYFIELD_LEFT + (drawpoint.x.v >> 4));
	screen_y_t y2 = (PLAYFIELD_TOP + (drawpoint.y.v >> 4));

	grcg_line(x1, y1, x2, y2);
}

// Copies lines [0..17] to lines [1..18].
void pascal near shinki_lineset_forward_copy(lineset_t near &set)
{
	for(int i = SHINKI_LINE_4; i > 0; i--) {
		set.center[i] = set.center[i - 1];
		set.angle[i] = set.angle[i - 1];
		set.radius[i].v = set.radius[i - 1].v;
	}
}

inline void shinki_bg_render_blue_particles_and_lines(void) {
	grcg_setmode_rmw();

	grcg_setcolor_direct(8);
	shinki_bg_particles_render();
	grcg_lineset_line_put(linesets[0], SHINKI_LINE_4);
	grcg_lineset_line_put(linesets[0], SHINKI_LINE_3);
	grcg_lineset_line_put(linesets[1], SHINKI_LINE_4);
	grcg_lineset_line_put(linesets[1], SHINKI_LINE_3);

	grcg_setcolor_direct(9);
	grcg_lineset_line_put(linesets[0], SHINKI_LINE_2);
	grcg_lineset_line_put(linesets[1], SHINKI_LINE_2);

	grcg_setcolor_direct(V_WHITE);
	grcg_lineset_line_put(linesets[0], SHINKI_LINE_MAIN);
	grcg_lineset_line_put(linesets[1], SHINKI_LINE_MAIN);

	grcg_off();
}

// Particles: Blue, shooting out from the center in random directions and at
//            random speeds
// Lines: Two parallel, repeatedly zooming lines that give the impression of
//        flying into a corridor, with random blue particles
void near shinki_bg_type_a_update_and_render(void)
{
	// MODDERS: Just fuse into this function.
	shinki_bg_type_a_update_part1();

	lineset_t near *set = linesets;
	int i = 0;
	while(i < SHINKI_LINESET_COUNT) {
		shinki_lineset_forward_copy(*set);
		set->radius[SHINKI_LINE_MAIN].v += to_sp(SHB_TYPE_A_LINE_GROWTH_PX);
		vector2_at(
			set->center[SHINKI_LINE_MAIN],
			to_sp(PLAYFIELD_W / 2),
			to_sp(PLAYFIELD_H / 2),
			((set->radius[SHINKI_LINE_MAIN].v * 3) / 4),
			(set->angle[SHINKI_LINE_MAIN] - 0x40)
		);
		if(set->radius[SHINKI_LINE_MAIN] >= to_sp(SHB_TYPE_A_RING_LIMIT_PX)) {
			shinki_bg_linesets_zoomed_out++;
			set->radius[SHINKI_LINE_MAIN].v = to_sp(0.0f);
		}
		i++;
		set++;
	}
	shinki_bg_render_blue_particles_and_lines();
}

void near shinki_bg_type_b_update_part1(void)
{
	boss_particle_t near *particle;
	int i;
	subpixel_t center_x;
	int line_i;
	lineset_t near *set;

	if(!shinki_bg_type_b_initialized) {
		center_x = to_sp(playfield_fraction_x(1 / 6.0f));
		set = linesets;
		i = 0;
		while(i < SHINKI_LINESET_COUNT) {
			for(line_i = SHINKI_LINE_4; line_i >= 0; line_i--) {
				set->center[line_i].x.v = center_x;
				set->center[line_i].y.v = to_sp((PLAYFIELD_H / 2) + SHB_TYPE_B_CENTRAL_Y_OFFSET_PX);
				set->radius[line_i].v = to_sp(SHB_TYPE_B_INITIAL_RADIUS_PX);
				set->angle[line_i] = SHB_TYPE_B_ANGLE;
			}
			set->velocity_y.v = to_sp(0.0f);
			i++;
			set++;
			center_x += to_sp(playfield_fraction_x(4 / 6.0f));
		}
		particle = boss_particles;
		i = 0;
		while(i < BOSS_PARTICLE_COUNT) {
			particle->pos.x.v = randring1_next16_mod(to_sp(PLAYFIELD_W));
			// Huh? Not PLAYFIELD_H?
			particle->pos.y.v = randring1_next16_mod(to_sp(PLAYFIELD_W));
			particle->origin.x = particle->pos.x;
			particle->origin.y.v = to_sp(SHB_TYPE_D_RISING_VELOCITY_PX);
			particle->velocity.x.v = to_sp(0.0f);
			particle->velocity.y.v = to_sp(0.0f);
			particle->patnum = background_random8(
				PAT_PARTICLE, (PAT_PARTICLE_last + 1)
			);
			i++;
			particle++;
		}
		shinki_bg_type_b_initialized++;
		return;
	}

	particle = boss_particles;
	i = 0;
	while(i < BOSS_PARTICLE_COUNT) {
		if(particle->velocity.y < to_sp(SHB_TYPE_B_FALLING_LIMIT_PX)) {
			particle->velocity.y.v += stage_frame_mod2;
		}
		i++;
		particle++;
	}
}

// Particles: Blue, at random X positions, falling down
// Lines: Spinning and horizontally shifting at both sides of Shinki's wings,
//        starting near the center of the playfield, moving up to
//        [SHINKI_SPINLINE_TOP], and then pushed *down* into a vertical
//        formation, until the set has reached its target velocity.
void near shinki_bg_type_b_update_and_render(void)
{
	// MODDERS: Just fuse into this function.
	shinki_bg_type_b_update_part1();

	lineset_t near *set;
	int set_i;
	subpixel_t delta;
	int line_i;

	delta = SHINKI_SPINLINE_MOVE_SPEED;
	set = linesets;
	set_i = 0;
	while(set_i < SHINKI_LINESET_COUNT) {
		shinki_lineset_forward_copy(*set);
		set->center[SHINKI_LINE_MAIN].y.v += set->velocity_y.v;
		if(set->velocity_y > to_sp(SHB_TYPE_B_VELOCITY_LIMIT_PX)) {
			set->velocity_y.v -= (
				(stage_frame_mod4 == 0) ? to_sp(0.0625f) : to_sp(0.0f)
			);
		}
		shinki_spinline_x_and_angle(set, delta);

		set_i++;
		set++;
		delta = -delta;
	}

	shinki_bg_spinline_frame++;

	set = linesets;
	if(set->center[SHINKI_LINE_MAIN].y < SHINKI_SPINLINE_TOP) {
		shinki_spinline_y_formation_top(set, delta, set_i, line_i);
	}

	shinki_bg_render_blue_particles_and_lines();
}

void near shinki_bg_type_c_update_part1(void)
{
	boss_particle_t near *particle;
	int i;

	if(!shinki_bg_type_c_initialized) {
		particle = boss_particles;
		if(particle->velocity.y < to_sp(0.0f)) {
			i = 0;
			while(i < BOSS_PARTICLE_COUNT) {
				particle->origin.y.v = to_sp(PLAYFIELD_H + 1.0f);
				i++;
				particle++;
			}
			shinki_bg_type_c_initialized++;
		}
	}

	particle = boss_particles;
	i = 0;
	while(i < BOSS_PARTICLE_COUNT) {
		if(particle->velocity.y.v > to_sp(SHB_TYPE_C_RISING_LIMIT_PX)) {
			particle->velocity.y.v -= stage_frame_mod2;
		}
		i++;
		particle++;
	}
}

// Particles: Blue, keeping their random X positions from type B, rising
// Lines: Moving back up to [SHINKI_SPINLINE_TOP], starting at the Y velocity
//        they had from the previous background type. Then, moving down to
//        [SHINKI_SPINLINE_BOTTOM], and then pushed *up* into a vertical
//        formation, until the set has reached its target velocity.
void near shinki_bg_type_c_update_and_render(void)
{
	// MODDERS: Just fuse into this function.
	shinki_bg_type_c_update_part1();

	lineset_t near *set;
	int set_i;
	subpixel_t delta;
	int line_i;

	delta = SHINKI_SPINLINE_MOVE_SPEED;
	set = linesets;
	set_i = 0;
	while(set_i < SHINKI_LINESET_COUNT) {
		shinki_lineset_forward_copy(*set);
		set->center[SHINKI_LINE_MAIN].y.v += set->velocity_y.v;
		if(set->velocity_y < to_sp(SHB_TYPE_C_VELOCITY_LIMIT_PX)) {
			set->velocity_y.v += stage_frame_mod2;
		}
		shinki_spinline_x_and_angle(set, delta);

		set_i++;
		set++;
		delta = -delta;
	}

	shinki_bg_spinline_frame++;

	set = linesets;
	// [velocity_y] is still negative from type B in the beginning. Continue
	// applying friction until [velocity_y] gets positive again
	if(set->center[SHINKI_LINE_MAIN].y < SHINKI_SPINLINE_TOP) {
		shinki_spinline_y_formation_top(set, delta, set_i, line_i);
	} else if(set->center[SHINKI_LINE_MAIN].y > SHINKI_SPINLINE_BOTTOM) {
		shinki_spinline_y_formation_bottom(set, delta, set_i, line_i);
	}

	shinki_bg_render_blue_particles_and_lines();
}

// Rising "smoke" particles.
void near shinki_bg_type_d_update(void)
{
	boss_particle_t near *particle;
	int i;

	if(!shinki_bg_type_d_initialized) {
		particle = boss_particles;
		i = 0;
		while(i < BOSS_PARTICLE_COUNT) {
			particle->origin.y.v = to_sp(
				SHINKI_TYPE_D_BACKDROP_TOP - PLAYFIELD_TOP
			);
			particle->velocity.y.v = to_sp(SHB_TYPE_D_RISING_VELOCITY_PX);
			i++;
			particle++;
		}
		shinki_bg_type_d_initialized++;
	}

	particle = boss_particles;
	i = 0;
	while(i < BOSS_PARTICLE_COUNT) {
		int cel = ((PARTICLE_CELS - 1) - (particle->pos.y.v / to_sp(SHB_TYPE_D_SMOKE_HEIGHT_PX)));
		if(cel < 0) {
			cel = 0;
		}
		particle->patnum = (PAT_PARTICLE + cel);
		i++;
		particle++;
	}
}

void pascal near shinki_bg_render(void)
{
	if(boss.phase == PHASE_HP_FILL) {
		boss_backdrop_render(
			SHINKI_BACKDROP_LEFT, SHINKI_STAGE_BACKDROP_TOP, 1
		);
	} else if(boss.phase == PHASE_BOSS_ENTRANCE_BB) {
		unsigned char entrance_cel = (
			boss.phase_frame / ENTRANCE_BB_FRAMES_PER_CEL
		);
		if(entrance_cel < (TILES_BB_CELS / 2)) {
			boss_backdrop_render(
				SHINKI_BACKDROP_LEFT, SHINKI_STAGE_BACKDROP_TOP, 1
			);
		} else {
			boss_bg_fill_col_0();
		}
		tiles_bb_col = V_WHITE;
		tiles_bb_put(bb_boss_seg, entrance_cel);
	} else if(boss.phase < SHB_BACKGROUND_A_END_PHASE) {
		boss_bg_fill_col_0();
		shinki_bg_type_a_update_and_render();
	} else if(boss.phase < SHB_BACKGROUND_B_END_PHASE) {
		boss_bg_fill_col_0();
		shinki_bg_type_b_update_and_render();
	} else if(boss.phase < SHB_BACKGROUND_C_END_PHASE) {
		boss_bg_fill_col_0();
		shinki_bg_type_c_update_and_render();
	} else /* if(boss.phase == PHASE_NONE) */ { \
		cdg_put_noalpha_8(
			SHINKI_BACKDROP_LEFT, SHINKI_TYPE_D_BACKDROP_TOP, CDG_BG_2
		);
		shinki_bg_type_d_colorfill();
		shinki_bg_type_d_update();

		grcg_setcolor(GC_RMW, 6);
		shinki_bg_particles_render();
		grcg_off();
	}
}
/// ----------------

/// Extra Stage - EX-Alice
/// ----------------------

static const screen_x_t HEXAGRAM_CENTER_X = (
	PLAYFIELD_LEFT + (PLAYFIELD_W / 2)
);
static const vram_y_t HEXAGRAM_CENTER_Y = (PLAYFIELD_TOP + (PLAYFIELD_H / 2));

#define exalice_hexagram_point_set(ret, radius, angle) \
	vector2_at( \
		ret, to_sp(HEXAGRAM_CENTER_X), to_sp(HEXAGRAM_CENTER_Y), radius, angle \
	)

void pascal near exalice_grcg_hexagram_put(subpixel_t radius, int angle)
{
	#define tri_point_0 drawpoint
	extern SPPoint tri_point_1;
	extern SPPoint tri_point_2;

	grcg_circle(HEXAGRAM_CENTER_X, HEXAGRAM_CENTER_Y, TO_PIXEL(radius));
	int i = 0;
	while(i < XHG_TRIANGLE_COUNT) {
		exalice_hexagram_point_set(tri_point_0, radius, angle);
		exalice_hexagram_point_set(tri_point_1, radius, (angle + XHG_VERTEX_ANGLE));
		exalice_hexagram_point_set(tri_point_2, radius, (angle - XHG_VERTEX_ANGLE));

		TO_PIXEL_INPLACE(tri_point_0.x.v);
		TO_PIXEL_INPLACE(tri_point_0.y.v);
		TO_PIXEL_INPLACE(tri_point_1.x.v);
		TO_PIXEL_INPLACE(tri_point_1.y.v);
		TO_PIXEL_INPLACE(tri_point_2.x.v);
		TO_PIXEL_INPLACE(tri_point_2.y.v);

		grcg_line(
			tri_point_0.x.v, tri_point_0.y.v, tri_point_1.x.v, tri_point_1.y.v
		);
		grcg_line(
			tri_point_1.x.v, tri_point_1.y.v, tri_point_2.x.v, tri_point_2.y.v
		);
		grcg_line(
			tri_point_0.x.v, tri_point_0.y.v, tri_point_2.x.v, tri_point_2.y.v
		);

		i++;
		angle += XHG_TRIANGLE_ROTATION;
	}

	#undef tri_point_0
}

// Finish with the two original EX-Alice background functions in a separate
// genuine compiler CODE contribution. This preserves the native FIXUPP record
// boundaries without adding a linker hole or changing the function bodies.
#pragma codeseg BOSS_BG_LATE_TEXT main_01

void near exalice_hexagrams_update_and_render(void)
{
	typedef char background_hexagrams_flag_is_1[(sizeof(hexagrams_flag_t) == 1) ? 1 : -1];
	int i;

	lineset_t near &set = linesets[0];
	if(hexagrams_flag == UNINITIALIZED) {
		for(i = 0; i < (LINESET_LINE_COUNT - XHG_LINE_EXCLUDE_LAST); i++) {
			set.radius[i].v = to_sp(XHG_INITIAL_RADIUS_PX);
			set.angle[i] = 0x00;
		}
		hexagrams_flag = TURN_RIGHT;
	}
	for(i = (LINESET_LINE_COUNT - XHG_LINE_SHIFT); i > 0; i--) {
		set.radius[i] = set.radius[i - 1];
		set.angle[i] = set.angle[i - 1];
	}
	set.radius[0].v += to_sp(XHG_RADIUS_STEP_PX);
	if(set.radius[0].v >= to_sp(XHG_RADIUS_LIMIT_PX)) {
		set.radius[0].v = to_sp(XHG_INITIAL_RADIUS_PX);
		hexagrams_flag = static_cast<hexagrams_flag_t>(
			FLAG_COUNT - hexagrams_flag
		);
	}
	if(hexagrams_flag == TURN_RIGHT) {
		set.angle[0] += XHG_ANGLE_STEP;
	} else {
		set.angle[0] -= XHG_ANGLE_STEP;
	}

	grcg_setcolor(GC_RMW, XHG_COLOR_OUTER);
	exalice_grcg_hexagram_put(set.radius[XHG_DIAMOND_LINE_OUTER].v, set.angle[XHG_DIAMOND_LINE_OUTER]);
	grcg_setcolor(GC_RMW, XHG_COLOR_INNER);
	exalice_grcg_hexagram_put(set.radius[XHG_DIAMOND_LINE_INNER].v, set.angle[XHG_DIAMOND_LINE_INNER]);
	if(boss.phase < XHG_PALETTE_VARIATION_FIRST_PHASE || boss.phase > XHG_PALETTE_VARIATION_LAST_PHASE) {
		grcg_setcolor(GC_RMW, V_WHITE);
	}
	exalice_grcg_hexagram_put(set.radius[0].v, set.angle[0]);
	grcg_off();
}

void pascal near exalice_bg_render(void)
{
	if(boss.phase == PHASE_HP_FILL) {
		tiles_render_after_custom(boss.phase_frame);
	} else if(boss.phase == PHASE_BOSS_ENTRANCE_BB) {
		unsigned char entrance_cel = (boss.phase_frame / 4);
		boss_bg_fill_col_0();
		tiles_bb_col = V_WHITE;
		tiles_bb_put(bb_boss_seg, entrance_cel);
	} else if(boss.phase < PHASE_BOSS_EXPLODE_BIG) {
		boss_bg_fill_col_0();
		exalice_hexagrams_update_and_render();
	} else if(boss.phase == PHASE_BOSS_EXPLODE_BIG) {
		tiles_render_all();
	} else /* if(boss.phase == PHASE_NONE) */ { \
		tiles_render_after_custom(boss.phase_frame);
	}
}
/// ----------------------
