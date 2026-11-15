/* Frame counter of the big boss explosion. ZUN defined it in C, so it */
/* has an unmangled C symbol. */
#pragma option -zCBOSS_EXPLOSION_FRAME_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C, not C++
#endif
#include "src/main/boss/explosion_frame.h"

int near explosion_big_frame = 0;
typedef char big_explosion_frame_is_a_word[(sizeof(explosion_big_frame) == 2) ? 1 : -1];
