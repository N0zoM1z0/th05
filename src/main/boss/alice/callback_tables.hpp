// Complete Alice puppet and four-wave attack callback schedule interfaces.
#ifndef TH05_ALICE_CALLBACK_TABLES_HPP
#define TH05_ALICE_CALLBACK_TABLES_HPP
#include "src/main/boss/alice/puppet_patterns.hpp"

typedef bool (near pascal *near AlicePuppetPattern)(AlicePuppet near &puppet);
typedef void (near *near AlicePattern)(void);

#pragma codeseg ALICE_OPN_TEXT main_03
void near alice_pattern_opening_cycle(void);
void near alice_pattern_ring_stack(void);
void near alice_pattern_spread_stack(void);
#pragma codeseg ALICE_CHG_TEXT main_03
void near alice_pattern_laser_fan(void);
void near alice_pattern_paired_stacks(void);
void near alice_pattern_rotating_ring(void);
#pragma codeseg ALICE_CALLBACK_TABLE_TEXT main_03

extern const AlicePuppetPattern alice_puppet_choices[4];
extern AlicePattern alice_pattern_table[4][3];
typedef char alice_puppet_callback_word[(sizeof(AlicePuppetPattern) == 2) ? 1 : -1];
typedef char alice_wave_callback_word[(sizeof(AlicePattern) == 2) ? 1 : -1];
typedef char alice_puppet_choices_size[(sizeof(alice_puppet_choices) == 8) ? 1 : -1];
typedef char alice_wave_table_size[(sizeof(alice_pattern_table) == 24) ? 1 : -1];
#endif
