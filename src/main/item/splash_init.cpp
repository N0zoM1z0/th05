// memset() version of item_splashes_init(). Not built: Borland's intrinsic
// memset() gives 24 bytes instead of the original 26.
// splash_init_register_exact.cpp has the version that matches.
#pragma option -zCITEM_SPLASH_INIT_TEXT -zPmain_03
#include <mem.h>
#include "src/main/item/splash.hpp"
#pragma intrinsic memset
#pragma codeseg ITEM_SPLASH_INIT_TEXT main_03

void near item_splashes_init(void)
{
    memset(item_splashes, 0, sizeof(item_splashes));
    item_splash_last_id = 0;
}
