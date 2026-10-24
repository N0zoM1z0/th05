// Real puppet recovery callbacks and opening-phase pattern interfaces.
#ifndef TH05_MAIN_BOSS_ALICE_OPENING_PATTERNS_HPP
#define TH05_MAIN_BOSS_ALICE_OPENING_PATTERNS_HPP
#include "src/main/boss/alice/beam.hpp"

#pragma codeseg B4_UPDATE_TEXT main_03
void pascal near gather_add_only_3stack(int frame,
    unsigned int first_color, unsigned int other_color);
#pragma codeseg ALICE_OPN_TEXT main_03

bool pascal near alice_puppet_recover(AlicePuppet near &puppet);
bool pascal near alice_puppet_hold(AlicePuppet near &puppet);
void near alice_pattern_opening(void);
void near alice_pattern_opening_cycle(void);
void near alice_pattern_ring_stack(void);
void near alice_pattern_spread_stack(void);

static const unsigned char ALICE_OPENING_BALL_BLUE = 44;
static const unsigned char ALICE_OPENING_BALL_RED = 48;
#endif
