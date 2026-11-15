// Declarations for player movement (TH04 move.hpp, th04/hardware/inputvar.h).
#ifndef TH05_MAIN_PLAYER_MOVE_HPP
#define TH05_MAIN_PLAYER_MOVE_HPP
#include "src/main/player/player.hpp"

// The 16-bit input word. Named apart from input_t, which another header defines.
typedef uint16_t player_input_t;
static const player_input_t PLAYER_INPUT_NONE = 0;
static const player_input_t PLAYER_INPUT_UP = 0x0001;
static const player_input_t PLAYER_INPUT_DOWN = 0x0002;
static const player_input_t PLAYER_INPUT_LEFT = 0x0004;
static const player_input_t PLAYER_INPUT_RIGHT = 0x0008;
static const player_input_t PLAYER_INPUT_UP_LEFT = 0x0100;
static const player_input_t PLAYER_INPUT_UP_RIGHT = 0x0200;
static const player_input_t PLAYER_INPUT_DOWN_LEFT = 0x0400;
static const player_input_t PLAYER_INPUT_DOWN_RIGHT = 0x0800;
static const player_input_t PLAYER_INPUT_USED_BITS = 0x0FFF;

// Separate signed word globals; the unused words after them belong to no object.
extern subpixel_t playchar_speed_aligned;
extern subpixel_t playchar_speed_diagonal;
enum move_ret_t { MOVE_INVALID = 0, MOVE_VALID = 1, MOVE_NOINPUT = 2 };
// Caller clears velocity; cardinal cases deliberately leave the other axis.
move_ret_t pascal near player_move(player_input_t input);

typedef char player_move_input_is_word[(sizeof(player_input_t) == 2) ? 1 : -1];
typedef char player_move_result_is_byte[(sizeof(move_ret_t) == 1) ? 1 : -1];
typedef char player_move_aligned_is_word[(sizeof(playchar_speed_aligned) == 2) ? 1 : -1];
typedef char player_move_diagonal_is_word[(sizeof(playchar_speed_diagonal) == 2) ? 1 : -1];
#endif
