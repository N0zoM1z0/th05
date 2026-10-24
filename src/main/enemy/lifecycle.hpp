// Natural TH05 enemy lifecycle ABI. Reuse the canonical 64-byte enemy,
// 14-byte BulletTemplate, 12-byte player motion and geometry unchanged.
// Semantic donor: maintained TH04 enemy/stage owners; ReC98 b6ba5b0a supplies
// disassembly/format corroboration only, with original target operands checked.
#ifndef TH05_MAIN_ENEMY_LIFECYCLE_HPP
#define TH05_MAIN_ENEMY_LIFECYCLE_HPP

#pragma codeseg ENEMY_SPAWN_TEXT main_03
extern "C" void pascal near enemies_add(void);
void pascal far std_run(void);
#pragma codeseg ENEMY_UPDATE_TEXT main_03
extern "C" void pascal far enemies_update(void);
#pragma codeseg

#include <dos.h>
#include "src/main/enemy/enemy.hpp"

static const subpixel_t ENEMY_HOMING_NONE = -999 * 16;
static const int PAT_ENEMY_KILL = 4;
static const int ENEMY_KILL_CELS = 8;
static const int RANK_LUNATIC = 3;
#define BST_NORMAL 0

// This is the real 8-byte on-disk TH05 STD spawn record. Word coordinates are
// unaligned within this byte-packed record, as in the original resource.
struct StdEnemySpawnRecord {
    uint8_t script;
    subpixel_t center_x;
    subpixel_t center_y;
    uint8_t item;
    uint8_t subtype;
    uint8_t unused;
};
struct StdFarPointerWords { uint16_t offset; uint16_t segment; };
extern void far *std_ip;
extern void near *std_enemy_scripts[32];
typedef void (far pascal *near EnemyStageVM)(void);
extern EnemyStageVM stage_vm;
extern bool midboss_active;
extern unsigned int stage_frame;
extern unsigned char stage_id;
extern unsigned char dream;
extern SPPoint homing_target;
extern SPPoint shot_hitbox_center;
extern SPPoint shot_hitbox_radius;
extern enemy_t near *enemy_cur;
extern unsigned int enemies_gone;
extern unsigned int enemies_killed;
extern BulletTemplate bullet_template;
typedef void (near pascal *near EnemyBulletTuning)(void);
extern EnemyBulletTuning bullet_template_tune;

// STD advances only the pointer's 16-bit offset, preserving its segment on
// wrap; expressing this actual far-pointer representation is intentional.
#define std_ip_offset (reinterpret_cast<StdFarPointerWords near *>(&std_ip)->offset)
#define current_spawn (*reinterpret_cast<const StdEnemySpawnRecord far *>(std_ip))

#pragma codeseg ENEMY_MAIN01_CONTEXT main_01
int far shots_hittest(void);
extern "C" {
    void pascal far hud_dream_put(void);
    void pascal far nullfunc_far(void);
    void pascal far snd_se_play(int sound);
}
#pragma codeseg MIDBOSS_TEXT main_03
void far midboss_activate_if_stage_frame_is_midboss_start_frame(void);
#pragma codeseg

uint16_t near randring2_next16(void);
uint16_t pascal near randring2_next16_mod(uint16_t divisor);
extern "C" {
    // The complete interpreter consumes global enemy_cur, preserves SI/DI,
    // and returns its observed byte result in AL. Its internal CF-returning
    // movement helper is not misdeclared or called from this C++ owner.
    unsigned char near enemy_script_update(void);
    void near bullets_add_regular(void);
    // Genuine foreign REP MOVSW helper: one near pointer to a 14-byte template,
    // Pascal RET 2. TH05 takes a template reference, not a whole enemy reference.
    void pascal near enemy_bullet_template_push(const BulletTemplate near &source);
}

typedef char lifecycle_std_record_is_8[(sizeof(StdEnemySpawnRecord) == 8) ? 1 : -1];
typedef char lifecycle_std_x_at_1[(offsetof(StdEnemySpawnRecord, center_x) == 1) ? 1 : -1];
typedef char lifecycle_std_y_at_3[(offsetof(StdEnemySpawnRecord, center_y) == 3) ? 1 : -1];
typedef char lifecycle_std_item_at_5[(offsetof(StdEnemySpawnRecord, item) == 5) ? 1 : -1];
typedef char lifecycle_std_subtype_at_6[(offsetof(StdEnemySpawnRecord, subtype) == 6) ? 1 : -1];
typedef char lifecycle_far_words_are_4[(sizeof(StdFarPointerWords) == 4) ? 1 : -1];
typedef char lifecycle_far_segment_at_2[(offsetof(StdFarPointerWords, segment) == 2) ? 1 : -1];
typedef char lifecycle_std_pointer_is_4[(sizeof(std_ip) == 4) ? 1 : -1];
typedef char lifecycle_std_script_offsets_are_64[(sizeof(std_enemy_scripts) == 64) ? 1 : -1];
typedef char lifecycle_enemy_pointer_is_2[(sizeof(enemy_cur) == 2) ? 1 : -1];
typedef char lifecycle_stage_callback_is_4[(sizeof(stage_vm) == 4) ? 1 : -1];
typedef char lifecycle_tuning_callback_is_2[(sizeof(bullet_template_tune) == 2) ? 1 : -1];

#pragma codeseg
#endif
