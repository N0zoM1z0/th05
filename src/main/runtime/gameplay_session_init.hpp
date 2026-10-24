// Complete TH05 new-game state and callback ABI. Resident storage is reused;
// function-selector tables remain the actual foreign objects.
#ifndef TH05_SESSION_INIT_HPP
#define TH05_SESSION_INIT_HPP
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This source implements TH05 MAIN new-game initialization
#endif

typedef void (near pascal *near nearfunc_t_near)(void);
typedef void (near pascal *near SessionShotFunction)(void);
typedef void (near pascal *near SessionBulletTuning)(void);
static const int SESSION_PLAYCHAR_COUNT = 4;
static const int SESSION_SHOT_LEVELS = 10;
enum session_playchar_t {
    SESSION_REIMU = 0, SESSION_MARISA = 1,
    SESSION_MIMA = 2, SESSION_YUUKA = 3
};
enum session_rank_t {
    SESSION_EASY = 0, SESSION_NORMAL = 1, SESSION_HARD = 2,
    SESSION_LUNATIC = 3, SESSION_EXTRA = 4
};

extern unsigned char playchar;
extern unsigned char stage_id;
extern unsigned char rank;
extern bool turbo_mode;
extern unsigned char bombs;
extern unsigned char lives;
extern unsigned char power;
extern unsigned char dream;
extern score_lebcd_t score;
extern int playchar_speed_aligned;
extern int playchar_speed_diagonal;
extern nearfunc_t_near playchar_bomb_func;
extern SessionShotFunction near SHOT_FUNCS[SESSION_PLAYCHAR_COUNT][SESSION_SHOT_LEVELS];
extern SessionShotFunction near *near playchar_shot_funcs;
extern SessionBulletTuning bullet_template_tune;
extern unsigned int item_point_score_at_full_dream;
extern unsigned int graze_score;
extern unsigned char playperf_min;
extern unsigned char playperf_max;

#pragma codeseg SESSION_MAIN01_TEXT main_01
extern "C" void pascal near bb_txt_load(void);
void near score_reset(void);
void near hiscore_load(void);
void pascal near bomb_reimu(void);
void pascal near bomb_marisa(void);
void pascal near bomb_mima(void);
void pascal near bomb_yuuka(void);

// Preserve the real first-declaration frame of the existing tuning routines.
#pragma codeseg BULLET_A_TEXT main_03
#include "src/main/bullet/tune.hpp"
#pragma codeseg SESSION_INIT_TEXT main_01
void near gameplay_session_init(void);
#pragma codeseg

typedef char session_shot_function_is_2[(sizeof(SessionShotFunction) == 2) ? 1 : -1];
typedef char session_shot_row_is_20[(sizeof(SHOT_FUNCS[0]) == 20) ? 1 : -1];
typedef char session_shot_table_is_80[(sizeof(SHOT_FUNCS) == 80) ? 1 : -1];
typedef char session_shot_selector_is_2[(sizeof(playchar_shot_funcs) == 2) ? 1 : -1];
typedef char session_bomb_callback_is_2[(sizeof(playchar_bomb_func) == 2) ? 1 : -1];
typedef char session_tuning_callback_is_2[(sizeof(bullet_template_tune) == 2) ? 1 : -1];
typedef char session_speed_is_2[(sizeof(playchar_speed_aligned) == 2) ? 1 : -1];
typedef char session_dream_score_is_2[(sizeof(item_point_score_at_full_dream) == 2) ? 1 : -1];
typedef char session_graze_score_is_2[(sizeof(graze_score) == 2) ? 1 : -1];
#endif
