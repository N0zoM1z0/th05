// Staff roll particle state and the particle lifecycle functions.
#ifndef TH05_MAINE_STAFF_LIFECYCLE_HPP
#define TH05_MAINE_STAFF_LIFECYCLE_HPP

// Every function is declared under the code segment of its definition
// (`#pragma codeseg`), since Borland binds a function to the segment of its
// first declaration. With TH05_STAFF_FULL_FAMILY, all staff functions go into
// the shared STAFF_FULL_TEXT segment; otherwise, each standalone wrapper gets
// its own segment.
#pragma codeseg _TEXT
extern "C" void pascal far grc_setclip(int left, int top, int right, int bottom);
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg SCORE_TEXT group_01
#endif
void pascal near space_window_set(int center_x, int center_y, int w, int h);
#include "src/maine/staff/staff.hpp"

// Same definition as in staff.cpp (after ReC98).
struct orb_particle_t {
    SPPointBase< SubpixelBase< long, pixel_t > > center;
    SPPoint velocity;
    int patnum_tiny;
    Subpixel speed;
    int gather_frame; // Only used during the orb gather phase.
    unsigned char angle;
    union {
        unsigned char radius; // In pixels. Only used with the orb instance.
        x_direction_t rain_sway_x_direction;
    } al;
};

static const int ORB_PARTICLE_COUNT = 64;
static const int ORB_TRAIL_COUNT = 8;
static const int STAR_COUNT = 48;
static const int ORB_INDEX = ORB_PARTICLE_COUNT;
static const int PAT_ORB_PARTICLE = 0; // First of 6 cels, ordered from big to small

// Below this [al.radius], the orb is rendered as a monochrome filled circle.
static const int ORB_RADIUS_FULL = 16;

// X coordinate of inactive particles, trails and the hidden orb.
static const subpixel_t STAFF_CENTER_NONE = -999 * 16;

// All coordinates are relative to the center of the space window. The last
// element is the big orb.
extern orb_particle_t particles[ORB_PARTICLE_COUNT + 1];
extern SPPoint orb_trails_center[ORB_TRAIL_COUNT];

// Even elements use the big star sprite, odd ones the small one.
extern SPPoint stars_center[STAR_COUNT];

extern pixel_t space_window_w;
extern pixel_t space_window_h;

// Effectively just moves all the entities into the opposite direction.
extern SPPoint space_camera_velocity;

extern SPPoint staff_spawn_point;   // Scratch output of vector2_at()
extern int staff_particle_decay;    // Subtracted from particle speeds if nonzero
extern int staff_frame;

// Alternates between 0 and 1 every frame, and is also used as a 0/1 term in
// the orb and camera motion.
extern unsigned char staff_back_page;

#pragma codeseg _TEXT
extern "C" {
    int pascal far irand(void);
    int pascal far iatan2(int y, int x);
    int pascal far ihypot(int x, int y);
}

#pragma codeseg SHARED
#include "src/shared/math/vector.hpp"

#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_TRAIL_TEXT group_01
#endif
void near staff_orb_spark_add(void);
void near staff_orb_trail_update(void);

#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_LIFE_TEXT group_01
#endif
void near staff_particles_init(void);
void near staff_particles_gather(void);
void near staff_particles_clear(void);
void near staff_particles_scatter(void);
void near staff_particles_update(void);

#endif
