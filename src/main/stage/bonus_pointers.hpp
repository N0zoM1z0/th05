// Actual two-byte near UI pointers consumed by the stage-bonus functions.
#ifndef TH05_STAGE_BONUS_POINTERS_HPP
#define TH05_STAGE_BONUS_POINTERS_HPP
#include "src/main/stage/bonus_strings.hpp"
extern const char near *const STAGE_CLEAR_BONUS_DESC[11];
extern const char near *BONUS_STAGE;
extern const char near *BONUS_DREAM;
extern const char near *GRAZEX50;
extern const char near *POINT_ITEMS;
extern const char near *BONUS_NOMISS;
extern const char near *BONUS_NOBOMB;
extern const char near *BONUS_TOTAL;
extern const char near *ALL_CLEAR;
extern const char near *PLAYER_REM;
extern const char near *POINT_TOTAL;
typedef char bonus_near_description_bank22[(sizeof(STAGE_CLEAR_BONUS_DESC) == 22) ? 1 : -1];
#endif
