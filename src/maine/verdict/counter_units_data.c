// Distinct miss/bomb counter-unit objects, each including its own terminator.
#pragma option -zCVERDICT_COUNT_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error This initialized semantic DATA producer requires C mode
#endif
#include "src/maine/verdict/format_text_c.h"

const VerdictCounterUnits near verdict_counter_units = {
    "回",
    "回"
};
