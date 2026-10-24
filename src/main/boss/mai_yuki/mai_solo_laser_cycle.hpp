// Actual 461-byte Mai laser cycle, distinct from the270-byte bounce attack.
#ifndef TH05_MAI_SOLO_LASER_CYCLE_HPP
#define TH05_MAI_SOLO_LASER_CYCLE_HPP
#include "src/main/boss/mai_yuki/mai_solo_advanced.hpp"
#pragma codeseg MAIN_035_TEXT main_03
typedef void (near *near MaiSoloLaserPattern)(void);
extern int mai_solo_laser_count;
extern int mai_solo_laser_speed;
extern int mai_solo_laser_fraction;
extern MaiSoloLaserPattern mai_solo_laser_pattern;
extern MaiSoloLaserPattern mai_solo_laser_patterns[3];
bool near mai_solo_laser_cycle(void);
#pragma codeseg
typedef char mai_cycle_laser_is_24[(sizeof(Laser) == 24) ? 1 : -1];
typedef char mai_cycle_callback_is_2[(sizeof(MaiSoloLaserPattern) == 2) ? 1 : -1];
typedef char mai_cycle_callback_bank_is_6[(sizeof(mai_solo_laser_patterns) == 6) ? 1 : -1];
#endif
