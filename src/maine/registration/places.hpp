// Full score layout/count and the original two-word row-rendering interface.
#ifndef TH05_MREG_PLACES_HPP
#define TH05_MREG_PLACES_HPP
#include "src/op/hiscore/view.hpp"
#pragma codeseg REG_PLACE_ENTRY_TEXT GROUP_01
void pascal near registration_place_put(int place, int pc);
#pragma codeseg REG_PLACES_TEXT GROUP_01
void pascal near places_put(int pc);
#endif
