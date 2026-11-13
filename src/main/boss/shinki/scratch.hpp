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

// The final spiral phase reinitializes these two bytes after Devil's inner
// and outer bullet angles have served their own attack lifetime.
union ShinkiSpiralOrDevilInnerAngle {
    unsigned char spiral_pellet_angle;
    unsigned char devil_bullet_angle_inner;
};
union ShinkiSpiralOrDevilOuterAngle {
    unsigned char spiral_red_angle;
    unsigned char devil_bullet_angle_outer;
};
typedef char shinki_spiral_inner_angle_is_1[(sizeof(ShinkiSpiralOrDevilInnerAngle) == 1) ? 1 : -1];
typedef char shinki_spiral_outer_angle_is_1[(sizeof(ShinkiSpiralOrDevilOuterAngle) == 1) ? 1 : -1];
typedef char shinki_spiral_pellet_at_union_zero[(offsetof(ShinkiSpiralOrDevilInnerAngle, spiral_pellet_angle) == 0) ? 1 : -1];
typedef char shinki_devil_inner_at_union_zero[(offsetof(ShinkiSpiralOrDevilInnerAngle, devil_bullet_angle_inner) == 0) ? 1 : -1];
typedef char shinki_spiral_red_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, spiral_red_angle) == 0) ? 1 : -1];
typedef char shinki_devil_outer_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, devil_bullet_angle_outer) == 0) ? 1 : -1];

typedef struct ShinkiPhaseScratch {
    unsigned char prior_phase_state[10];
    ShinkiWaveOrDevilLaserLatch wave_or_laser;
    unsigned char other_state[3];
    ShinkiSpiralOrDevilInnerAngle spiral_or_devil_inner_angle;
    ShinkiSpiralOrDevilOuterAngle spiral_or_devil_outer_angle;
};
typedef char shinki_scratch_is_16[(sizeof(ShinkiPhaseScratch) == 16) ? 1 : -1];
typedef char shinki_wave_latch_at_10[(offsetof(ShinkiPhaseScratch, wave_or_laser) == 10) ? 1 : -1];
typedef char shinki_wave_index_at_union_zero[(offsetof(ShinkiWaveOrDevilLaserLatch, wave_relative_index) == 0) ? 1 : -1];
typedef char shinki_devil_latch_at_union_zero[(offsetof(ShinkiWaveOrDevilLaserLatch, devil_lasers_active) == 0) ? 1 : -1];
typedef char shinki_pellet_angle_at_14[(offsetof(ShinkiPhaseScratch, spiral_or_devil_inner_angle) == 14) ? 1 : -1];
typedef char shinki_red_angle_at_15[(offsetof(ShinkiPhaseScratch, spiral_or_devil_outer_angle) == 15) ? 1 : -1];

#define shinki_scratch (*reinterpret_cast<ShinkiPhaseScratch near *>(boss_statebyte))

// During pattern_devil(), all nine final bytes form a different, contiguous
// protocol. In particular, byte 10 switches from wave index to laser latch;
// bytes 14/15 become the Devil's inner/outer bullet angles, then are reused
// by final circles as pellet/red angles. The laser latch survives long enough
// to select the next shared wave; final circles reinitialize both angles at
// the start of the twirl.
struct ShinkiDevilScratch {
    unsigned char prior_phase_state[7];
    unsigned char laser_direction;
    unsigned char laser_angle_inner;
    unsigned char laser_angle_outer;
    ShinkiWaveOrDevilLaserLatch wave_or_laser;
    unsigned char bullet_direction;
    unsigned char bullet_intro_done;
    unsigned char b6ball_interval;
    ShinkiSpiralOrDevilInnerAngle spiral_or_devil_inner_angle;
    ShinkiSpiralOrDevilOuterAngle spiral_or_devil_outer_angle;
};
typedef char shinki_devil_scratch_is_16[(sizeof(ShinkiDevilScratch) == 16) ? 1 : -1];
typedef char shinki_devil_laser_direction_at_7[(offsetof(ShinkiDevilScratch, laser_direction) == 7) ? 1 : -1];
typedef char shinki_devil_laser_latch_at_10[(offsetof(ShinkiDevilScratch, wave_or_laser) == 10) ? 1 : -1];
typedef char shinki_phase_devil_latch_offsets_match[(
    offsetof(ShinkiPhaseScratch, wave_or_laser) ==
    offsetof(ShinkiDevilScratch, wave_or_laser)
) ? 1 : -1];
typedef char shinki_devil_bullet_interval_at_13[(offsetof(ShinkiDevilScratch, b6ball_interval) == 13) ? 1 : -1];
typedef char shinki_devil_inner_angle_at_14[(offsetof(ShinkiDevilScratch, spiral_or_devil_inner_angle) == 14) ? 1 : -1];
typedef char shinki_devil_outer_angle_at_15[(offsetof(ShinkiDevilScratch, spiral_or_devil_outer_angle) == 15) ? 1 : -1];
typedef char shinki_phase_devil_inner_angle_offsets_match[(
    offsetof(ShinkiPhaseScratch, spiral_or_devil_inner_angle) ==
    offsetof(ShinkiDevilScratch, spiral_or_devil_inner_angle)
) ? 1 : -1];
typedef char shinki_phase_devil_outer_angle_offsets_match[(
    offsetof(ShinkiPhaseScratch, spiral_or_devil_outer_angle) ==
    offsetof(ShinkiDevilScratch, spiral_or_devil_outer_angle)
) ? 1 : -1];

#define shinki_devil_scratch (*reinterpret_cast<ShinkiDevilScratch near *>(boss_statebyte))

#endif
