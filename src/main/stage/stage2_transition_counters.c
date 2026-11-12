/* Stage-two transition: native particle count and paired palette clocks. */
#pragma option -zCSTAGE2_TRANSITION_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Original stage-two initialized DATA is produced by C
#endif

#include "src/main/stage/stage2_transition_counters.h"

int near stage2_particles_spawned = 0;
unsigned char near stage2_palette_level = 0;
unsigned char near stage2_tone_offset = 0;

typedef char stage2_particle_count_is_word[
    (sizeof(stage2_particles_spawned) == 2) ? 1 : -1];
typedef char stage2_palette_clock_is_byte[
    (sizeof(stage2_palette_level) == 1) ? 1 : -1];
typedef char stage2_tone_clock_is_byte[
    (sizeof(stage2_tone_offset) == 1) ? 1 : -1];
typedef char stage2_transition_data_is_four[
    ((sizeof(stage2_particles_spawned) + sizeof(stage2_palette_level) +
      sizeof(stage2_tone_offset)) == 4) ? 1 : -1];
