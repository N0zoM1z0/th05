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
    unsigned char wing_palette_tone;
    unsigned char cheeto_wall_interval;
};
union ShinkiSpiralOrDevilOuterAngle {
    unsigned char spiral_red_angle;
    unsigned char devil_bullet_angle_outer;
    unsigned char curved_ring_delta_angle;
    unsigned char dual_speed_ring_interval;
    unsigned char wing_animation_frame;
    unsigned char aimed_b6ball_interval;
    // The original Cheeto-wall callback writes this ranked byte but never
    // reads it; retain the observable store under an honest name.
    unsigned char cheeto_wall_unused_value;
};
typedef char shinki_spiral_inner_angle_is_1[(sizeof(ShinkiSpiralOrDevilInnerAngle) == 1) ? 1 : -1];
typedef char shinki_spiral_outer_angle_is_1[(sizeof(ShinkiSpiralOrDevilOuterAngle) == 1) ? 1 : -1];
typedef char shinki_spiral_pellet_at_union_zero[(offsetof(ShinkiSpiralOrDevilInnerAngle, spiral_pellet_angle) == 0) ? 1 : -1];
typedef char shinki_devil_inner_at_union_zero[(offsetof(ShinkiSpiralOrDevilInnerAngle, devil_bullet_angle_inner) == 0) ? 1 : -1];
typedef char shinki_spiral_red_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, spiral_red_angle) == 0) ? 1 : -1];
typedef char shinki_devil_outer_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, devil_bullet_angle_outer) == 0) ? 1 : -1];
typedef char shinki_wing_tone_at_union_zero[(offsetof(ShinkiSpiralOrDevilInnerAngle, wing_palette_tone) == 0) ? 1 : -1];
typedef char shinki_cheeto_interval_at_union_zero[(offsetof(ShinkiSpiralOrDevilInnerAngle, cheeto_wall_interval) == 0) ? 1 : -1];
typedef char shinki_curved_ring_delta_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, curved_ring_delta_angle) == 0) ? 1 : -1];
typedef char shinki_dual_ring_interval_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, dual_speed_ring_interval) == 0) ? 1 : -1];
typedef char shinki_wing_frame_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, wing_animation_frame) == 0) ? 1 : -1];
typedef char shinki_aimed_b6ball_interval_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, aimed_b6ball_interval) == 0) ? 1 : -1];
typedef char shinki_cheeto_unused_at_union_zero[(offsetof(ShinkiSpiralOrDevilOuterAngle, cheeto_wall_unused_value) == 0) ? 1 : -1];

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

// Additional full-size views for the wing transition, ranked Cheeto walls,
// and late symmetric B6-ball wave. These are aliases of the same sixteen
// bytes, not independent state objects.
struct ShinkiWingPreparationScratch {
    unsigned char prior_phase_state[14];
    ShinkiSpiralOrDevilInnerAngle tone;
    ShinkiSpiralOrDevilOuterAngle frame;
};
typedef char shinki_wing_scratch_is_16[(sizeof(ShinkiWingPreparationScratch) == 16) ? 1 : -1];
typedef char shinki_wing_tone_at_14[(offsetof(ShinkiWingPreparationScratch, tone) == 14) ? 1 : -1];
typedef char shinki_wing_frame_at_15[(offsetof(ShinkiWingPreparationScratch, frame) == 15) ? 1 : -1];

struct ShinkiCheetoWallScratch {
    unsigned char prior_phase_state[14];
    ShinkiSpiralOrDevilInnerAngle ranked_interval;
    ShinkiSpiralOrDevilOuterAngle ranked_unused_value;
};
typedef char shinki_cheeto_wall_scratch_is_16[(sizeof(ShinkiCheetoWallScratch) == 16) ? 1 : -1];
typedef char shinki_cheeto_interval_at_14[(offsetof(ShinkiCheetoWallScratch, ranked_interval) == 14) ? 1 : -1];
typedef char shinki_cheeto_unused_at_15[(offsetof(ShinkiCheetoWallScratch, ranked_unused_value) == 15) ? 1 : -1];

struct ShinkiAimedB6BallScratch {
    unsigned char prior_phase_state[15];
    ShinkiSpiralOrDevilOuterAngle ranked_interval;
};
typedef char shinki_aimed_b6ball_scratch_is_16[(sizeof(ShinkiAimedB6BallScratch) == 16) ? 1 : -1];
typedef char shinki_aimed_b6ball_interval_at_15[(offsetof(ShinkiAimedB6BallScratch, ranked_interval) == 15) ? 1 : -1];

#define shinki_wing_scratch (*reinterpret_cast<ShinkiWingPreparationScratch near *>(boss_statebyte))
#define shinki_cheeto_wall_scratch (*reinterpret_cast<ShinkiCheetoWallScratch near *>(boss_statebyte))
#define shinki_aimed_b6ball_scratch (*reinterpret_cast<ShinkiAimedB6BallScratch near *>(boss_statebyte))

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
