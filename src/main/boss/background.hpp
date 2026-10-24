// Boss background ABI adapted from natural C++ in nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/main/boss/render.cpp,
// th05/main/boss/bosses.hpp, th04/main/boss/impl.hpp and their interface headers.
#ifndef TH05_MAIN_BOSS_BACKGROUND_HPP
#define TH05_MAIN_BOSS_BACKGROUND_HPP

#include "src/main/boss/movement.hpp"

typedef int screen_x_t;
typedef int screen_y_t;
typedef int vram_y_t;
typedef unsigned char vc_t;
typedef unsigned int vc2;
typedef unsigned char bb_tiles8_t;

#define PLAYFIELD_LEFT 32
#define PLAYFIELD_TOP 16
#define PLAYFIELD_W 384
#define PLAYFIELD_H 368
#define PLAYFIELD_RIGHT (PLAYFIELD_LEFT + PLAYFIELD_W)
#define PLAYFIELD_BOTTOM (PLAYFIELD_TOP + PLAYFIELD_H)
#define SEG_PLANE_B 0xA800
#define GC_RMW 0xC0
#define V_WHITE 15
#define TO_SP(value) ((value) << 4)
#define TO_PIXEL(value) ((value) >> 4)
#define TO_PIXEL_INPLACE(value) ((value) >>= 4)
#define PARTICLE_W 16
#define PARTICLE_H 16
#define PARTICLE_CELS 4
#define PAT_PARTICLE 172
#define PAT_PARTICLE_last (PAT_PARTICLE + PARTICLE_CELS - 1)
#define CDG_BG_BOSS 16
#define CDG_BG_2 17
#define TILES_BB_CELS (2048 / 128)

static const unsigned char PHASE_HP_FILL = 0;
static const unsigned char PHASE_BOSS_ENTRANCE_BB = 1;
static const unsigned char PHASE_BOSS_EXPLODE_BIG = 254;

#define BOSS_PARTICLE_COUNT 64
#define LINESET_LINE_COUNT 20
#define LINESET_COUNT 4

// All fields are represented; no layout-only padding arrays.
struct boss_particle_t {
    PlayfieldPoint pos;
    PlayfieldPoint origin;
    SPPoint velocity;
    int age;
    unsigned char angle;
    unsigned char patnum;
};

struct lineset_t {
    SPPoint center[LINESET_LINE_COUNT];
    Subpixel velocity_y;
    Subpixel radius[LINESET_LINE_COUNT];
    unsigned char angle[LINESET_LINE_COUNT];
};

extern boss_particle_t boss_particles[BOSS_PARTICLE_COUNT];
extern lineset_t linesets[LINESET_COUNT];
extern PlayfieldPoint drawpoint;
extern bb_tiles8_t __seg *bb_boss_seg;
extern bb_tiles8_t __seg *tiles_bb_seg;
extern unsigned char tiles_bb_col;
extern unsigned char stage_frame_mod2;
extern unsigned char stage_frame_mod4;

void near grcg_setmode_rmw(void);
void near grcg_setmode_tdw(void);
void near grcg_setcolor_direct_raw(void);
void pascal near boss_backdrop_render(screen_x_t left, vram_y_t top, vc_t col);
#define grcg_setcolor_direct(color_value) \
    _AH = color_value; grcg_setcolor_direct_raw()
#define grcg_off() outportb(0x7C, 0)

extern "C" {
    void pascal far cdg_put_noalpha_8(screen_x_t left, vram_y_t top, int slot);
    void pascal far vector2_at(SPPoint near &ret, subpixel_t origin_x,
        subpixel_t origin_y, subpixel_t length, int angle);
    void pascal far grcg_line(screen_x_t x1, vram_y_t y1,
        screen_x_t x2, vram_y_t y2);
    void pascal far grcg_setcolor(int mode, vc2 color);
    void pascal far grcg_circle(screen_x_t center_x, vram_y_t center_y,
        unsigned int radius);
    void pascal near z_super_roll_put_16x16_mono_raw(int patnum);
}
#define z_super_roll_put_16x16_mono(left_value, top_value, pattern_value) \
    _AX = top_value; _CX = left_value; \
    z_super_roll_put_16x16_mono_raw(pattern_value)

void pascal near tiles_render_all(void);
void pascal near tiles_render(void);
void pascal near tiles_redraw_invalidated(void);
void pascal near tiles_bb_put_raw(int cel);
void pascal near tiles_bb_invalidate_raw(int cel);
#define tiles_bb_put(segment_value, cel_value) { \
    tiles_bb_seg = segment_value; tiles_bb_put_raw(cel_value); \
}
#define tiles_bb_invalidate(segment_value, cel_value) { \
    tiles_bb_seg = segment_value; tiles_bb_invalidate_raw(cel_value); \
}
inline void tiles_render_after_custom(const int& frame) {
    if(frame <= 2) { tiles_render_all(); }
    else { tiles_render(); }
}

