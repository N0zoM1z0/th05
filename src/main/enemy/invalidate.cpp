// enemies_invalidate(): marks the tiles behind each enemy's previous position
// for redrawing. Same algorithm as TH04's.
#pragma option -zCENEMY_INVALIDATE_TEXT -zPmain_01 -k-
#include "src/main/enemy/invalidate.hpp"

// tiles_invalidate_around() reads one 4-byte point from the stack (x in the
// low word, y in the high word). Calling it through this pointer type passes
// the SPPoint as a whole, which gives the original single 32-bit PUSH.
typedef void (near pascal *near EnemyInvalidationPointCall)(const SPPoint center);
typedef char enemy_point_call_is_near[(sizeof(EnemyInvalidationPointCall) == 2) ? 1 : -1];

void near enemies_invalidate(void)
{
    register enemy_t near *enemy;
    register int enemies_left;
    // Set tile_invalidate_box's width and height with one 32-bit store.
    *reinterpret_cast<uint32_t near *>(&tile_invalidate_box) =
        ((static_cast<uint32_t>(ENEMY_H) << 16) | ENEMY_W);
    enemy = enemies;
    enemies_left = ENEMY_COUNT;
    do {
        if((enemy->flag != EF_FREE) && (enemy->flag != EF_ALIVE_FIRST_FRAME)) {
            reinterpret_cast<EnemyInvalidationPointCall>(
                &tiles_invalidate_around
            )(enemy->pos.prev);
        }
        enemy++;
    } while(--enemies_left);
}
