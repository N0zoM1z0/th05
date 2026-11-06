// Complete consecutive initialization, spawning, extend and reward family.
#pragma option -zCITEM_FAMILY_TEXT -zPmain_03
#define TH05_ITEM_FAMILY_CONTEXT
#include "src/main/item/family.hpp"
#pragma codeseg ITEM_FAMILY_TEXT main_03
// Restore the maintained TH04 owner's alignment context after complete types.
#pragma option -a

#include "src/main/item/initialization.cpp"
#include "src/main/item/spawn.cpp"
#include "src/main/item/extend.cpp"
#include "src/main/item/collect.cpp"
