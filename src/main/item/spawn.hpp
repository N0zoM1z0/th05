#ifndef TH05_MAIN_ITEM_SPAWN_HPP
#define TH05_MAIN_ITEM_SPAWN_HPP
#include "src/main/item/item.hpp"
#include "src/main/item/splash.hpp"

#pragma codeseg ITEM_SPAWN_TEXT main_03
uint16_t pascal near randring2_next16_mod(uint16_t divisor);
uint16_t pascal near randring2_next16_and(uint16_t mask);
void pascal near items_add(subpixel_t x, subpixel_t y, item_type_t type);
extern "C" void pascal far items_miss_add(void);
#pragma codeseg
#endif
