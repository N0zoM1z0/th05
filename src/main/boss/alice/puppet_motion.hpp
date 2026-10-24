// Canonical puppet storage and real movement/dispatcher foreign interfaces.
#ifndef TH05_MAIN_BOSS_ALICE_PUPPET_MOTION_HPP
#define TH05_MAIN_BOSS_ALICE_PUPPET_MOTION_HPP
#include "src/main/boss/alice/beam.hpp"
#pragma codeseg SHARED
#include "src/shared/math/vector.hpp"
#pragma codeseg MAIN_01_TEXT main_01
int far shots_hittest(void);
#pragma codeseg ALICE_PMV_TEXT main_03

typedef bool (near pascal *near AliceMotionPattern)(AlicePuppet near &puppet);
extern AliceMotionPattern alice_puppet_pattern0;
extern AliceMotionPattern alice_puppet_pattern1;
extern AliceMotionPattern alice_puppet_pattern_table[4];
extern unsigned long score_delta;
bool pascal near alice_puppet_recover(AlicePuppet near &puppet);
void near alice_puppets_entrance(void);
void near alice_puppets_update(void);

typedef char alice_motion_pattern_pointer_is_near[(sizeof(AliceMotionPattern) == 2) ? 1 : -1];
typedef char alice_motion_pattern_table_is_8[(sizeof(alice_puppet_pattern_table) == 8) ? 1 : -1];
#endif
