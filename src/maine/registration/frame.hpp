// Declarations for registration_frame().
#ifndef TH05_MREG_FRAME_HPP
#define TH05_MREG_FRAME_HPP
#include <dos.h>
#include "src/maine/registration/glyphball.hpp"
#pragma codeseg SHARED
#include "src/shared/sound/se.hpp"
void pascal far frame_delay(int frames);
#pragma codeseg REG_GLYPH_UPDATE_TEXT GROUP_01
void near glyphballs_update(void);
#pragma codeseg REG_FRAME_TEXT GROUP_01
void near registration_frame(void);
#pragma codeseg

// Defined in initial_cursor_state.cpp.
extern unsigned char registration_page;
#endif
