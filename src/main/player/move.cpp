// Natural maintained TH04 move.cpp algorithm, GAME5 dynamic signed speeds.
// TH05 additionally ignores the highest four input bits before dispatch.
#pragma option -zCPLAYER_MOVE_TEXT -zPmain_01 -k-
#include "src/main/player/move.hpp"
#pragma codeseg PLAYER_MOVE_TEXT main_01
// The maintained donor requests ordinary word alignment for its switch data.
#pragma option -a2

inline void player_move_velocity(int direction_x, int direction_y)
{
    if((direction_x != 0) && (direction_y != 0)) {
        player_pos.velocity.x.v = direction_x * playchar_speed_diagonal;
        player_pos.velocity.y.v = direction_y * playchar_speed_diagonal;
    } else if(direction_x != 0) {
        player_pos.velocity.x.v = direction_x * playchar_speed_aligned;
    } else if(direction_y != 0) {
        player_pos.velocity.y.v = direction_y * playchar_speed_aligned;
    }
}

move_ret_t pascal near player_move(player_input_t input)
{
    move_ret_t ret = MOVE_VALID;
    switch(input & PLAYER_INPUT_USED_BITS) {
    case PLAYER_INPUT_NONE:
        ret = MOVE_NOINPUT; break;
    case PLAYER_INPUT_LEFT:
        player_move_velocity(-1, 0); break;
    case (PLAYER_INPUT_DOWN | PLAYER_INPUT_LEFT):
    case PLAYER_INPUT_DOWN_LEFT:
        player_move_velocity(-1, +1); break;
    case PLAYER_INPUT_DOWN:
        player_move_velocity(0, +1); break;
    case (PLAYER_INPUT_DOWN | PLAYER_INPUT_RIGHT):
    case PLAYER_INPUT_DOWN_RIGHT:
        player_move_velocity(+1, +1); break;
    case PLAYER_INPUT_RIGHT:
        player_move_velocity(+1, 0); break;
    case (PLAYER_INPUT_UP | PLAYER_INPUT_RIGHT):
    case PLAYER_INPUT_UP_RIGHT:
        player_move_velocity(+1, -1); break;
    case PLAYER_INPUT_UP:
        player_move_velocity(0, -1); break;
    case (PLAYER_INPUT_UP | PLAYER_INPUT_LEFT):
    case PLAYER_INPUT_UP_LEFT:
        player_move_velocity(-1, -1); break;
    default:
        ret = MOVE_INVALID; break;
    }
    return ret;
}
