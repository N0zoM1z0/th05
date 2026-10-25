// Actual TH05 stage/session entry and foreign resource/runtime interfaces.
#ifndef TH05_STAGE_SESSION_HPP
#define TH05_STAGE_SESSION_HPP
#include <dos.h>
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner implements TH05 MAIN stage-session initialization
#endif

typedef void (near pascal *near nearfunc_t_near)(void);
typedef void (near *near StageInputCallback)(void);
extern int load_playchar_resources;
extern bool debug_frame_step_enabled;
extern unsigned char stage_id;
extern unsigned char playchar;
extern unsigned char power;
extern StageInputCallback input_sense_hook;
extern nearfunc_t_near bg_render_not_bombing;
extern nearfunc_t_near bg_render_bombing_func;
extern nearfunc_t_near overlay1;
extern nearfunc_t_near overlay2;
extern unsigned int pellet_bottom_col;
extern unsigned char page_back;
extern unsigned char page_front;
extern char far *stage_bgm_name;
extern unsigned int PaletteTone;
extern long random_seed;
extern "C" volatile unsigned int vsync_Count2;

// These are real existing filename objects, not owned payload or pointer arrays.
extern const char near SESSION_EYE_RGB[];
extern const char near SESSION_REIMU_BFT[];
extern const char near SESSION_MARI_BFT[];
extern const char near SESSION_MIMA_BFT[];
extern const char near SESSION_YUKA_BFT[];
extern const char near SESSION_MIKOD_BFT[];
extern const char near SESSION_MIKO32_BFT[];
extern const char near SESSION_REIMU16_BFT[];
extern const char near SESSION_MARI16_BFT[];
extern const char near SESSION_MIMA16_BFT[];
extern const char near SESSION_YUKA16_BFT[];
extern const char near SESSION_MIKO16_BFT[];
extern const char near SESSION_BOMB_YUUKA_BFT[];
extern const char near SESSION_BOMB_BFT[];
extern const char near SESSION_BSS0_CD2[];
extern const char near SESSION_ST00_BFT[];
extern const char near SESSION_ST00_MPN[];
extern const char near SESSION_BSS1_CD2[];
extern const char near SESSION_ST01_BFT[];
extern const char near SESSION_ST01_MPN[];
extern const char near SESSION_BSS2_CD2[];
extern const char near SESSION_ST02_BFT[];
extern const char near SESSION_ST02_MPN[];
extern const char near SESSION_BSS3_CD2[];
extern const char near SESSION_ST03_BFT[];
extern const char near SESSION_ST03_MPN[];
extern const char near SESSION_BSS4_CD2[];
extern const char near SESSION_ST04_BFT[];
extern const char near SESSION_ST04_MPN[];
// Stage6 really references distinct copies of the stage5 filenames.
extern const char near SESSION_BSS4_CD2_REPEAT[];
extern const char near SESSION_ST04_BFT_REPEAT[];
extern const char near SESSION_BSS6_CD2[];
extern const char near SESSION_ST06_BFT[];
extern const char near SESSION_ST06_MPN[];

#pragma codeseg _TEXT
extern "C" {
    void pascal far text_fillca(unsigned int ch, unsigned int attr);
    int pascal far palette_entry_rgb(const char far *filename);
    void pascal far palette_show(void);
    void pascal far palette_black_out(unsigned int speed);
    int pascal far super_entry_bfnt(const char far *filename);
    int pascal far super_convert_tiny(int pattern);
}
#pragma codeseg SHARED
enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
extern "C" {
    void pascal far snd_load(const char far *filename, snd_load_func_t operation);
    int pascal far snd_kaja_interrupt(int ax);
}
#pragma codeseg STAGE_SESSION_MAIN03_CONTEXT main_03
void far midboss_reset(void);

// These real interfaces are all in frameAE1, including the three far-return
// services whose original calls use a same-frame far transfer.
#pragma codeseg STAGE_SESSION_TEXT main_01
void near stage_session_init(void);
void near gameplay_session_init(void);
void near demo_load(void);
void near DemoPlay(void);
extern "C" void pascal near nullfunc_near(void);
void near clear_blue_vram_pages(void);
void near overlay_wipe(void);
void near overlay_black(void);
void near stage_runtime_init(void);
void far hud_put(void);
void near eyecatch_animate(void);
extern "C" void pascal near bb_cheeto_load(void);
void near bomb_bg_load__ems_preload_playchar_cdgs(void);
extern "C" void pascal near bb_playchar_load(void);
void far tiles_activate(void);
void far shot_level_update(void);
void pascal near ems_preload_boss_faceset(const char far *filename);
void pascal near stage1_setup(void);
void pascal near stage2_setup(void);
void pascal near stage3_setup(void);
void pascal near stage4_setup(void);
void pascal near stage5_setup(void);
void pascal near stage6_setup(void);
void pascal near stagex_setup(void);
void pascal near shinki_bg_render(void);
extern "C" int pascal near mpn_load(const char far *filename);
void near map_load(void);
void near std_load(void);
void near dialog_load(void);
extern "C" void pascal near tiles_fill_initial(void);
void pascal near tiles_render_all(void);
void pascal near overlay_stage_enter_update_and_render(void);
#pragma codeseg

typedef char stage_session_resident_is_full[(sizeof(resident_t) == 128) ? 1 : -1];
typedef char stage_session_input_callback_is_2[(sizeof(StageInputCallback) == 2) ? 1 : -1];
typedef char stage_session_overlay_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
typedef char stage_session_song_pointer_is_4[(sizeof(stage_bgm_name) == 4) ? 1 : -1];
#endif
