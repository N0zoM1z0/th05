// Four complete staff state functions, D387..D5E1; updater is retained separately.
#pragma option -zCSTAFF_LIFE_TEXT -zPgroup_01
#include "src/maine/staff/lifecycle.hpp"

void near staff_particles_init(void)
{
    orb_particle_t near *p = particles;
    SPPoint near *trail_center = orb_trails_center;
    SPPoint near *star_center = stars_center;
    int i;

    space_window_set(320, 200, 384, 320);
    staff_particle_decay = 0;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->center.x.v = ((irand() % space_window_w) * 16) - (space_window_w * 8);
        p->center.y.v = ((irand() % space_window_h) * 16) - (space_window_h * 8);
        p->angle = irand();
        p->speed.v = 10; // 0.625 pixels/frame, in sixteenths.
        p->patnum_tiny = PAT_ORB_PARTICLE;
        p->al.rain_sway_x_direction = X_RIGHT;
        vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
    }
    // The array's final element is the large orb, following the 64 particles.
    p->center.x.v = STAFF_CENTER_NONE;
    p->al.radius = 0;
    p->velocity.x.v = 0;
    p->velocity.y.v = 0;
    space_camera_velocity.x.v = 0;
    space_camera_velocity.y.v = 0;

    for(i = 0; i < ORB_TRAIL_COUNT; i++, trail_center++) {
        trail_center->x.v = STAFF_CENTER_NONE;
    }
    for(i = 0; i < STAR_COUNT; i++, star_center++) {
        star_center->x.v = ((irand() % space_window_w) * 16) - (space_window_w * 8);
        star_center->y.v = ((irand() % space_window_h) * 16) - (space_window_h * 8);
    }
}

void near staff_particles_gather(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->angle = iatan2(-p->center.y.v, -p->center.x.v);
        p->speed.v = ihypot(p->center.x.v, p->center.y.v) / 32;
        p->gather_frame = 0;
        vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
    }
    p->center.x.v = 0;
    p->center.y.v = 0;
    p->al.radius = 1;
}

void near staff_particles_clear(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->center.x.v = STAFF_CENTER_NONE;
    }
    p->al.radius = ORB_RADIUS_FULL;
    staff_particle_decay = 1;
}

void near staff_particles_scatter(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        // These initial polar values really precede the random replacement.
        p->angle = iatan2(-p->center.y.v, -p->center.x.v);
        p->speed.v = ihypot(p->center.x.v, p->center.y.v) / 32;
        p->patnum_tiny = PAT_ORB_PARTICLE;
        p->angle = irand() & 0x7F;
        p->speed.v = (irand() % (4 * 16)) + ((5 * 16) + 12);
        vector2_at(staff_spawn_point, particles[ORB_INDEX].center.x.v,
            particles[ORB_INDEX].center.y.v, 12 * 16, p->angle);
        vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
        p->center.x.v = staff_spawn_point.x.v;
        p->center.y.v = staff_spawn_point.y.v;
    }
    p->center.x.v = STAFF_CENTER_NONE;
    staff_particle_decay = 1;
}
