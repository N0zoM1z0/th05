// Complete shot/decay/cache layouts and real runtime call interfaces.
#ifndef TH05_SHOT_RUNTIME_HPP
#define TH05_SHOT_RUNTIME_HPP
#pragma codeseg _TEXT
extern "C" int pascal far iatan2(int y, int x);
#pragma codeseg SHOT_UPDATE_TEXT main_01
void near shots_update(void);
#pragma codeseg SHOT_HIT_TEXT main_01
int far shots_hittest(void);
int far shots_hittest_laser(void);
#include "src/main/player/reimu.hpp"
#include "src/main/player/player.hpp"
#include "src/main/hud/resident.hpp"
#include "src/main/bullet/template.hpp"

#if GAME != 5 || BINARY != 'M'
#error This shot runtime belongs to TH05 MAIN
#endif

static const int SHOT_RUNTIME_COUNT = 64;
static const int HITSHOT_COUNT = 24;
static const int HITSHOT_CELS = 4;
static const int HITSHOT_FRAMES_PER_CEL = 3;
static const int HITSHOT_FRAMES = HITSHOT_CELS * HITSHOT_FRAMES_PER_CEL;
static const subpixel_t SHOT_SUBPIXEL_NONE = -999 * 16;

struct shot_alive_t {
    SPPoint pos;
    Shot near *shot;
};
struct hitshot_t {
    unsigned char age;
    unsigned char patnum;
    PlayfieldMotion pos;
};
enum shot_playchar_t {
    SHOT_PLAYCHAR_REIMU = 0, SHOT_PLAYCHAR_MARISA = 1,
    SHOT_PLAYCHAR_MIMA = 2, SHOT_PLAYCHAR_YUUKA = 3,
    SHOT_PLAYCHAR_COUNT = 4, _shot_playchar_t_FORCE_UINT8 = 0xFF
};

extern Shot near shots[SHOT_RUNTIME_COUNT];
extern hitshot_t hitshots[HITSHOT_COUNT];
extern shot_alive_t shots_alive[SHOT_RUNTIME_COUNT];
extern unsigned int shots_alive_count;
extern SPPoint homing_target;
extern SPPoint shot_hitbox_center;
extern SPPoint shot_hitbox_radius;
extern bool shots_hittest_against_boss;
extern unsigned char shot_hit_spark_cycle;
extern bool bombing;
extern unsigned char bomb_frame;
extern unsigned char stage_frame_mod4;
extern unsigned char stage_id;
extern unsigned char rank;
extern unsigned char playchar;
extern unsigned long score_delta;

#pragma codeseg SHOT_RUNTIME_MAIN01_CONTEXT main_01
extern "C" void pascal near hitshot_from(Shot near *shot);
uint16_t near randring1_next16(void);
int pascal far select_for_playchar(int reimu, int marisa, int mima, int yuuka);
#pragma codeseg SHOT_RUNTIME_MAIN03_CONTEXT main_03
void pascal far sparks_add_random(Subpixel center_x, Subpixel center_y,
    subpixel_t radius_min, int count);
extern "C" void far bullets_add_regular_far(void);
#pragma codeseg

typedef char shot_alive_size_is_6[(sizeof(shot_alive_t) == 6) ? 1 : -1];
typedef char shot_alive_pointer_at_4[(offsetof(shot_alive_t, shot) == 4) ? 1 : -1];
typedef char hitshot_size_is_14[(sizeof(hitshot_t) == 14) ? 1 : -1];
typedef char hitshot_motion_at_2[(offsetof(hitshot_t, pos) == 2) ? 1 : -1];
typedef char shot_cache_is_384[(sizeof(shots_alive) == 384) ? 1 : -1];
typedef char hitshot_storage_is_336[(sizeof(hitshots) == 336) ? 1 : -1];
#endif
