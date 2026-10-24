// Survivor pattern scheduling and Mai's nested laser-pattern cycle.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/solo_pattern_tables.hpp"

MaiYukiPattern yuki_solo_pattern_pair1[2] = {
    yuki_solo_ring_sweep,
    yuki_solo_random_spreads
};

MaiYukiPattern yuki_solo_pattern_pair2[2] = {
    yuki_solo_random_rings,
    yuki_solo_snow_fan
};

MaiYukiPattern yuki_solo_pattern_final[5] = {
    yuki_solo_snow_cross,
    yuki_solo_vector_stacks,
    yuki_solo_vector_stacks,
    yuki_solo_vector_stacks,
    yuki_solo_vector_stacks
};

MaiSoloLaserPattern mai_solo_laser_patterns[3] = {
    mai_solo_rotating_fans,
    mai_solo_rotating_rings,
    mai_solo_snow_rings
};

MaiYukiPattern mai_solo_pattern_pair_middle[2] = {
    mai_solo_fans_and_snow,
    mai_solo_turning_fans
};

MaiYukiPattern mai_solo_pattern_pair_final[2] = {
    mai_solo_revenge_snow,
    mai_solo_laser_bounce
};

MaiYukiPattern mai_solo_pattern_pair_first[2] = {
    mai_solo_widening_fans,
    mai_solo_turning_stacks
};

typedef char b4_solo_banks_total_36[(
    sizeof(yuki_solo_pattern_pair1) + sizeof(yuki_solo_pattern_pair2) +
    sizeof(yuki_solo_pattern_final) + sizeof(mai_solo_laser_patterns) +
    sizeof(mai_solo_pattern_pair_middle) + sizeof(mai_solo_pattern_pair_final) +
    sizeof(mai_solo_pattern_pair_first) == 36) ? 1 : -1];
