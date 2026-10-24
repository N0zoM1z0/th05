// Natural maintained TH04 item invalidation with actual TH05 loop bounds.
#pragma option -zCITEM_INVALIDATE_TEXT -zPmain_01 -k-
#include "src/main/item/invalidate.hpp"
#pragma codeseg ITEM_INVALIDATE_TEXT main_01

void near items_invalidate(void)
{
    *reinterpret_cast<uint32_t near *>(&tile_invalidate_box) =
        (static_cast<uint32_t>(ITEM_H) << 16) | ITEM_W;
    {
        register item_t near *item;
        register int items_left;
        item = items;
        items_left = ITEM_INVALIDATE_COUNT;
        do {
            if(item->flag != F_FREE) {
                reinterpret_cast<ItemPointInvalidator>(
                    &tiles_invalidate_around
                )(item->pos.prev);
            }
            item++;
        } while(--items_left);
    }
    {
        register item_splash_t near *splash;
        register int splashes_left;
        splash = item_splashes;
        splashes_left = ITEM_SPLASH_COUNT;
        do {
            if(splash->flag != F_FREE) {
                tile_invalidate_box.y = tile_invalidate_box.x =
                    (static_cast<unsigned int>(splash->radius_prev.v) >> 3) + 1;
                reinterpret_cast<ItemPointInvalidator>(
                    &tiles_invalidate_around
                )(splash->center);
            }
            splash++;
        } while(--splashes_left);
    }
}
