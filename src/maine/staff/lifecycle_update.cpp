// Unaccepted update body retained verbatim from failed whole candidate b.
#pragma option -zCSTAFF_LIFE_TEXT -zPgroup_01
#include "src/maine/staff/lifecycle.hpp"

void near staff_particles_update(void)
{
    orb_particle_t near *p = particles;
    SPPoint near *trail_center = orb_trails_center;
    SPPoint near *star_center = stars_center;
    int i;

    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        if(p->center.x.v != STAFF_CENTER_NONE) {
            p->center.x.v += p->velocity.x.v - space_camera_velocity.x.v;
            p->center.y.v += p->velocity.y.v - space_camera_velocity.y.v;
            if(staff_particle_decay == 0) {
                if(p->center.x.v <= ((-space_window_w * 8) - (4 * 16))) {
                    p->center.x.v += (space_window_w * 16) + (8 * 16);
                } else if(p->center.x.v >= ((space_window_w * 8) + (4 * 16))) {
                    p->center.x.v -= (space_window_w * 16) + (8 * 16);
                }
                if(p->center.y.v <= ((-space_window_h * 8) - (4 * 16))) {
                    p->center.y.v += (space_window_h * 16) + (8 * 16);
                } else if(p->center.y.v >= ((space_window_h * 8) + (4 * 16))) {
                    p->center.y.v -= (space_window_h * 16) + (8 * 16);
                }
            }
            if(staff_particle_decay != 0) {
                p->speed.v -= staff_particle_decay;
                if(p->speed.v == 0) {
                    p->center.x.v = STAFF_CENTER_NONE;
                } else {
                    if(p->speed.v > ((2 * 16) + 3)) {
                        p->patnum_tiny = PAT_ORB_PARTICLE;
                    } else if((p->speed.v % 7) == 0) {
                        p->patnum_tiny++;
                    }
                    vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
                }
            }
        }
    }
    for(i = 0; i < ORB_TRAIL_COUNT; i++, trail_center++) {
        if(trail_center->x != STAFF_CENTER_NONE) {
            trail_center->x.v -= space_camera_velocity.x.v;
            trail_center->y.v -= space_camera_velocity.y.v;
        }
    }
    for(i = 0; i < STAR_COUNT; i++, star_center++) {
        if((i % 2) == 0) {
            star_center->x.v -= space_camera_velocity.x.v;
            star_center->y.v -= space_camera_velocity.y.v;
        } else {
            star_center->x.v -= space_camera_velocity.x.v / 2;
            star_center->y.v -= space_camera_velocity.y.v / 2;
        }
        if(space_camera_velocity.x.v == 0) {
            if(star_center->x.v <= (-space_window_w * 8) ||
                    star_center->x.v >= (space_window_w * 8)) {
                star_center->x.v = ((irand() % space_window_w) * 16) - (space_window_w * 8);
                star_center->y.v = space_window_h * 8;
            }
        } else {
            if(star_center->x.v <= (-space_window_w * 8)) {
                star_center->x.v = space_window_w * 8;
            } else if(star_center->x.v >= (space_window_w * 8)) {
                star_center->x.v = -space_window_w * 8;
            }
        }
        if(star_center->y.v <= (-space_window_h * 8)) {
            star_center->y.v = space_window_h * 8;
        } else if(star_center->y.v >= (space_window_h * 8)) {
            star_center->y.v = -space_window_h * 8;
        }
    }
    p = &particles[ORB_INDEX];
    if(p->center.x.v != STAFF_CENTER_NONE) {
        p->center.x.v += p->velocity.x.v - space_camera_velocity.x.v;
        p->center.y.v += p->velocity.y.v - space_camera_velocity.y.v;
        if(p->al.radius >= ORB_RADIUS_FULL && staff_back_page != 0) {
            staff_orb_spark_add();
            if(p->velocity.y.v < ((11 * 16) + 4)) {
                p->velocity.y.v++;
            }
        }
    }
    if((staff_frame % 3) == 0) {
        staff_orb_trail_update();
    }
}
