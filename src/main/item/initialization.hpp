// Full canonical item/splash records and the actual stage initialization APIs.
#ifndef TH05_ITEM_INITIALIZATION_HPP
#define TH05_ITEM_INITIALIZATION_HPP
#include "src/main/item/item.hpp"
#include "src/main/item/splash.hpp"

#pragma codeseg _TEXT
extern "C" int pascal far IRand(void);
#pragma codeseg ITEM_SPLASH_TEXT main_03
void near item_splashes_init(void);
#ifndef TH05_ITEM_FAMILY_CONTEXT
#pragma codeseg ITEM_INIT_TEXT main_03
void far items_init(void);
#endif
#pragma codeseg

extern unsigned int item_dream_score;
#endif