uint16_t near randring1_next16(void);
uint16_t pascal near randring1_next16_and(uint16_t mask);
uint16_t pascal near randring1_next16_mod(uint16_t divisor);
inline uint8_t background_random8(uint8_t min, uint8_t max) {
    return min + randring1_next16_and((max - min) - 1);
}
inline subpixel_t background_random_sp(float min_pixels, float max_pixels) {
    int min = to_sp(min_pixels);
    int max = to_sp(max_pixels);
    return (min >= 0)
        ? (min + randring1_next16_and((max - min) - 1))
        : (randring1_next16_and(max + -min - 1) - (-min));
}
static inline pixel_t playfield_fraction_x(float fraction = 1.0f) {
    return static_cast<pixel_t>(PLAYFIELD_W * fraction + 0.0001f);
}

static const pixel_t SARA_BACKDROP_W = 320;
static const screen_x_t SARA_BACKDROP_LEFT = (
	PLAYFIELD_LEFT + (PLAYFIELD_W / 2) - (SARA_BACKDROP_W / 2)
);
static const screen_y_t SARA_BACKDROP_TOP = PLAYFIELD_TOP;

static const screen_x_t LOUISE_BACKDROP_LEFT = PLAYFIELD_LEFT;
static const screen_y_t LOUISE_BACKDROP_TOP = PLAYFIELD_TOP;

static const pixel_t ALICE_BACKDROP_H = 163;
static const screen_x_t ALICE_BACKDROP_LEFT = PLAYFIELD_LEFT;
static const screen_y_t ALICE_BACKDROP_TOP = (
	PLAYFIELD_BOTTOM - ALICE_BACKDROP_H
);

static const pixel_t MAI_YUKI_BACKDROP_W = 256;
static const pixel_t MAI_YUKI_BACKDROP_H = 256;
static const screen_x_t MAI_YUKI_BACKDROP_LEFT = (
	PLAYFIELD_LEFT + (PLAYFIELD_W / 2) - (MAI_YUKI_BACKDROP_W / 2)
);
static const screen_y_t MAI_YUKI_BACKDROP_TOP = (
	PLAYFIELD_TOP + (PLAYFIELD_H / 2) - (MAI_YUKI_BACKDROP_H / 2)
);

static const screen_x_t YUMEKO_BACKDROP_LEFT = PLAYFIELD_LEFT;
static const screen_y_t YUMEKO_BACKDROP_TOP = PLAYFIELD_TOP;

static const screen_x_t SHINKI_BACKDROP_LEFT = PLAYFIELD_LEFT;
static const screen_y_t SHINKI_STAGE_BACKDROP_TOP = (
	PLAYFIELD_TOP + (PLAYFIELD_H / 2) - 80
);
static const pixel_t SHINKI_TYPE_D_BACKDROP_H = 128;
static const screen_y_t SHINKI_TYPE_D_BACKDROP_TOP = (
	PLAYFIELD_BOTTOM - SHINKI_TYPE_D_BACKDROP_H
);
// -----------------

// Boss-specific [boss_backdrop_colorfill] functions, called with the GRCG in
// TDW mode and the tile register set to the intended color.
void pascal near sara_backdrop_colorfill(void);
void pascal near louise_backdrop_colorfill(void);
void pascal near alice_backdrop_colorfill(void);
void pascal near mai_yuki_backdrop_colorfill(void);
void pascal near yumeko_backdrop_colorfill(void);
void pascal near shinki_stage_backdrop_colorfill(void);

// These enable and disable the GRCG themselves.
void near boss_bg_fill_col_0(void);
void near shinki_bg_type_d_colorfill(void);
/// ---------

// Same for all bosses in this game.
static const int ENTRANCE_BB_FRAMES_PER_CEL = 4;
static const int ENTRANCE_BB_TRANSITION_FRAMES_PER_CEL = 2;

