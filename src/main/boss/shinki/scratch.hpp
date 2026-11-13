// The original sixteen Boss scratch bytes are shared across Shinki phases.
// The same byte can intentionally pass state between attack modes; it is not
// cleared automatically by the phase switch. No new storage is allocated.
#ifndef TH05_MAIN_BOSS_SHINKI_SCRATCH_HPP
#define TH05_MAIN_BOSS_SHINKI_SCRATCH_HPP

// One physical byte changes meaning across the original phase boundary.
// The Devil attack's laser latch is the same byte that the surrounding
// controller uses as its shared-wave index; the value is intentionally kept
// alive across the callback so the next phase can observe it.
union ShinkiWaveOrDevilLaserLatch {
    unsigned char wave_relative_index;
    unsigned char devil_lasers_active;
};

typedef char shinki_wave_latch_union_is_1[(sizeof(ShinkiWaveOrDevilLaserLatch) == 1) ? 1 : -1];

typedef struct ShinkiPhaseScratch {
    unsigned char prior_phase_state[10];
    ShinkiWaveOrDevilLaserLatch wave_or_laser;
    unsigned char other_state[3];
    // These bytes are pattern_devil()'s inner/outer bullet angles in phase 10.
    unsigned char spiral_pellet_angle;
    unsigned char spiral_red_angle;
};
typedef char shinki_scratch_is_16[(sizeof(ShinkiPhaseScratch) == 16) ? 1 : -1];
typedef char shinki_wave_latch_at_10[(offsetof(ShinkiPhaseScratch, wave_or_laser) == 10) ? 1 : -1];
typedef char shinki_wave_index_at_union_zero[(offsetof(ShinkiWaveOrDevilLaserLatch, wave_relative_index) == 0) ? 1 : -1];
typedef char shinki_devil_latch_at_union_zero[(offsetof(ShinkiWaveOrDevilLaserLatch, devil_lasers_active) == 0) ? 1 : -1];
typedef char shinki_pellet_angle_at_14[(offsetof(ShinkiPhaseScratch, spiral_pellet_angle) == 14) ? 1 : -1];
typedef char shinki_red_angle_at_15[(offsetof(ShinkiPhaseScratch, spiral_red_angle) == 15) ? 1 : -1];

#define shinki_scratch (*reinterpret_cast<ShinkiPhaseScratch near *>(boss_statebyte))

// During pattern_devil(), all nine final bytes form a different, contiguous
// protocol. In particular, byte 10 switches from wave index to laser latch;
// bytes 14/15 become inner/outer spread angles. The laser latch survives
// long enough to select the next shared wave; final circles reinitialize
// their own angle state at the start of the twirl.
struct ShinkiDevilScratch {
    unsigned char prior_phase_state[7];
    unsigned char laser_direction;
    unsigned char laser_angle_inner;
    unsigned char laser_angle_outer;
    unsigned char lasers_active;
    unsigned char bullet_direction;
    unsigned char bullet_intro_done;
    unsigned char b6ball_interval;
    unsigned char bullet_angle_inner;
    unsigned char bullet_angle_outer;
};
typedef char shinki_devil_scratch_is_16[(sizeof(ShinkiDevilScratch) == 16) ? 1 : -1];
typedef char shinki_devil_laser_direction_at_7[(offsetof(ShinkiDevilScratch, laser_direction) == 7) ? 1 : -1];
typedef char shinki_devil_laser_latch_at_10[(offsetof(ShinkiDevilScratch, lasers_active) == 10) ? 1 : -1];
typedef char shinki_devil_bullet_interval_at_13[(offsetof(ShinkiDevilScratch, b6ball_interval) == 13) ? 1 : -1];
typedef char shinki_devil_inner_angle_at_14[(offsetof(ShinkiDevilScratch, bullet_angle_inner) == 14) ? 1 : -1];
typedef char shinki_devil_outer_angle_at_15[(offsetof(ShinkiDevilScratch, bullet_angle_outer) == 15) ? 1 : -1];

#define shinki_devil_scratch (*reinterpret_cast<ShinkiDevilScratch near *>(boss_statebyte))

#endif
