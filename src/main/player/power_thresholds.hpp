// Complete unsigned-word thresholds indexed by the real shot-level updater.
#ifndef TH05_SHOT_POWER_THRESHOLDS_HPP
#define TH05_SHOT_POWER_THRESHOLDS_HPP
#include "src/shared/abi.hpp"
extern const uint16_t SHOT_LEVEL_TO_POWER[9];
typedef char shot_power_threshold_bank18[(sizeof(SHOT_LEVEL_TO_POWER) == 18) ? 1 : -1];
#endif