// Common implementation of [boss_bg_render]:
// 1) Stage tiles before and after the fight
// 2) A static backdrop image during the fight
// 3) An opaque .BB tile animation as the transition between 1) and 2),
//    rendered on top of 1) during its first half, and on top of 2) during its
//    second half.
#define boss_bg_render_entrance_bb_opaque_and_backdrop( \
	on_hp_fill, \
	entrance_bb_cel_type, /* MODDERS: Pick one, and remove this parameter */ \
	entrance_bb_frames_per_cel, \
	backdrop_left, \
	backdrop_top, \
	backdrop_col, \
	backdrop_colorfill, /* MODDERS: Remove, and call boss_backdrop_render() */ \
	bb_col \
) { \
	if(boss.phase == PHASE_HP_FILL) { \
		on_hp_fill; \
	} else if(boss.phase == PHASE_BOSS_ENTRANCE_BB) { \
		entrance_bb_cel_type entrance_cel = ( \
			boss.phase_frame / entrance_bb_frames_per_cel \
		); \
		if(entrance_cel < (TILES_BB_CELS / 2)) { \
			tiles_render_all(); \
		} else { \
			/* A copy of boss_backdrop_render()… */ \
			grcg_setmode_tdw(); \
			grcg_setcolor_direct(backdrop_col); \
			/* … that probably predated [boss_backdrop_colorfill]? */ \
			backdrop_colorfill(); \
			grcg_off(); \
			\
			cdg_put_noalpha_8(backdrop_left, backdrop_top, CDG_BG_BOSS); \
		} \
		tiles_bb_col = bb_col; \
		tiles_bb_put(bb_boss_seg, entrance_cel); \
	} else if(boss.phase < PHASE_BOSS_EXPLODE_BIG) { \
		boss_backdrop_render(backdrop_left, backdrop_top, backdrop_col); \
	} else if(boss.phase == PHASE_BOSS_EXPLODE_BIG) { \
		tiles_render_all(); \
	} else /* if(boss.phase == PHASE_NONE) */ { \
		tiles_render_after_custom(boss.phase_frame); \
	}  \
}

// Like boss_bg_render_entrance_bb_opaque_and_backdrop(), but rendering 3) as
// a transition between stage tiles (where the entrance .BB bit is 0) and the
// backdrop image (where the entrance .BB bit is 1).
#define boss_bg_render_entrance_bb_transition_and_backdrop( \
	on_hp_fill, backdrop_left, backdrop_top, backdrop_col \
) { \
	if(boss.phase == PHASE_HP_FILL) { \
		on_hp_fill; \
	} else if(boss.phase == PHASE_BOSS_ENTRANCE_BB) { \
		boss_backdrop_render(backdrop_left, backdrop_top, backdrop_col); \
		tiles_bb_invalidate( \
			bb_boss_seg, \
			(boss.phase_frame / ENTRANCE_BB_TRANSITION_FRAMES_PER_CEL) \
		); \
		tiles_redraw_invalidated(); \
	} else if(boss.phase < PHASE_BOSS_EXPLODE_BIG) { \
		boss_backdrop_render(backdrop_left, backdrop_top, backdrop_col); \
	} else if(boss.phase == PHASE_BOSS_EXPLODE_BIG) { \
		tiles_render_all(); \
	} else /* if(boss.phase == PHASE_NONE) */ { \
		tiles_render_after_custom(boss.phase_frame); \
	} \
}

#pragma codeseg BOSS_BG_TEXT
void pascal near sara_bg_render(void);
void pascal near louise_bg_render(void);
void pascal near alice_bg_render(void);
void pascal near mai_yuki_bg_render(void);
void pascal near yumeko_bg_render(void);
void pascal near shinki_bg_render(void);
void pascal near exalice_bg_render(void);
#pragma codeseg

typedef char th05_background_particle_is_16[(sizeof(boss_particle_t) == 16) ? 1 : -1];
typedef char th05_background_particle_pos_at_0[(offsetof(boss_particle_t, pos) == 0) ? 1 : -1];
typedef char th05_background_particle_origin_at_4[(offsetof(boss_particle_t, origin) == 4) ? 1 : -1];
typedef char th05_background_particle_velocity_at_8[(offsetof(boss_particle_t, velocity) == 8) ? 1 : -1];
typedef char th05_background_particle_age_at_12[(offsetof(boss_particle_t, age) == 12) ? 1 : -1];
typedef char th05_background_particle_angle_at_14[(offsetof(boss_particle_t, angle) == 14) ? 1 : -1];
typedef char th05_background_particle_sprite_at_15[(offsetof(boss_particle_t, patnum) == 15) ? 1 : -1];
typedef char th05_background_lineset_is_142[(sizeof(lineset_t) == 142) ? 1 : -1];
typedef char th05_background_lineset_center_at_0[(offsetof(lineset_t, center) == 0) ? 1 : -1];
typedef char th05_background_lineset_velocity_at_80[(offsetof(lineset_t, velocity_y) == 80) ? 1 : -1];
typedef char th05_background_lineset_radius_at_82[(offsetof(lineset_t, radius) == 82) ? 1 : -1];
typedef char th05_background_lineset_angle_at_122[(offsetof(lineset_t, angle) == 122) ? 1 : -1];
typedef char th05_background_particle_near_pointer_is_2[(sizeof(boss_particle_t near *) == 2) ? 1 : -1];
typedef char th05_background_lineset_near_pointer_is_2[(sizeof(lineset_t near *) == 2) ? 1 : -1];
typedef char th05_background_bb_segment_is_2[(sizeof(bb_tiles8_t __seg *) == 2) ? 1 : -1];

#endif
