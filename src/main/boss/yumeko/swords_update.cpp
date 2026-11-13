// Full sword twirling, camera-relative motion, player collision and decay.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include <dos.h>
#include "src/main/boss/yumeko/update.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03
inline bool optimization_barrier(void) { return false; }

#pragma option -O
extern "C" void pascal near swords_update(void)
{
    sword_t near *sword;
    int i;
    sword = swords;
    for(i = 1; i < 1 + SWORD_COUNT; i++, sword++) {
        if(sword->flag != F_FREE) {
        if(bullet_clear_time != 0 && sword->flag == F_ALIVE) {
            sword->flag = F_REMOVE;
            sword->twirl_time = 0;
        }
        if(sword->twirl_time > 0) {
            sword->twirl_time--;
            if(sword->twirl_time == 0) {
                sword->patnum_tiny = bullet_patnum_for_angle(193, sword->angle);
                snd_se_play(3);
            } else {
                if((i & 1) != 0) {
                    sword->patnum_tiny += 2;
                    if(sword->patnum_tiny >= 225) {
                        sword->patnum_tiny -= 32;
                    }
                } else {
                    sword->patnum_tiny -= 2;
                    if(sword->patnum_tiny < 193) {
                        sword->patnum_tiny += 32;
                    }
                }
                continue;
            }
        }
        // Both genuine Point-return words are dead before any foreign call.
        sword->pos.update_seg3();
        if(static_cast<subpixel_t>(_AX) <= -16 * 16 ||
           static_cast<subpixel_t>(_AX) >= (PLAYFIELD_W + 16) * 16 ||
           static_cast<subpixel_t>(_DX) <= -16 * 16 ||
           static_cast<subpixel_t>(_DX) >= (PLAYFIELD_H + 16) * 16) {
            optimization_barrier();
            sword->flag = F_FREE;
            continue;
        }
        if(sword->flag != F_REMOVE) {
            _AX -= player_pos.cur.x.v;
            _DX -= player_pos.cur.y.v;
            if(static_cast<unsigned int>(static_cast<subpixel_t>(_AX) + 7 * 16) <= 14 * 16) {
                _DX += 7 * 16;
                if(static_cast<unsigned int>(_DX) <= 14 * 16) {
                    player_is_hit = 1;
                    sword->flag = F_REMOVE;
                    continue;
                }
            }
            optimization_barrier();
            continue;
        }
        if(sword->patnum_tiny < 225) {
            sword->patnum_tiny = 225;
            sword->pos.velocity.x.v /= 2;
            sword->pos.velocity.y.v /= 2;
            sword->decay_frame = 0;
        } else {
            sword->decay_frame++;
            if((sword->decay_frame % 4) == 0) {
                sword->patnum_tiny++;
                if(sword->patnum_tiny >= 229) {
remove:
                    sword->flag = F_FREE;
                }
            }
        }
        }
    }
}
