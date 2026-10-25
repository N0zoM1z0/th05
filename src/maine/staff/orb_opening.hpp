// Complete staff orb/trail helpers and opening-camera state.
#ifndef TH05_MAINE_STAFF_ORB_OPENING_HPP
#define TH05_MAINE_STAFF_ORB_OPENING_HPP

#include "src/maine/staff/lifecycle.hpp"

extern int staff_spark_cursor;
extern int staff_orb_opening_frame;
extern unsigned char staff_camera_accel_phase;

#pragma codeseg STAFF_TRAIL_TEXT group_01
void near staff_orb_particles_age(void);
int near staff_orb_opening_update(void);

#endif
