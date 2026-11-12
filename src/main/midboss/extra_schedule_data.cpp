// Real near callbacks and dash bearings for the Extra midboss fight.
// Original main_03 functions supply the near addresses at link time.
#pragma option -zCMIDBOSSX_SCHED_TEXT -zPmain_03
#include "src/main/midboss/extra_patterns.hpp"
#include "src/main/midboss/extra_attack_rules.hpp"
#pragma codeseg MIDBOSSX_SCHED_TEXT main_03

// The initial held callback waits for dash startup to finish.
MidbossXPattern near midbossx_pattern = midbossx_pattern_wait;

// Active phases select one of two callbacks per pattern set. The final
// sentinel row is physically present but never selected during combat.
MidbossXPattern near midbossx_patterns[3][2] = {
    { midbossx_pattern_spread, midbossx_pattern_random },
    { midbossx_pattern_decelerate, midbossx_pattern_decelerate },
    { 0, 0 }
};

// The eight slot bearings follow the actual masked dash counter, including
// its two adjacent 0x80 headings and the final two sentinel zeros.
const unsigned char near midbossx_dash_angles[8] = {
    MEX_DASH_BEARING_0, MEX_DASH_BEARING_1,
    MEX_DASH_BEARING_2, MEX_DASH_BEARING_3,
    MEX_DASH_BEARING_4, MEX_DASH_BEARING_5,
    MEX_DASH_BEARING_6, MEX_DASH_BEARING_7
};

typedef char extra_pattern_callback_is_word[(sizeof(MidbossXPattern) == 2) ? 1 : -1];
typedef char extra_pattern_rows_are_twelve[(sizeof(midbossx_patterns) == 12) ? 1 : -1];
typedef char extra_dash_angles_are_eight[(sizeof(midbossx_dash_angles) == 8) ? 1 : -1];
