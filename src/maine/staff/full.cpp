// All17 real bodies in original order, including both unaccepted updater/render.
#pragma option -zCSTAFF_FULL_TEXT -zPgroup_01
#define TH05_STAFF_FULL_FAMILY
#include "src/maine/staff/full.hpp"
#pragma codeseg STAFF_FULL_TEXT group_01
#include "src/maine/staff/body/space_window_set.inl"
#include "src/maine/staff/body/staff_particles_init.inl"
#include "src/maine/staff/body/staff_particles_gather.inl"
#include "src/maine/staff/body/staff_particles_clear.inl"
#include "src/maine/staff/body/staff_particles_scatter.inl"
#include "src/maine/staff/body/staff_particles_update.inl"
#include "src/maine/staff/body/staff_orb_spark_add.inl"
#include "src/maine/staff/body/staff_orb_trail_update.inl"
#include "src/maine/staff/body/staff_orb_particles_age.inl"
#include "src/maine/staff/body/staff_orb_opening_update.inl"
#include "src/maine/staff/body/staff_rain_spawn.inl"
#include "src/maine/staff/body/staff_rain_update.inl"
#include "src/maine/staff/body/staff_text_wipe.inl"
#include "src/maine/staff/body/staff_image_update_a.inl"
#include "src/maine/staff/body/staff_image_update_b.inl"
#include "src/maine/staff/body/staff_scene_render.inl"
#include "src/maine/staff/body/staff_frame_advance.inl"
