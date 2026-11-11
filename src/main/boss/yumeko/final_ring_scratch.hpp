// Original 16-byte Boss phase scratch area viewed during Yumeko's final ring.
// Previous phases may use the same bytes differently; no extra state is added.
#ifndef TH05_MAIN_BOSS_YUMEKO_FINAL_RING_SCRATCH_HPP
#define TH05_MAIN_BOSS_YUMEKO_FINAL_RING_SCRATCH_HPP

struct YumekoFinalRingScratch {
    unsigned char earlier_phase_state[14];
    unsigned char advancing_angle;
    unsigned char completed_rings;
};

typedef char yumeko_final_scratch_is_16[(sizeof(YumekoFinalRingScratch) == 16) ? 1 : -1];
typedef char yumeko_final_angle_at_14[(offsetof(YumekoFinalRingScratch, advancing_angle) == 14) ? 1 : -1];
typedef char yumeko_final_rings_at_15[(offsetof(YumekoFinalRingScratch, completed_rings) == 15) ? 1 : -1];

#define yumeko_final_scratch (*reinterpret_cast<YumekoFinalRingScratch near *>(boss_statebyte))

// Before the final ring, byte 15 means the mirrored fan side, not an emitted
// ring count. The final-ring initializer replaces this previous value with 0.
// Both views overlap the *same original* boss_statebyte[15] memory cell.
struct YumekoFanScratch {
    unsigned char earlier_phase_state[15];
    unsigned char mirrored_side;
};
typedef char yumeko_fan_scratch_is_16[(sizeof(YumekoFanScratch) == 16) ? 1 : -1];
typedef char yumeko_fan_side_at_15[(offsetof(YumekoFanScratch, mirrored_side) == 15) ? 1 : -1];
#define yumeko_fan_scratch (*reinterpret_cast<YumekoFanScratch near *>(boss_statebyte))

// Movement/reposition vs active callback are original Boss mode values.
static const unsigned char YUMEKO_MODE_REPOSITION = 0;
static const unsigned char YUMEKO_MODE_ATTACK = 1;
static const unsigned char YUMEKO_FAN_NORMAL_SIDE = 0;
static const unsigned char YUMEKO_FAN_MIRRORED_SIDE = 1;
static const unsigned char YUMEKO_WAVE_PATTERN_LIMIT = 20;

#endif
