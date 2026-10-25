// Semantic power breakpoints; the updater scans all nine unsigned words.
#pragma option -zCSHOT_LEVEL_DATA_TEXT -zPmain_01
#include "src/main/player/power_thresholds.hpp"

const uint16_t SHOT_LEVEL_TO_POWER[9] = {
    6, 12, 16, 24, 32, 48, 72, 96, 128
};
