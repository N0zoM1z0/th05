// Real four-phase/two-choice callback schedule with the canonical callback ABI.
#ifndef TH05_EXALICE_PATTERN_PAIRS_HPP
#define TH05_EXALICE_PATTERN_PAIRS_HPP
#include "src/main/boss/exalice/patterns.hpp"

// These are the complete original interfaces from the frozen later/laser/final
// headers. No shortened object layout or alternate calling convention is used.
#pragma codeseg EXALICE_LAT_TEXT main_03
bool near exalice_pattern_gravity_stacks(void);
bool near exalice_pattern_diamond_rings(void);
#pragma codeseg EXALICE_LSR_TEXT main_03
bool near exalice_pattern_bouncing_rings(void);
bool near exalice_pattern_speedup_fans(void);
#pragma codeseg EXALICE_FIN_TEXT main_03
bool near exalice_pattern_cross_cheetos(void);
bool near exalice_pattern_turning_cheetos(void);
#pragma codeseg EXALICE_PAIR_DATA_TEXT main_03

extern exalice_pattern_t exalice_patterns_by_phase[4][2];
typedef char exalice_pair_pointer2[(sizeof(exalice_pattern_t) == 2) ? 1 : -1];
typedef char exalice_pair_schedule16[(sizeof(exalice_patterns_by_phase) == 16) ? 1 : -1];
#endif
