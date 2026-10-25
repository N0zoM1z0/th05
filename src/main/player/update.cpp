// Natural maintained TH04 player-update donor with original TH05 control flow.
#pragma option -zCPLAYER_UPDATE_TEXT -zPmain_01
#include "src/main/player/update.hpp"
#pragma codeseg PLAYER_UPDATE_TEXT main_01

void near player_update(void)
{
    bool retry;
    player_input_t input;

    if(player_invincibility_time != 0) {
        player_invincibility_time--;
        player_is_hit = false;
    } else if(player_is_hit) {
        miss_time = PLAYER_UPDATE_DEATHBOMB_TIME;
        player_is_hit = false;
        player_invincibility_time = PLAYER_UPDATE_INVINCIBILITY;
        player_respawn_motion_time = PLAYER_UPDATE_RESPAWN_TIME;
        player_pos.velocity.x.v = 0;
        player_pos.velocity.y.v = 0;
    }

    if(player_respawn_motion_time == 0) {
        player_pos.velocity.x.v = 0;
        player_pos.velocity.y.v = 0;
        input = (key_det & PLAYER_UPDATE_MOVEMENT);
        retry = true;
        do {
            if((player_move(input) != MOVE_INVALID) || !retry || (player_input_prev == input)) {
                break;
            }
            input &= ~player_input_prev;
            retry = false;
        } while(true);

        if(shiftkey) {
            player_pos.velocity.x.v /= 2;
            player_pos.velocity.y.v /= 2;
        }
        player_pos_update_and_clamp();
        if(retry) {
            player_input_prev = input;
        }

        if((key_det & PLAYER_UPDATE_INPUT_SHOT) && (shot_time == 0)) {
            shot_time = PLAYER_UPDATE_SHOT_CYCLE;
        }
        if(shot_time > PLAYER_UPDATE_SHOT_CYCLE) {
            shot_time = 0;
        }
        if(shot_time != 0) {
            playchar_shot_func();
            shot_time--;
        }
    } else {
        // Discard the genuine full-point result; the real method updates motion.
        player_pos.update_seg1();
        player_respawn_motion_time--;
    }

    player_option_pos_prev = player_option_pos_cur;
    player_option_pos_cur = player_pos.cur;
    player_option_pos_cur.x.v -= player_pos.velocity.x.v;
    player_option_pos_cur.y.v -= player_pos.velocity.y.v;

    if(key_det & PLAYER_UPDATE_INPUT_BOMB) {
        player_bomb();
    }
    if(miss_time != 0) {
        player_miss_update();
    }
}
