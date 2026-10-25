// Natural TH05 custom-ball motion, collision, destruction and revenge shots.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include <dos.h>
#include "src/main/boss/mai_yuki/b4ball_update.hpp"
#pragma codeseg MAIN_035_TEXT main_03

extern "C" void pascal near b4balls_update(void)
{
    int damage;
    b4ball_t near *ball;
    int i;

    shot_hitbox_radius.x.v = B4_UPDATE_HIT_RADIUS;
    shot_hitbox_radius.y.v = B4_UPDATE_HIT_RADIUS;
    for((ball = b4balls, i = 1); i < (1 + B4BALL_COUNT); (i++, ball++)) {
        if(ball->flag == F_FREE) {
            continue;
        }
        ball->age++;
        // Borrow the actual packed Point return through the DOS intrinsics.
        // Both coordinates are consumed before the first collision helper.
        ball->pos.update_seg3();
        if(static_cast<subpixel_t>(_AX) <= -B4_UPDATE_CLIP_MARGIN ||
           static_cast<subpixel_t>(_AX) >= (PLAYFIELD_W * 16) + B4_UPDATE_CLIP_MARGIN ||
           static_cast<subpixel_t>(_DX) <= -B4_UPDATE_CLIP_MARGIN ||
           static_cast<subpixel_t>(_DX) >= (PLAYFIELD_H * 16) + B4_UPDATE_CLIP_MARGIN) {
            ball->flag = F_FREE;
            continue;
        }
        if(ball->flag != F_REMOVE) {
            if(static_cast<unsigned int>(static_cast<subpixel_t>(_AX) - player_pos.cur.x.v +
                    B4_UPDATE_HIT_RADIUS) <= (2 * B4_UPDATE_HIT_RADIUS) &&
               static_cast<unsigned int>(static_cast<subpixel_t>(_DX) - player_pos.cur.y.v +
                    B4_UPDATE_HIT_RADIUS) <= (2 * B4_UPDATE_HIT_RADIUS)) {
                player_is_hit = 1;
            }
            // The original reloads the real current position at this boundary;
            // no returned coordinate is kept across the shot-collision call.
            shot_hitbox_center = ball->pos.cur;
            if((damage = shots_hittest()) != 0) {
                if(ball->patnum_tiny_base != B4_UPDATE_SNOW) {
                    snd_se_play(10);
                } else {
                    ball->damaged_this_frame = 1;
                    ball->hp -= damage;
                    snd_se_play(4);
                    if(ball->hp < 0) {
                        ball->flag++;
                        ball->age = 0;
                        ball->patnum_tiny_base = B4_UPDATE_DECAY_FIRST;
                        // Signed division preserves truncation toward zero.
                        ball->pos.velocity.x.v /= 4;
                        ball->pos.velocity.y.v /= 4;
                        score_delta += B4_UPDATE_KILL_SCORE;
                        if(ball->revenge != 0 &&
                           ball->pos.cur.y.v <= B4_UPDATE_REVENGE_Y_MAX) {
                            bullet_template.origin = ball->pos.cur;
                            bullets_add_regular();
                        }
                        snd_se_play(3);
                    }
                }
            }
        } else if((ball->age & 3) == 0) {
            ball->patnum_tiny_base++;
            if(ball->patnum_tiny_base >=
                    B4_UPDATE_DECAY_FIRST + B4_UPDATE_DECAY_CELS) {
                ball->flag = F_FREE;
            }
        }
    }
}
