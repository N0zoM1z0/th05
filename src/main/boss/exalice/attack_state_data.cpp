// Original EX-Alice laser-slot allocator and last-phase horizontal sweep seed.
// Two native near 16-bit states, immediately preceding the paired pattern tables.
#pragma option -zCEXALICE_ATTACK_STATE_TEXT -zPmain_03
#include "src/main/boss/exalice/laser_patterns.hpp"
#include "src/main/boss/exalice/final_patterns.hpp"
#include "src/main/boss/exalice/final_attack_rules.hpp"

int exalice_laser_slot = 0;
subpixel_t exalice_sweep_x = (EXF_FAN_CENTER_X_PX * 16);

typedef char exalice_laser_index_is_word[(sizeof(exalice_laser_slot) == 2) ? 1 : -1];
typedef char exalice_sweep_x_is_word[(sizeof(exalice_sweep_x) == 2) ? 1 : -1];
