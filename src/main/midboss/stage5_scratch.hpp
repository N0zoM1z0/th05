// The Stage 5 midboss attack controller and its pattern helpers share the
// original sixteen Boss scratch bytes; this is a typed view, not new storage.
#ifndef TH05_MAIN_MIDBOSS_STAGE5_SCRATCH_HPP
#define TH05_MAIN_MIDBOSS_STAGE5_SCRATCH_HPP
#include <stddef.h>
struct Midboss5Scratch {
    unsigned char prior_stage_state[13];
    unsigned char patterns_done;
    unsigned char current_pattern_phase;
    // Four-state horizontal movement cycle, reset on entry to attacks.
    unsigned char horizontal_step;
};
typedef char midboss5_scratch_is_16[(sizeof(Midboss5Scratch) == 16) ? 1 : -1];
typedef char midboss5_patterns_at_13[(offsetof(Midboss5Scratch, patterns_done) == 13) ? 1 : -1];
typedef char midboss5_mode_at_14[(offsetof(Midboss5Scratch, current_pattern_phase) == 14) ? 1 : -1];
typedef char midboss5_step_at_15[(offsetof(Midboss5Scratch, horizontal_step) == 15) ? 1 : -1];
#define midboss5_scratch (*reinterpret_cast<Midboss5Scratch near *>(boss_statebyte))
#endif
