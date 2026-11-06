// One coherent source contribution for initialization, spawning and rewards.
#ifndef TH05_ITEM_FAMILY_HPP
#define TH05_ITEM_FAMILY_HPP
#include "src/main/item/item.hpp"

#pragma codeseg ITEM_FAMILY_TEXT main_03
void far items_init(void);
void pascal near items_add(subpixel_t x, subpixel_t y, item_type_t type);
extern "C" void pascal far items_miss_add(void);
void near item_extend_check(void);
void pascal near item_collect(item_t near *item);
void pascal near item_miss_penalty(item_t near *item);
#pragma codeseg

#include "src/main/item/initialization.hpp"
#include "src/main/item/spawn.hpp"
#include "src/main/item/update.hpp"
#endif
