// Complete shared Mai/Yuki state-machine interfaces and original callback ABI.
#ifndef TH05_MAIN_BOSS_MAI_YUKI_UPDATE_HPP
#define TH05_MAIN_BOSS_MAI_YUKI_UPDATE_HPP

#pragma codeseg _TEXT
extern "C" int pascal far super_convert_tiny(int patnum);
#pragma codeseg MY_UPDATE_MAIN01_TEXT main_01
void pascal near mai_yuki_bg_render(void);
void pascal near mai_yuki_survivor_render(void);
void pascal near tiles_render_all(void);
void pascal near overlay_boss_bgm_update_and_render(void);
void far dialog_animate(void);
extern "C" void pascal near cheetos_render(void);
#include "src/main/dialog/file.hpp"
// This owner needs the real title pointer, not the independent HUD surface's
// second to_sp() definition. Preserve its byte element and genuine FAR pointer.
typedef uint8_t shiftjis_t;
extern shiftjis_t far *boss_bgm_title;
#pragma codeseg MAIN_035_TEXT main_03
#include "src/main/boss/mai_yuki/later_patterns.hpp"
#pragma codeseg MAIN_035_TEXT main_03

// Complete canonical explosion enum and one-byte zap union; avoid including
// the unrelated generic owner whose BOSS_W constant conflicts with the frozen
// flight header's same-valued macro. No accepted header is modified.
enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7fff
};
union BulletZapState { bool active; unsigned char frame; };
extern BulletZapState bullet_zap;
extern unsigned char bullet_clear_time;
extern unsigned char player_invincibility_time;
extern unsigned char stage_frame_mod2;
extern unsigned char stage_frame_mod4;
extern int playfield_shake_x;
extern int playfield_shake_y;
extern unsigned int slowdown_factor;
extern unsigned int PaletteTone;
extern bool palette_changed;
extern SPPoint homing_target;
extern nearfunc_t_near bg_render_bombing_func;
extern nearfunc_t_near overlay1;

// Genuine external semantic near CODE-pointer arrays; no entries are supplied.
extern const MaiYukiPattern MAI_PATTERNS_FIRST[4];
extern const MaiYukiPattern MAI_PATTERNS_FINAL[4];
extern const MaiYukiPattern YUKI_PATTERNS_FIRST[4];
extern const MaiYukiPattern YUKI_PATTERNS_LASER[4];
extern const MaiYukiPattern YUKI_PATTERNS_FINAL[4];
extern const char MY_DIALOG_YUKI[];
extern const char MY_DIALOG_MAI[];
extern shiftjis_t MY_BGM_TITLE_YUKI[];
extern shiftjis_t MY_BGM_TITLE_MAI[];

// Original helper at177F0: signed radii/effect words, RET6, damage inAX.
int pascal near yuki_hittest_shots_damage(subpixel_t radius_x,
    subpixel_t radius_y, int effect);
// Original1782C defeat selector returns actual codes0/1/2 inAL: none/Mai/Yuki.
unsigned char near mai_yuki_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void pascal near boss_explode_small(explosion_type_t type);
void near boss_explode_big_circle(void);
void pascal near boss2_explode_small(unsigned int type);
void near boss2_explode_big_circle(void);
void near cheetos_update(void);
void pascal near hud_hp_update_and_render(int hp, int total);
bool pascal near mai_yuki_flystep_random(int frame);
extern "C" {
    void pascal far yuki_update(void);
    void pascal far mai_update(void);
}
void pascal far mai_yuki_update(void);

static const unsigned char MY_PHASE_EXPLODE_SMALL = 253;
static const unsigned char MY_PHASE_EXPLODE_BIG = 254;
static const unsigned char MY_PHASE_SURVIVOR_DIALOG = 255;
static const int MY_TINY_FIRST = 212;
static const int MY_TINY_END = 228;
static const int MY_BOTH_HP_TOTAL = 9000;
static const int MY_SHARED_HP = 4500;
static const int MY_SURVIVOR_HP = 7900;
typedef char my_explosion_enum_is_word[(sizeof(explosion_type_t) == 2) ? 1 : -1];
typedef char my_zap_state_is_byte[(sizeof(BulletZapState) == 1) ? 1 : -1];

#endif
