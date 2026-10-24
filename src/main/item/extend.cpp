// Natural TH05 point-item extend check. Original complete helper near1CDAC.
#pragma option -zCITEM_EXTEND_TEXT -zPmain_03
#include "src/main/item/update.hpp"
#pragma codeseg ITEM_EXTEND_TEXT main_03

void near item_extend_check(void)
{
    if((extends_gained * ITEM_EXTEND_POINT_INTERVAL + ITEM_EXTEND_POINT_INTERVAL)
        <= extend_point_items_collected) {
        playperf_raise(4);
        extends_gained++;
        if(lives < ITEM_EXTEND_LIVES_MAX) {
            lives++;
            ITEM_CLEAR_BULLETS();
            hud_lives_put();
            ITEM_SHOW_POPUP(POPUP_ID_EXTEND);
            snd_se_play(7);
        }
    }
}
