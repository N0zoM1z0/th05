// Natural full-pool initialization; request the compiler's standard inline form.
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
