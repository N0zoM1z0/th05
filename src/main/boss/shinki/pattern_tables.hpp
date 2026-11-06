// Canonical byte-bool near callbacks and the actual two-phase schedule.
#ifndef TH05_SHINKI_PATTERN_TABLES_HPP
#define TH05_SHINKI_PATTERN_TABLES_HPP
#include "src/main/boss/shinki/shinki.hpp"

#pragma codeseg B6_UPDATE_TEXT main_03
bool near pattern_random_directional_and_kunai(void);
bool near pattern_dense_blue_stacks(void);
#pragma codeseg B6_TABLES_TEXT main_03

extern const pattern_oneshot_func_t SHINKI_PATTERNS_PHASE_2_3[2][2];
typedef char shinki_table_pointer_is_2[(sizeof(pattern_oneshot_func_t) == 2) ? 1 : -1];
typedef char shinki_phase_table_is_8[(sizeof(SHINKI_PATTERNS_PHASE_2_3) == 8) ? 1 : -1];
#endif
