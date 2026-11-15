/* If set, zapping bullets turns every 4th one into a point item. */
#pragma option -zCBULLET_ZAP_DROP_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif

#include "src/main/boss/late_game_state_publics.h"

unsigned char near bullet_zap_drop_point_items = 0;
typedef char native_bullet_zap_drop_point_items_width[(sizeof(bullet_zap_drop_point_items) == 1) ? 1 : -1];
