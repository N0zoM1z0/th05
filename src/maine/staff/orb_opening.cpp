// Four complete natural staff helpers; the preceding updater is not included.
#pragma option -zCSTAFF_TRAIL_TEXT -zPgroup_01
#include "src/maine/staff/orb_opening.hpp"

#pragma codeseg STAFF_TRAIL_TEXT group_01
void near staff_orb_spark_add(void)
{
    orb_particle_t near *p = &particles[staff_spark_cursor++];
    p->patnum_tiny = PAT_ORB_PARTICLE;
    p->angle = irand() & 0x7F;
    p->speed.v = 3 * 16;
    vector2_at(staff_spawn_point, particles[ORB_INDEX].center.x.v,
        particles[ORB_INDEX].center.y.v, 12 * 16, p->angle);
    p->center.x.v = staff_spawn_point.x.v;
    p->center.y.v = staff_spawn_point.y.v;
    if(staff_spark_cursor >= ORB_PARTICLE_COUNT) {
        staff_spark_cursor = 0;
    }
}

void near staff_orb_trail_update(void)
{
    int i;
    for(i = ORB_TRAIL_COUNT - 2; i >= 0; i--) {
        orb_trails_center[i + 1].x.v = orb_trails_center[i].x.v;
        orb_trails_center[i + 1].y.v = orb_trails_center[i].y.v;
    }
    orb_trails_center[0].x.v = particles[ORB_INDEX].center.x.v;
    orb_trails_center[0].y.v = particles[ORB_INDEX].center.y.v;
}

void near staff_orb_particles_age(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->gather_frame++;
        if(((p->gather_frame % 8) == 0) && (p->patnum_tiny < 5)) {
            p->patnum_tiny++;
        }
    }
    // The same pointer now addresses the array's real final, large-orb element.
    if(p->al.radius < ORB_RADIUS_FULL) {
        p->al.radius += staff_back_page;
    }
}

int near staff_orb_opening_update(void)
{
    int elapsed;
    int horizontal_offset;
    staff_orb_opening_frame++;
    if(staff_orb_opening_frame >= 80) {
        if(staff_orb_opening_frame < 176) {
            space_camera_velocity.y.v++;
        } else if(staff_orb_opening_frame < 344) {
            space_camera_velocity.y.v += staff_back_page;
        } else if(staff_camera_accel_phase == 0) {
            space_camera_velocity.y.v += ((staff_frame % 16) == 0);
            if(space_camera_velocity.y.v > ((11 * 16) + 6)) {
                staff_camera_accel_phase++;
            }
        } else {
            space_camera_velocity.y.v -= ((staff_frame % 16) == 0);
            if(space_camera_velocity.y.v < ((11 * 16) + 2)) {
                staff_camera_accel_phase--;
            }
        }

        if(staff_orb_opening_frame >= 234) {
            if(staff_orb_opening_frame < 512) {
                elapsed = staff_orb_opening_frame - 234;
                horizontal_offset = (elapsed > 88) ? (elapsed - 88) : 0;
                space_window_set(320 - horizontal_offset, 200,
                    384 - (elapsed / 2), 320 + (elapsed / 8));
            } else {
                if((staff_orb_opening_frame >= 992) &&
                    (staff_orb_opening_frame <= 1024)) {
                    particles[ORB_INDEX].velocity.x.v--;
                }
                if((staff_orb_opening_frame >= 1008) &&
                    (staff_orb_opening_frame <= 1040)) {
                    space_camera_velocity.x.v--;
                }
                return 1;
            }
        }
    }
    return 0;
}
