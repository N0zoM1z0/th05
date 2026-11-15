// Marks the tiles under all items and item splashes for redrawing.
#ifndef TH05_MAIN_ITEM_INVALIDATE_HPP
#define TH05_MAIN_ITEM_INVALIDATE_HPP
#include "src/main/item/item.hpp"
#include "src/main/item/splash.hpp"

// ZUN bug: TH05 has 40 items, but this still only covers TH04's 32, so the
// tiles under the last 8 items are not redrawn.
static const int ITEM_INVALIDATE_COUNT = 32;
// tiles_invalidate_around() takes two stack words, x at SP+2 and y at SP+4,
// and returns with RET 4. Calling it through this type passes an
// SPPoint by value, which pushes the same two words.
typedef void (near pascal *near ItemPointInvalidator)(const SPPoint center);
typedef char item_point_invalidator_is_near[(sizeof(ItemPointInvalidator) == 2) ? 1 : -1];
void near items_invalidate(void);
#endif
