// Canonical MAIN callback and scroll interfaces for dialog-to-boss activation.
#ifndef TH05_DIALOG_BOSS_TRANSITION_HPP
#define TH05_DIALOG_BOSS_TRANSITION_HPP
#include "src/shared/geometry.hpp"
#include "src/main/hud/resident.hpp"
#if GAME != 5 || BINARY != 'M'
#error This owner belongs to TH05 MAIN
#endif

typedef bool (near *near RuntimeStdCallback)(void);
typedef void (near pascal *near nearfunc_t_near)(void);
typedef void (far pascal *near func_t_near)(void);

extern SubpixelLength8 scroll_speed;
extern unsigned char page_back;
extern unsigned int total_std_frames;
extern RuntimeStdCallback std_update;
extern nearfunc_t_near bg_render_not_bombing;
extern nearfunc_t_near boss_bg_render_func;
extern func_t_near boss_update;
extern func_t_near boss_update_func;
extern nearfunc_t_near boss_fg_render;
extern nearfunc_t_near boss_fg_render_func;
extern nearfunc_t_near overlay1;

// These are all real AE1-frame functions. Preserve each first declaration's
// near callback context and the genuine far cdecl animation interface.
#pragma codeseg STD_ACTIVATE_TEXT main_01
bool near std_update_done(void);
bool near std_update_frames_then_animate_dialog_and_activate_boss_if_done(void);
void far dialog_animate(void);
#pragma samecodeseg dialog_animate
void pascal near overlay_boss_bgm_update_and_render(void);
#pragma codeseg

typedef char std_activate_near_callback_is_2[(sizeof(RuntimeStdCallback) == 2) ? 1 : -1];
typedef char std_activate_render_callback_is_2[(sizeof(nearfunc_t_near) == 2) ? 1 : -1];
typedef char std_activate_update_callback_is_4[(sizeof(func_t_near) == 4) ? 1 : -1];
typedef char std_activate_scroll_speed_is_1[(sizeof(scroll_speed) == 1) ? 1 : -1];
#endif
