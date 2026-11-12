// Native sixteen-sprite midboss defeat orbit and original clipping footprint.
// Compile-time semantics only; the actual angle byte remains C-owned DATA.
#ifndef TH05_MAIN_MIDBOSS_DEFEAT_RING_GEOMETRY_HPP
#define TH05_MAIN_MIDBOSS_DEFEAT_RING_GEOMETRY_HPP
#define MDR_SUBPIXEL_SHIFT 4
#define MDR_RING_MAX_RADIUS_PX 48
#define MDR_ORBIT_ANGLE_STEP 0x10
#define MDR_ORBIT_ROTATION_PER_FRAME 1
#define MDR_ORBIT_SPRITE_COUNT 16
#define MDR_SPRITE_CLIP_MARGIN_PX 16
#define MDR_MAX_CLIP_Y_PX 368
#define MDR_MAX_CLIP_X_PX 384
#define MDR_SCREEN_X_OFFSET_PX 16
#endif
