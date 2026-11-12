// Shinki's six-laser wing-opening geometry, visible palette and burst timing.
// These are source-level compile-time values; the existing Boss state bytes
// at 14/15 remain the actual tone and wing-frame countdown storage.
#ifndef TH05_SHINKI_WING_PREPARATION_RULES_HPP
#define TH05_SHINKI_WING_PREPARATION_RULES_HPP

#define SWPREP_START_FRAME 16
#define SWPREP_LASER_COUNT 6
#define SWPREP_R_OUTER_ANGLE 0x50
#define SWPREP_R_INNER_ANGLE 0x48
#define SWPREP_R_CENTER_ANGLE 0x40
#define SWPREP_L_CENTER_ANGLE 0x40
#define SWPREP_L_INNER_ANGLE 0x38
#define SWPREP_L_OUTER_ANGLE 0x30
#define SWPREP_LASER_SWEEP_LIMIT 0x80
#define SWPREP_LASER_TURN_STEP 0x01
#define SWPREP_BASE_TONE 100
#define SWPREP_FLASH_TONE 150
#define SWPREP_WING_VISIBLE_FRAMES 8
#define SWPREP_SPAWN_BULLET_COUNT 50
#define SWPREP_RAIN_ANGLE_MIN 0x10
#define SWPREP_RAIN_ANGLE_END 0x70
#define SWPREP_RAIN_SPEED_MIN 1.5f
#define SWPREP_RAIN_SPEED_MAX 5.5f
#define SWPREP_START_SE 8
#define SWPREP_RELEASE_SE 15
#define SWPREP_SCREEN_SHAKE_FRAMES 8

#endif
