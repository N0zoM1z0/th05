// The Extra midboss's sixteen original Boss scratch bytes. The fight updater
// and five near pattern/movement functions operate on the same physical slots.
#ifndef TH05_MAIN_MIDBOSS_EXTRA_SCRATCH_HPP
#define TH05_MAIN_MIDBOSS_EXTRA_SCRATCH_HPP
#include <stddef.h>
struct MidbossExtraScratch {
    unsigned char earlier_phase_state[12];
    unsigned char second_pattern_set;
    // Written by the rotating ring at frame 94 as +1 or -1 (modulo 256).
    unsigned char ring_rotation;
    unsigned char completed_dashes;
    unsigned char dash_animation_active;
};
typedef char midboss_extra_scratch_is_16[(sizeof(MidbossExtraScratch) == 16) ? 1 : -1];
typedef char midboss_extra_set_at_12[(offsetof(MidbossExtraScratch, second_pattern_set) == 12) ? 1 : -1];
typedef char midboss_extra_rotation_at_13[(offsetof(MidbossExtraScratch, ring_rotation) == 13) ? 1 : -1];
typedef char midboss_extra_dashes_at_14[(offsetof(MidbossExtraScratch, completed_dashes) == 14) ? 1 : -1];
typedef char midboss_extra_animation_at_15[(offsetof(MidbossExtraScratch, dash_animation_active) == 15) ? 1 : -1];
#define midboss_extra_scratch (*reinterpret_cast<MidbossExtraScratch near *>(boss_statebyte))

static const unsigned char MIDBOSSX_PHASE_ENTRANCE_DASH = 0;
static const unsigned char MIDBOSSX_PHASE_ATTACK_DASHES = 1;
static const unsigned char MIDBOSSX_PHASE_LARGE_EXPLOSION = 254;
static const unsigned char MIDBOSSX_SECOND_PATTERN_SET = 1;
static const unsigned char MIDBOSSX_DASH_ACTIVE = 1;
static const int MIDBOSSX_DASH_ANGLE_TABLE_MASK = 7;
static const unsigned char MIDBOSSX_ATTACK_CHOICE_MODULUS = 2;
static const int MIDBOSSX_ATTACK_DASH_FRAME_BIAS = 64;
static const int MIDBOSSX_MAX_COMPLETED_DASHES = 20;

// The near dash helper operates in five distinct animation intervals.
static const int MIDBOSSX_DASH_ANTICIPATION_FRAME = -8;
static const int MIDBOSSX_DASH_MOVING_FRAMES = 30;
static const int MIDBOSSX_DASH_ATTACK_START_FRAME = 40;
static const int MIDBOSSX_RING_ROTATION_FRAME = 94;
static const int MIDBOSSX_RING_ACTIVE_END_FRAME = 114;
static const int MIDBOSSX_ATTACK_END_FRAME = 128;
#endif
