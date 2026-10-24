// Genuine no-argument callbacks and foreign APIs used by the TH05 frame loop.
#ifndef TH05_GAMEPLAY_LOOP_HPP
#define TH05_GAMEPLAY_LOOP_HPP
#include <dos.h>
#include "src/main/runtime/main.hpp"

// These are the complete canonical stage/setup callback typedefs, unchanged.
typedef void (near pascal *near nearfunc_t_near)(void);
typedef void (far pascal *near func_t_near)(void);
typedef void (near *near RuntimeInputCallback)(void);
typedef bool (near *near RuntimeStdCallback)(void);

extern RuntimeInputCallback input_sense_hook;
extern RuntimeStdCallback std_update;
extern func_t_near stage_vm;
extern nearfunc_t_near bg_render_not_bombing;
extern nearfunc_t_near bg_render_bombing;
extern func_t_near midboss_update;
extern func_t_near boss_update;
extern nearfunc_t_near stage_render;
extern nearfunc_t_near playchar_bomb_func;
extern nearfunc_t_near boss_fg_render;
extern nearfunc_t_near midboss_render;
extern nearfunc_t_near boss_custombullets_render;
extern nearfunc_t_near overlay1;
extern nearfunc_t_near overlay2;

extern unsigned int key_det;
extern bool bombing;
extern bool palette_changed;
extern bool slowdown_caused_by_bullets;
extern bool debug_frame_step_enabled;
extern signed char debug_frame_step;
extern unsigned char player_is_hit;
extern unsigned char page_front;
extern unsigned char page_back;
extern unsigned int slowdown_factor;
extern unsigned long total_slow_frames;
extern unsigned long total_frames;
extern unsigned long frames_unused;
extern unsigned int stage_frame;
extern unsigned char stage_frame_mod16;
extern unsigned char stage_frame_mod8;
extern unsigned char stage_frame_mod4;
extern unsigned char stage_frame_mod2;
extern "C" volatile unsigned int vsync_Count1;

static const unsigned int INPUT_CANCEL = 0x1000;
static const unsigned int INPUT_Q = 0x4000;

#pragma codeseg RUNTIME_MAIN01_TEXT main_01
extern "C" int near pause(void);
extern "C" void pascal far playperf_raise(char delta);
extern "C" void pascal near pointnums_update(void);
void near circles_update(void);
extern "C" void near sparks_update(void);
void near player_update(void);
void near shots_update(void);
void near lasers_update(void);
void pascal near enemies_render(void);
void near shots_render(void);
extern "C" void pascal near player_render(void);
void near grcg_setmode_rmw(void);
void near lasers_render(void);
extern "C" void near sparks_render(void);
extern "C" void pascal near items_render(void);
extern "C" void pascal near pointnums_render(void);
extern "C" void pascal near bullets_render(void);
void near circles_render(void);
void near playfield_shake_update_and_render(void);
void near slowdown_frame_delay(void);
void near scroll_driver(void);
void near score_update_and_render(void);

#pragma codeseg RUNTIME_MAIN03_TEXT main_03
void far bullets_update(void);
extern "C" void pascal far enemies_update(void);
extern "C" void pascal far items_update(void);
void far gather_update(void);
void far gather_render(void);

#pragma codeseg SHARED
void pascal far frame_delay(int frames);
int far input_reset_sense(void);
int far input_sense(void);
extern "C" void far snd_se_update(void);
#pragma codeseg _TEXT
extern "C" void pascal far palette_show(void);
#pragma codeseg

typedef char runtime_near_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
typedef char runtime_far_callback_is_4[(sizeof(func_t_near) == 4) ? 1 : -1];
typedef char runtime_input_callback_is_2[(sizeof(RuntimeInputCallback) == 2) ? 1 : -1];
typedef char runtime_std_callback_is_2[(sizeof(RuntimeStdCallback) == 2) ? 1 : -1];
typedef char runtime_slow_frames_is_4[(sizeof(total_slow_frames) == 4) ? 1 : -1];
typedef char runtime_frames_is_4[(sizeof(total_frames) == 4) ? 1 : -1];
typedef char runtime_unused_frames_is_4[(sizeof(frames_unused) == 4) ? 1 : -1];
#endif
