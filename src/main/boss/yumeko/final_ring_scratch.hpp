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

#endif
