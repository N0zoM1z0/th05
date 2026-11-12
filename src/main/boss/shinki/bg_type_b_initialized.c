/* Original mutable Shinki background type-B initialization latch. */
#pragma option -zCSHINKI_BG_TYPE_B_START_TEXT -zPmain_01
#ifdef __cplusplus
#error This initialized background DATA public is compiled as C
#endif

#include "src/main/boss/shinki/background_rules.h"

unsigned char near shinki_bg_type_b_initialized = 0;
typedef char shinki_bg_type_b_initialized_width[(sizeof(shinki_bg_type_b_initialized) == 1) ? 1 : -1];
