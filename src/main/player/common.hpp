// Common TH05 shot-control ABI; the complete canonical Shot stays shared.
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47, th05/p_common.cpp
// and th04/main/player/shot.hpp. No shared header is modified.
#ifndef TH05_MAIN_PLAYER_COMMON_HPP
#define TH05_MAIN_PLAYER_COMMON_HPP
#include "src/main/player/reimu.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner is TH05 MAIN common player shot control
#endif
static const int SHOT_COUNT = 64;
extern unsigned char shot_time;
extern Shot near shots[SHOT_COUNT];
extern Shot near *shot_ptr;
extern char shot_last_id;
extern "C" void pascal far snd_se_play(int effect);

char near shot_cycle_init(void);
void pascal near shot_l0(void);
void pascal near shot_l1(void);

typedef char th05_common_shots_is_1152[(sizeof(shots) == 1152) ? 1 : -1];
typedef char th05_common_cycle_time_is_1[(sizeof(shot_time) == 1) ? 1 : -1];
typedef char th05_common_shot_last_id_is_1[(sizeof(shot_last_id) == 1) ? 1 : -1];
#endif
