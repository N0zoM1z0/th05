// Semantic donor: maintained TH04 src/main/enemy/enemies_invalidate.cpp.
// Original TH05 interval/stride/flags and call ABI independently reviewed.
#pragma option -zCENEMY_INVALIDATE_TEXT -zPmain_01 -k-
#include "src/main/enemy/invalidate.hpp"

// Legacy Borland ABI view: the original near Pascal entry consumes
// exactly four bytes (x low word, y high word) and RET4. The canonical existing
// symbol remains declared as two words; this cast marshals the same real frame.
// This expresses the observed Borland ABI, not ISO-portable type compatibility.
typedef void (near pascal *near EnemyInvalidationPointCall)(const SPPoint center);
typedef char enemy_point_call_is_near[(sizeof(EnemyInvalidationPointCall) == 2) ? 1 : -1];

void near enemies_invalidate(void)
{
    register enemy_t near *enemy;
    register int enemies_left;
    // Pack the actual complete four-byte width/height object, native endian.
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
