// Actual MAINE staff frame-pump providers and shared canonical state.
#ifndef TH05_MAINE_STAFF_FRAME_HPP
#define TH05_MAINE_STAFF_FRAME_HPP

#include <dos.h>
#include "src/maine/staff/lifecycle.hpp"

extern unsigned char staff_text_clear_requested;
extern int staff_bgm_measure;

#pragma codeseg _TEXT
extern "C" void pascal far text_clear(void);
#pragma codeseg SHARED
void pascal far frame_delay(int frames);
int far snd_bgm_measure(void);
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_DRAW_TEXT group_01
#endif
void near staff_scene_render(void);
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_FRAME_TEXT group_01
#endif
void near staff_frame_advance(void);

#endif
