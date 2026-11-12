/* Original mutable Shinki background B/C background alternating-line frame clock. */
#pragma option -zCSHINKI_BG_SPINLINE_CLOCK_TEXT -zPmain_01
#ifdef __cplusplus
#error This initialized background DATA public is compiled as C
#endif

#include "src/main/boss/shinki/background_rules.h"

unsigned int near shinki_bg_spinline_frame = 0;
typedef char shinki_bg_spinline_frame_width[(sizeof(shinki_bg_spinline_frame) == 2) ? 1 : -1];
