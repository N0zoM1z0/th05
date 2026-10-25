// Complete shot/decay storage and the existing four-byte invalidation frame.
#ifndef TH05_MAIN_PLAYER_SHOT_INVALIDATE_HPP
#define TH05_MAIN_PLAYER_SHOT_INVALIDATE_HPP
#include "src/main/player/shot_runtime.hpp"
#include "src/main/hud/overlay.hpp"

// The canonical existing declaration takes complete signed subpixel y/x
// words: x at SS:SP+2, y at+4, with RET4. No new callable ABI is introduced.
#pragma codeseg SHOT_INVALIDATE_TEXT main_01
void near shots_invalidate(void);
#pragma codeseg

typedef char shot_invalidate_shot_is_18[(sizeof(Shot) == 18) ? 1 : -1];
typedef char shot_invalidate_hitshot_is_14[(sizeof(hitshot_t) == 14) ? 1 : -1];
typedef char shot_invalidate_point_is_4[(sizeof(SPPoint) == 4) ? 1 : -1];
#endif
