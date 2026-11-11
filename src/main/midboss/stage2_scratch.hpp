// Stage 2 midboss: the orbit mover and three-stage controller share these
// bytes of the canonical Boss scratch array. No extra object is allocated.
#ifndef TH05_MAIN_MIDBOSS_STAGE2_SCRATCH_HPP
#define TH05_MAIN_MIDBOSS_STAGE2_SCRATCH_HPP
#include <stddef.h>
struct Midboss2Scratch {
    unsigned char prior_phase_state[14];
    // Signed 8-bit radial drift, held in the original unsigned storage and
    // explicitly cast back to signed char by midboss2_move().
    unsigned char orbit_center_drift;
    // 0 expands the radius, 1 contracts it; reset on the entrance transition.
    unsigned char orbit_contracting;
};
typedef char midboss2_scratch_is_16[(sizeof(Midboss2Scratch) == 16) ? 1 : -1];
typedef char midboss2_speed_at_14[(offsetof(Midboss2Scratch, orbit_center_drift) == 14) ? 1 : -1];
typedef char midboss2_direction_at_15[(offsetof(Midboss2Scratch, orbit_contracting) == 15) ? 1 : -1];
#define midboss2_scratch (*reinterpret_cast<Midboss2Scratch near *>(boss_statebyte))

static const unsigned char MIDBOSS2_PHASE_ENTRANCE = 0;
static const unsigned char MIDBOSS2_PHASE_ORBIT_ATTACK = 1;
static const unsigned char MIDBOSS2_PHASE_FINAL_ATTACK = 2;
static const unsigned char MIDBOSS2_ORBIT_EXPANDING = 0;
static const unsigned char MIDBOSS2_ORBIT_CONTRACTING = 1;
static const unsigned char MIDBOSS2_ORBIT_DRIFT_INITIAL = 0x20;
#endif
