// Complete TH05 staff particle state and actual MAINE helper interfaces.
#ifndef TH05_MAINE_STAFF_LIFECYCLE_HPP
#define TH05_MAINE_STAFF_LIFECYCLE_HPP

// Preserve the true first-declaration contexts of the accepted clip provider.
#pragma codeseg _TEXT
extern "C" void pascal far grc_setclip(int left, int top, int right, int bottom);
#pragma codeseg SCORE_TEXT group_01
void pascal near space_window_set(int center_x, int center_y, int w, int h);
#include "src/maine/staff/staff.hpp"

// This is the same complete class definition as the accepted staff state TU.
// That TU owns storage; this owner only references the real objects.
struct orb_particle_t {
    SPPointBase< SubpixelBase< long, pixel_t > > center;
    SPPoint velocity;
    int patnum_tiny;
    Subpixel speed;
    int gather_frame;
    unsigned char angle;
    union {
        unsigned char radius;
        x_direction_t rain_sway_x_direction;
    } al;
};

static const int ORB_PARTICLE_COUNT = 64;
static const int ORB_TRAIL_COUNT = 8;
static const int STAR_COUNT = 48;
static const int ORB_INDEX = ORB_PARTICLE_COUNT;
static const int PAT_ORB_PARTICLE = 0;
static const int ORB_RADIUS_FULL = 16;
static const subpixel_t STAFF_CENTER_NONE = -999 * 16;

extern orb_particle_t particles[ORB_PARTICLE_COUNT + 1];
extern SPPoint orb_trails_center[ORB_TRAIL_COUNT];
extern SPPoint stars_center[STAR_COUNT];
extern pixel_t space_window_w;
extern pixel_t space_window_h;
extern SPPoint space_camera_velocity;
extern SPPoint staff_spawn_point;
extern int staff_particle_decay;
extern int staff_frame;
extern unsigned char staff_back_page;

#pragma codeseg _TEXT
extern "C" {
    int pascal far irand(void);
    int pascal far iatan2(int y, int x);
    int pascal far ihypot(int x, int y);
}

// The five-word Pascal call writes a real near SPPoint output argument.
#pragma codeseg SHARED
#include "src/shared/math/vector.hpp"

// Both real foreign trail providers are no-argument near procedures.
#pragma codeseg STAFF_TRAIL_TEXT group_01
void near staff_orb_spark_add(void);
void near staff_orb_trail_update(void);

#pragma codeseg STAFF_LIFE_TEXT group_01
void near staff_particles_init(void);
void near staff_particles_gather(void);
void near staff_particles_clear(void);
void near staff_particles_scatter(void);
void near staff_particles_update(void);

typedef char staff_particle_size_is_20[(sizeof(orb_particle_t) == 20) ? 1 : -1];
typedef char staff_particle_center_at_0[(offsetof(orb_particle_t, center) == 0) ? 1 : -1];
typedef char staff_particle_velocity_at_8[(offsetof(orb_particle_t, velocity) == 8) ? 1 : -1];
typedef char staff_particle_pattern_at_12[(offsetof(orb_particle_t, patnum_tiny) == 12) ? 1 : -1];
typedef char staff_particle_speed_at_14[(offsetof(orb_particle_t, speed) == 14) ? 1 : -1];
typedef char staff_particle_gather_at_16[(offsetof(orb_particle_t, gather_frame) == 16) ? 1 : -1];
typedef char staff_particle_angle_at_18[(offsetof(orb_particle_t, angle) == 18) ? 1 : -1];
typedef char staff_particle_union_at_19[(offsetof(orb_particle_t, al) == 19) ? 1 : -1];
typedef char staff_particles_size_is_1300[(sizeof(particles) == 1300) ? 1 : -1];
typedef char staff_trails_size_is_32[(sizeof(orb_trails_center) == 32) ? 1 : -1];
typedef char staff_stars_size_is_192[(sizeof(stars_center) == 192) ? 1 : -1];

#endif
