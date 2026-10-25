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
#pragma codeseg STAFF_DRAW_TEXT group_01
void near staff_scene_render(void);
#pragma codeseg STAFF_FRAME_TEXT group_01
void near staff_frame_advance(void);

#endif
