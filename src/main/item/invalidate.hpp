#ifndef TH05_MAIN_ITEM_INVALIDATE_HPP
#define TH05_MAIN_ITEM_INVALIDATE_HPP
#include "src/main/item/item.hpp"
#include "src/main/item/splash.hpp"

// Original TH05 invalidation retains TH04's32-slot loop despite a40-slot pool.
static const int ITEM_INVALIDATE_COUNT = 32;
// Genuine legacy ABI view: existing near Pascal entry consumes four bytes,
// x at SP+2 and y at SP+4, RET4. Aggregate copying preserves that real frame.
// This explicit DOS ABI adaptation does not assert ISO-portable function types.
typedef void (near pascal *near ItemPointInvalidator)(const SPPoint center);
typedef char item_point_invalidator_is_near[(sizeof(ItemPointInvalidator) == 2) ? 1 : -1];
void near items_invalidate(void);
#endif
