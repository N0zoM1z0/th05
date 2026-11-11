// Stage-four midboss writes into the existing sixteen Boss scratch bytes.
// The last three slots carry the lifetime of the four pattern callbacks.
#ifndef TH05_MAIN_MIDBOSS_STAGE4_SCRATCH_HPP
#define TH05_MAIN_MIDBOSS_STAGE4_SCRATCH_HPP
#include <stddef.h>
struct Midboss4Scratch {
    unsigned char other_stage_state[13];
    unsigned char completed_patterns;
    unsigned char current_pattern;
    unsigned char shot_vulnerable;
};
typedef char midboss4_scratch_size_is_16[(sizeof(Midboss4Scratch) == 16) ? 1 : -1];
typedef char midboss4_completed_at_13[(offsetof(Midboss4Scratch, completed_patterns) == 13) ? 1 : -1];
typedef char midboss4_pattern_at_14[(offsetof(Midboss4Scratch, current_pattern) == 14) ? 1 : -1];
typedef char midboss4_vulnerable_at_15[(offsetof(Midboss4Scratch, shot_vulnerable) == 15) ? 1 : -1];
#define midboss4_scratch (*reinterpret_cast<Midboss4Scratch near *>(boss_statebyte))
#endif
