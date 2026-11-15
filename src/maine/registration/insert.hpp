// Declarations for score_insert().
#ifndef TH05_MREG_INSERT_HPP
#define TH05_MREG_INSERT_HPP
#include "src/op/hiscore/view.hpp"
extern uint8_t entered_place;
static const unsigned char REG_INSERT_EXTRA = 0xFD; // ES_EXTRA
static const unsigned char REG_INSERT_ALL = 0xE9; // "ALL" stage gaiji
#pragma codeseg REG_VALUES_TEXT GROUP_01
void near score_insert(void);
#endif
