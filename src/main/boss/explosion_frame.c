/* Source owner of the one genuine near-DATA big explosion frame counter. */
#pragma option -zCBOSS_EXPLOSION_FRAME_TEXT -zPmain_01
#ifdef __cplusplus
#error Original initialized Boss explosion frame requires native C
#endif
#include "src/main/boss/explosion_frame.h"

int near explosion_big_frame = 0;
typedef char original_big_explosion_frame_word[(sizeof(explosion_big_frame) == 2) ? 1 : -1];
