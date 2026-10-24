// Semantic initialized pointer data, not a table of target offsets or bytes.
// Actual original order is character-major, then power/shot level0 through9.
#pragma option -zCSHOT_TABLE_CONTEXT -zPmain_01
#include "src/main/player/shot_tables.hpp"

SessionShotFunction near SHOT_FUNCS[SESSION_PLAYCHAR_COUNT][SESSION_SHOT_LEVELS] = {
    {
        shot_l0, shot_l1,
        shot_reimu_l2, shot_reimu_l3, shot_reimu_l4, shot_reimu_l5,
        shot_reimu_l6, shot_reimu_l7, shot_reimu_l8, shot_reimu_l9
    },
    {
        shot_l0, shot_l1,
        shot_marisa_l2, shot_marisa_l3, shot_marisa_l4, shot_marisa_l5,
        shot_marisa_l6, shot_marisa_l7, shot_marisa_l8, shot_marisa_l9
    },
    {
        shot_l0, shot_l1,
        shot_mima_l2, shot_mima_l3, shot_mima_l4, shot_mima_l5,
        shot_mima_l6, shot_mima_l7, shot_mima_l8, shot_mima_l9
    },
    {
        shot_l0, shot_l1,
        shot_yuuka_l2, shot_yuuka_l3, shot_yuuka_l4, shot_yuuka_l5,
        shot_yuuka_l6, shot_yuuka_l7, shot_yuuka_l8, shot_yuuka_l9
    }
};
