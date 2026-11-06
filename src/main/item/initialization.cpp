// Natural stage initialization from the maintained TH04 item owner.
#ifndef TH05_ITEM_FAMILY_CONTEXT
#pragma option -zCITEM_INIT_TEXT -zPmain_03
#endif
#include "src/main/item/initialization.hpp"
#ifndef TH05_ITEM_FAMILY_CONTEXT
#pragma codeseg ITEM_INIT_TEXT main_03
#endif

void far items_init(void)
{
    item_drop_cycle = (IRand() & 0x0F);
    item_splashes_init();
    items_pull_to_player = false;
    item_dream_score = 0;
}
