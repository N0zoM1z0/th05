// Genuine registration-frame callbacks and Borland PC-98 page I/O boundary.
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

// Original initialized byte at DS:1521, shared by the registration screen.
extern unsigned char registration_page;
typedef char reg_frame_page_is_byte[(sizeof(registration_page) == 1) ? 1 : -1];
#endif
