// Full custom-ball state and real shot/motion/sound interfaces.
#ifndef TH05_B4BALL_UPDATE_HPP
#define TH05_B4BALL_UPDATE_HPP
#pragma codeseg SHOT_HIT_TEXT main_01
int far shots_hittest(void);
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki/b4ball.hpp"

extern SPPoint shot_hitbox_center;
extern SPPoint shot_hitbox_radius;
extern unsigned long score_delta;

static const int B4_UPDATE_HIT_RADIUS = 8 * 16;
static const int B4_UPDATE_CLIP_MARGIN = 16 * 16;
static const int B4_UPDATE_SNOW = 212;
static const int B4_UPDATE_DECAY_FIRST = 224;
static const int B4_UPDATE_DECAY_CELS = 4;
static const int B4_UPDATE_KILL_SCORE = 550;
static const int B4_UPDATE_REVENGE_Y_MAX = 240 * 16;

typedef char b4_update_full_point_is_4[(sizeof(PlayfieldPoint) == 4) ? 1 : -1];
typedef char b4_update_full_motion_is_12[(sizeof(PlayfieldMotion) == 12) ? 1 : -1];
typedef char b4_update_live_pool_is_1638[(sizeof(b4ball_t) * B4BALL_COUNT == 1638) ? 1 : -1];
#endif
