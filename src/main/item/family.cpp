// Item initialization, spawning, extends and collection, compiled as one
// translation unit in their original order. item_collect() needs the
// preceding functions: only at its original offset does Borland pad its
// switch jump table with the original zero byte and emit the relocations in
// the original order.
#pragma option -zCITEM_FAMILY_TEXT -zPmain_03
#define TH05_ITEM_FAMILY_CONTEXT
#include "src/main/item/family.hpp"
#pragma codeseg ITEM_FAMILY_TEXT main_03
// Word alignment, as in the TH04 source of these functions
#pragma option -a

#include "src/main/item/initialization.cpp"
#include "src/main/item/spawn.cpp"
#include "src/main/item/extend.cpp"
#include "src/main/item/collect.cpp"
