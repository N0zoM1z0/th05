// Standalone build of the orb spark, trail, growth and opening functions.
#pragma option -zCSTAFF_TRAIL_TEXT -zPgroup_01
#include "src/maine/staff/state_publics.h"
#include "src/maine/staff/orb_opening.hpp"

#pragma codeseg STAFF_TRAIL_TEXT group_01
#include "src/maine/staff/body/staff_orb_spark_add.inl"

#include "src/maine/staff/body/staff_orb_trail_update.inl"

#include "src/maine/staff/body/staff_orb_particles_age.inl"

#include "src/maine/staff/body/staff_orb_opening_update.inl"
