// Canonical UTF-8 source; the compiler consumes explicit CP932 staging.
#pragma option -zCVERDICT_PUNCT_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error This initialized semantic DATA producer requires C mode
#endif
#include "src/maine/verdict/format_text_c.h"

const VerdictPunctuation near verdict_punctuation = {
    "点",
    "．",
    "％",
    "．"
};
