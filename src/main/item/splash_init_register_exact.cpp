// Clear all eight complete splash records using the native register memory copy.
#pragma option -zCITEM_SPLASH_INIT_TEXT -zPmain_03
#include <dos.h>
#include "src/main/item/splash.hpp"
#pragma codeseg ITEM_SPLASH_INIT_TEXT main_03
void near item_splashes_init(void)
{
    _CX = sizeof(item_splashes) / sizeof(unsigned int);
    _AX = _DS;
    _ES = _AX;
    asm { xor ax, ax }
    _DI = reinterpret_cast<unsigned int>(&item_splashes[0]);
    asm { rep stosw }
    item_splash_last_id = 0;
}
