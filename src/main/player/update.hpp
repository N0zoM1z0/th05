// Actual TH05 input, respawn and shot-dispatch lifecycle, full canonical motion.
#ifndef TH05_PLAYER_UPDATE_HPP
#define TH05_PLAYER_UPDATE_HPP
#include "src/main/player/move.hpp"
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner implements TH05 MAIN player update
#endif

typedef void (near pascal *near PlayerUpdateShotCallback)(void);
extern unsigned int key_det;
extern unsigned char shiftkey;
extern player_input_t player_input_prev;
extern unsigned char player_invincibility_time;
extern unsigned char player_is_hit;
extern unsigned char player_respawn_motion_time;
extern unsigned char miss_time;
extern unsigned char shot_time;
extern SPPoint player_option_pos_cur;
extern SPPoint player_option_pos_prev;
extern PlayerUpdateShotCallback playchar_shot_func;

static const player_input_t PLAYER_UPDATE_MOVEMENT = 0x0F0F;
static const unsigned int PLAYER_UPDATE_INPUT_SHOT = 0x0020;
static const unsigned int PLAYER_UPDATE_INPUT_BOMB = 0x0010;
static const unsigned char PLAYER_UPDATE_SHOT_CYCLE = 18;
static const unsigned char PLAYER_UPDATE_DEATHBOMB_TIME = 40;
static const unsigned char PLAYER_UPDATE_INVINCIBILITY = 192;
static const unsigned char PLAYER_UPDATE_RESPAWN_TIME = 72;

#pragma codeseg PLAYER_UPDATE_AFTER_TEXT main_01
extern "C" void pascal near player_bomb(void);
#pragma codeseg PLAYER_UPDATE_TEXT main_01
void near player_pos_update_and_clamp(void);
void near player_miss_update(void);
void near player_update(void);
#pragma codeseg

typedef char player_update_motion_is_12[(sizeof(PlayfieldMotion) == 12) ? 1 : -1];
typedef char player_update_point_is_4[(sizeof(SPPoint) == 4) ? 1 : -1];
typedef char player_update_shot_callback_is_2[(sizeof(PlayerUpdateShotCallback) == 2) ? 1 : -1];
typedef char player_update_respawn_byte[(sizeof(player_respawn_motion_time) == 1) ? 1 : -1];
#endif
