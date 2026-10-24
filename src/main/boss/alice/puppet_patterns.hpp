// Complete puppet pattern callbacks using the validated26-byte storage ABI.
#ifndef TH05_MAIN_BOSS_ALICE_PUPPET_PATTERNS_HPP
#define TH05_MAIN_BOSS_ALICE_PUPPET_PATTERNS_HPP
#include "src/main/boss/alice/beam.hpp"

#pragma codeseg CIRCLE_TEXT main_01
// Real far Pascal producer; x/y are signed16-bit subpixel coordinates.
void pascal far circles_add_shrinking(subpixel_t x, subpixel_t y);
#pragma codeseg ALICE_PUP_TEXT main_03
extern unsigned int stage_frame;
#define ALICE_PUPPET_NO_DECELERATE 0x10

bool pascal near alice_puppet_initial(AlicePuppet near &puppet);
bool pascal near alice_puppet_spread(AlicePuppet near &puppet);
bool pascal near alice_puppet_aimed_bursts(AlicePuppet near &puppet);
bool pascal near alice_puppet_ring_bursts(AlicePuppet near &puppet);
bool pascal near alice_puppet_rings(AlicePuppet near &puppet);
#endif
