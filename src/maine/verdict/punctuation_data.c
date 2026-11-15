// Score unit, decimal points and percent sign used by the verdict number
// formatters. (UTF-8; converted to Shift-JIS before compiling.)
#pragma option -zCVERDICT_PUNCT_DATA_TEXT -zPgroup_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/maine/verdict/format_text_c.h"

const VerdictPunctuation near verdict_punctuation = {
    "点",
    "．",
    "％",
    "．"
};
