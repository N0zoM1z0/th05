// Complete player-miss state and truthful foreign calling interfaces.
#ifndef TH05_PLAYER_MISS_HPP
#define TH05_PLAYER_MISS_HPP
#include "src/main/player/player.hpp"
#include "src/main/boss/movement.hpp"
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This source implements TH05 MAIN player-miss behavior
#endif

// Complete canonical quit enum, identical to runtime/main.hpp. Avoid importing
// that startup owner's unrelated function-declaration segment contexts.
enum quit_t { Q_KEEP_RUNNING = 0, Q_QUIT_TO_OP = 1, Q_NEXT_STAGE = 2 };
extern quit_t quit;
extern unsigned char miss_time;
extern unsigned int miss_explosion_radius;
extern unsigned char miss_explosion_angle;
extern unsigned char power;
extern int power_overflow;
extern unsigned char dream;
extern unsigned char playperf;
extern unsigned char lives;
extern unsigned char bombs;
extern unsigned char bullet_clear_time;
extern unsigned char stage_frame_mod2;
extern unsigned int PaletteTone;
extern bool palette_changed;

static const unsigned char PLAYER_MISS_ANIMATION_FRAMES = 32;
static const unsigned char PLAYER_MISS_FLASH_FRAME_COUNT = 4;
static const unsigned int PLAYER_MISS_RADIUS_STEP = 7 * 16;
static const unsigned char PLAYER_MISS_ANGLE_STEP = 8;
static const unsigned char PLAYER_MISS_BOSS_HP_FILL = 0;

#pragma codeseg PLAYER_MISS_MAIN03_TEXT main_03
extern "C" void pascal far items_miss_add(void);
#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int effect);
#pragma codeseg PLAYER_MISS_AFTER_TEXT main_01
extern "C" {
    void pascal far shot_level_update(void);
    void pascal far playperf_lower(char delta);
    void pascal far hud_dream_put(void);
}
void far hud_lives_put(void);
void far hud_bombs_put(void);
unsigned char near gameover_run(void);
#pragma samecodeseg shot_level_update
#pragma samecodeseg playperf_lower
#pragma samecodeseg hud_dream_put
#pragma samecodeseg hud_lives_put
#pragma samecodeseg hud_bombs_put
#pragma codeseg PLAYER_MISS_TEXT main_01
void near player_miss_update(void);
#pragma codeseg

typedef char player_miss_motion_is_12[(sizeof(PlayfieldMotion) == 12) ? 1 : -1];
typedef char player_miss_boss_is_24[(sizeof(boss_stuff_t) == 24) ? 1 : -1];
typedef char player_miss_quit_is_1[(sizeof(quit_t) == 1) ? 1 : -1];
typedef char player_miss_resident_count_at_27[(offsetof(resident_t, miss_count) == 27) ? 1 : -1];
#endif
