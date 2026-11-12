/* Shinki stage-six background lifecycle shared with the true C seed owner.
 * Values are compile-time protocol, not another mutable Boss structure. */
#ifndef TH05_SHINKI_BACKGROUND_RULES_H
#define TH05_SHINKI_BACKGROUND_RULES_H

#define SHB_PARTICLES_UNINITIALIZED (-1 & 0xff)
#define SHB_LINESET_INITIAL_ANGLE 0x40
#define SHB_LINESET_OPPOSITE_ANGLE 0x80
#define SHB_PARTICLE_INACTIVE_X_PX (-999)
#define SHB_PARTICLE_SPAWN_EVERY 4
#define SHB_PARTICLE_MIN_SPEED_PX 2.0f
#define SHB_PARTICLE_MAX_SPEED_PX 6.0f
#define SHB_PARTICLE_INITIAL_AGE 0
#define SHB_PHASE_A_SPIN 3
#define SHB_LINES_SPIN_ANGLE 0x02
#define SHB_TYPE_A_LINE_GROWTH_PX 4.0f
#define SHB_TYPE_A_RING_LIMIT_PX 224.0f
#define SHB_TYPE_B_VELOCITY_LIMIT_PX (-14.0f)
#define SHB_TYPE_B_FALLING_LIMIT_PX 10.0f
#define SHB_TYPE_C_VELOCITY_LIMIT_PX 14.0f
#define SHB_TYPE_C_RISING_LIMIT_PX (-10.0f)
#define SHB_TYPE_D_RISING_VELOCITY_PX (-1.0f)
#define SHB_TYPE_D_SMOKE_HEIGHT_PX 64.0f
#define SHB_TYPE_B_CENTRAL_Y_OFFSET_PX 32
#define SHB_TYPE_B_INITIAL_RADIUS_PX 256.0f
#define SHB_TYPE_B_ANGLE 0x40
#define SHB_LINE_FRAME_COUNT 2
#define SHB_BACKGROUND_A_END_PHASE 4
#define SHB_BACKGROUND_B_END_PHASE 8
#define SHB_BACKGROUND_C_END_PHASE 12

#ifdef __cplusplus
extern "C" {
#endif
/* Independent near DATA objects, all from their original C publics. */
extern unsigned char near shinki_bg_linesets_zoomed_out;
extern int near shinki_bg_type_a_particles_alive;
extern unsigned char near shinki_bg_type_b_initialized;
extern unsigned int near shinki_bg_spinline_frame;
extern unsigned char near shinki_bg_type_c_initialized;
extern unsigned char near shinki_bg_type_d_initialized;
#ifdef __cplusplus
}
#include "src/main/boss/exalice/hexagram_rules.hpp"
enum hexagrams_flag_t {
    UNINITIALIZED = XHG_FLAG_UNINITIALIZED,
    TURN_RIGHT = XHG_FLAG_CLOCKWISE,
    TURN_LEFT = XHG_FLAG_COUNTERCLOCKWISE,
    FLAG_COUNT,
};
extern "C" hexagrams_flag_t near hexagrams_flag;
#else
extern unsigned char near hexagrams_flag;
#endif

#endif
