// Constants of the Stage 2 background ("S2T" = stage 2 transition): the fade
// from the tile map to the particle backdrop, the falling particles, and the
// pulse of palette color 0.
#ifndef TH05_STAGE2_TRANSITION_RULES_HPP
#define TH05_STAGE2_TRANSITION_RULES_HPP

// Transition timeline, in stage frames. The effect is skipped while the boss
// is fighting, and from 32 frames into its entrance animation.
#define S2T_BOSS_ENTRANCE_MAX_FRAME 32
#define S2T_FADE_START_FRAME 256
#define S2T_FADE_END_FRAME 304
#define S2T_SCROLL_END_FRAME 306

// Brightness flash on top of the normal PaletteTone of 100: it rises by 2 per
// frame during the fade and falls by 4 per frame afterwards.
#define S2T_BRIGHTNESS_BASE 100
#define S2T_BRIGHTNESS_INCREMENT 2
#define S2T_BRIGHTNESS_DECREMENT 4

// The tile wipe overwrites columns outward from the two center columns of the
// 24-column, 25-row tile ring, using the source tile at this VRAM row.
#define S2T_SCREEN_WIPE_ROWS 25
#define S2T_SCREEN_WIPE_COLUMNS 24
#define S2T_TILE_WIPE_LEFT_ANCHOR 11
#define S2T_TILE_WIPE_RIGHT_ANCHOR 12
#define S2T_RING_WIPE_SOURCE_Y 256

// Color 0 pulses between these levels, one step every 4 frames. Red and green
// get twice the level, blue four times the level.
#define S2T_PALETTE_PULSE_CEILING 0x3F
#define S2T_PALETTE_PULSE_FLOOR 0x20
#define S2T_PALETTE_RED_GREEN_SCALE 2
#define S2T_PALETTE_BLUE_SCALE 4

// Particles
// ---------
// Each particle flies at a random angle within a 0x20-wide fan, and spawns
// at an X position proportional to its distance from the fan's far edge.
// This makes the particles form one slanted stream. Over a 4096-frame cycle,
// the stream turns between three fans:
//
//      frames  fan                      X offset
//    0..1000   S2T_PARTICLE_ANGLE_DOWN        64
//   ..1128     turning to the left
//   ..2000   S2T_PARTICLE_ANGLE_DOWN_LEFT    128
//   ..2128     turning back
//   ..3000   S2T_PARTICLE_ANGLE_DOWN          64
//   ..3128     turning to the right
//   ..3968   S2T_PARTICLE_ANGLE_DOWN_RIGHT     0
//   ..4096     turning back
//
// While turning, the fan rotates by one angle unit every 8 frames and the
// X offset moves by half a pixel per frame.
#define S2T_PARTICLE_CYCLE_MASK 4095
#define S2T_PARTICLE_PHASE_A_END 1000
#define S2T_PARTICLE_PHASE_A_TURN_END 1128
#define S2T_PARTICLE_PHASE_B_END 2000
#define S2T_PARTICLE_PHASE_B_TURN_END 2128
#define S2T_PARTICLE_PHASE_C_END 3000
#define S2T_PARTICLE_PHASE_C_TURN_END 3128
#define S2T_PARTICLE_PHASE_D_END 3968

#define S2T_PARTICLE_ANGLE_RANGE 0x20
// First angle of each fan
#define S2T_PARTICLE_ANGLE_DOWN_RIGHT 0x20
#define S2T_PARTICLE_ANGLE_DOWN 0x30
#define S2T_PARTICLE_ANGLE_DOWN_LEFT 0x40

#define S2T_PARTICLE_X_PER_ANGLE 8
#define S2T_PARTICLE_X_DOWN_PX 64
#define S2T_PARTICLE_X_DOWN_LEFT_PX 128
#define S2T_PARTICLE_TURN_FRAMES_PER_ANGLE 8
#define S2T_PARTICLE_TURN_X_SUBPIXELS_PER_FRAME 8

// Random extra X offset of 0 to 7 pixels.
#define S2T_PARTICLE_JITTER_SPAN 8
#define S2T_PARTICLE_SUBPIXELS_PER_PX 16

#define S2T_PARTICLE_SPAWN_SPEED_PX 8
#define S2T_PARTICLE_INITIAL_ZOOM 8
// Particles are removed this far outside the playfield.
#define S2T_PARTICLE_CLIP_MARGIN_PX 8
// Size of the tile area redrawn around each particle.
#define S2T_PARTICLE_TILE_FOOTPRINT_PX 8
#endif
