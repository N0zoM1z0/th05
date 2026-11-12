// Original Alice Boss near-callback dispatch: puppet moves and four main waves.
#pragma option -zCALICE_CALLBACK_TABLE_TEXT -zPmain_03
#include "src/main/boss/alice/callback_tables.hpp"

const AlicePuppetPattern alice_puppet_choices[4] = {
    alice_puppet_initial,
    alice_puppet_spread,
    alice_puppet_aimed_bursts,
    alice_puppet_ring_bursts
};

AlicePattern alice_pattern_table[4][3] = {
    { alice_pattern_opening_cycle, alice_pattern_ring_stack, alice_pattern_spread_stack },
    { alice_pattern_ring_stack, alice_pattern_spread_stack, alice_pattern_paired_stacks },
    { alice_pattern_spread_stack, alice_pattern_laser_fan, alice_pattern_paired_stacks },
    { alice_pattern_laser_fan, alice_pattern_paired_stacks, alice_pattern_rotating_ring }
};
