// Genuine contiguous Yumeko source context, with one maintained body per function.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#define TH05_YUMEKO_COMBINED_CONTEXT 1
#include "src/main/boss/yumeko/swords_render.cpp"
#include "src/main/boss/yumeko/swords_add.cpp"
#include "src/main/boss/yumeko/swords_update.cpp"
// Restore the ordinary compiler's jump folding for the later attacks.
#pragma option -O
#include "src/main/boss/yumeko/patterns.cpp"
#include "src/main/boss/yumeko/aimed_swords.cpp"
#include "src/main/boss/yumeko/spreads.cpp"
#include "src/main/boss/yumeko/laser_swords.cpp"
