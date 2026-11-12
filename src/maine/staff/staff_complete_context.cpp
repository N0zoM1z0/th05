// Original 17 exact Staff scene functions, two PC-98 bitmap device kernels and the 991-byte controller.
#pragma option -zCSTAFF_FULL_TEXT
#define TH05_STAFF_FULL_FAMILY
#include "src/maine/staff/state_publics.h"
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

// All source CODE contributions stay in the actual original 17-function
// source segment. The two real GRCG device loops are original-language
// inline-ASM context, not accepted CODE owners at this stage.
#pragma codeseg STAFF_FULL_TEXT group_01
void pascal near verdict_bitmap_snap(size_t bitmap_offset);
void pascal near verdict_bitmap_put(size_t bitmap_offset);
void near staffroll_animate(void);
extern unsigned char verdict_bitmap[2][352][40];
// Both independent canonical headers define this real 0xC0 constant.
// Rename the second declaration only within this combined translation unit.
#define STAFF_GRCG_RMW STAFF_CONTROLLER_GRCG_RMW
#include "src/maine/staff/controller.hpp"
#undef STAFF_GRCG_RMW
#pragma codeseg STAFF_FULL_TEXT group_01
#include "src/maine/staff/bitmap_hardware_context.inl"
#pragma codeseg STAFF_FULL_TEXT group_01

#include "src/maine/staff/controller_body.inl"
