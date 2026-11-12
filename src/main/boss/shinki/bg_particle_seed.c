/* Shinki background's authentic 16-bit uninitialized-particle sentinel. */
#pragma option -zCSHINKI_BG_SEED_TEXT -zPmain_01
#ifdef __cplusplus
#error The original positive-data sentinel is a C initialized object
#endif

#include "src/main/boss/shinki/background_rules.h"

/* A live signed count, initialized to the positive 8-bit sentinel 255. */
int near shinki_bg_type_a_particles_alive = SHB_PARTICLES_UNINITIALIZED;
typedef char shinki_bg_particle_count_word[(sizeof(int) == 2) ? 1 : -1];
