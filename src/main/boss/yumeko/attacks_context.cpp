// Compiles the sword functions and Yumeko's attacks as one translation unit, in
// their order within the original binary. The aimed-sword and laser/sword
// attacks only get their original relocation order in this context, since the
// preceding code determines where Turbo C++ splits the OMF data records.
// TH05_YUMEKO_COMBINED_CONTEXT skips the -zC/-zP options of each file.
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
