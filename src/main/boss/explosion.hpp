// Boss explosion state and the graphics functions that explosion.cpp uses.
// Adapted from ReC98's th04/main/boss/explode.cpp, th03/math/polar.hpp,
// th04/formats/super.h and th03/hardware/palette.hpp.
#ifndef TH05_MAIN_BOSS_EXPLOSION_HPP
#define TH05_MAIN_BOSS_EXPLOSION_HPP

#include "src/shared/geometry.hpp"

typedef unsigned char bool;
#define false 0
#define true 1

static const int EXPLOSION_SMALL_COUNT = 2;
static const unsigned SEG_PLANE_B = 0xa800;

struct Explosion {
    bool alive;
    unsigned char age;
    SPPoint center;
    SPPoint radius_cur;
    SPPoint radius_delta;
    signed char unused; // ZUN bloat

    // Added to the angle for the Y coordinate, which turns the circle into a
    // slanted ellipse.
    unsigned char angle_offset;

    // A method is the most idiomatic way for this to compile into ZUN's
    // original three instructions.
    unsigned char angle_y(const unsigned char &angle_base) {
        return (angle_offset + angle_base);
    }
};

extern Explosion explosions_small[EXPLOSION_SMALL_COUNT];
extern Explosion explosions_big;
extern int explosion_big_frame;
extern bool palette_changed;

extern "C" {
    extern const short __cdecl SinTable8[256];
    extern const short __cdecl CosTable8[256];
    extern unsigned int __cdecl PaletteTone;
    void far pascal super_put(int x, int y, int patnum);
    void pascal near z_super_roll_put_tiny_16x16_raw(int patnum);
}

int far pascal polar(int center, int radius, int ratio);
void near grcg_setmode_rmw(void);
void near explosions_small_update_and_render(void);
void near explosions_big_update_and_render(void);

#define polar_x(center, radius, angle) polar(center, radius, CosTable8[angle])
#define polar_y(center, radius, angle) polar(center, radius, SinTable8[angle])

#define z_super_roll_put_tiny_16x16(left, top, patnum) \
    _DX = top; \
    _AX = left; \
    z_super_roll_put_tiny_16x16_raw(patnum)

#define palette_settone_deferred(tone) { \
    PaletteTone = tone; \
    palette_changed = true; \
}

enum {
    PAT_EXPLOSION_BIG = 3,
    PAT_EXPLOSION_SMALL = 164
};

// Macros rather than functions: the small renderer passes the unsigned AX/DX
// registers, the big one signed locals, and the clipping comparisons must
// keep those types.
#define explosion_to_screen_left(center, width) (32 + ((center) >> 4) - ((width) / 2))
#define explosion_to_screen_top(center, height) (16 + ((center) >> 4) - ((height) / 2))
#define explosion_clip_small(left, top, width, height) ( \
    ((left) <= (32 - (width))) || ((left) >= 416) || \
    ((top) <= (16 - (height))) || ((top) >= 384) \
)
#define explosion_clip_large(left, top, width, height) ( \
    ((left) < 0) || ((left) > (448 - (width))) || \
    ((top) < 0) || ((top) > (400 - (height))) \
)

// Layout checks: the original code hardcodes these offsets.
typedef char th05_explosion_is_16[(sizeof(Explosion) == 16) ? 1 : -1];
typedef char th05_explosion_alive_at_0[(offsetof(Explosion, alive) == 0) ? 1 : -1];
typedef char th05_explosion_age_at_1[(offsetof(Explosion, age) == 1) ? 1 : -1];
typedef char th05_explosion_center_at_2[(offsetof(Explosion, center) == 2) ? 1 : -1];
typedef char th05_explosion_radius_at_6[(offsetof(Explosion, radius_cur) == 6) ? 1 : -1];
typedef char th05_explosion_delta_at_10[(offsetof(Explosion, radius_delta) == 10) ? 1 : -1];
typedef char th05_explosion_unused_at_14[(offsetof(Explosion, unused) == 14) ? 1 : -1];
typedef char th05_explosion_angle_at_15[(offsetof(Explosion, angle_offset) == 15) ? 1 : -1];

#endif
