// Complete canonical Subpixel/item layouts; no storage or constructor substitute.
#ifndef TH05_ITEM_MISS_VELOCITY_DATA_HPP
#define TH05_ITEM_MISS_VELOCITY_DATA_HPP
#include "src/main/item/item.hpp"
enum { ITEM_DROP_SUBPIXELS_PER_PIXEL = 16 };
typedef char item_miss_velocity_cell_is_word[(sizeof(Subpixel) == 2) ? 1 : -1];
typedef char item_miss_velocity_axis_is_10[(sizeof(ITEM_MISS_VELOCITIES[0][0]) == 10) ? 1 : -1];
typedef char item_miss_velocity_field_is_20[(sizeof(ITEM_MISS_VELOCITIES[0]) == 20) ? 1 : -1];
typedef char item_miss_velocity_full_is_60[(sizeof(ITEM_MISS_VELOCITIES) == 60) ? 1 : -1];
#endif
