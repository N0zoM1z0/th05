// The score file name, followed by the entry name CONTINUE used by
// hiscore_continue_enter_raw(). That name consists of bold gaiji glyph numbers
// (0xAA = A, ...), written as the halfwidth katakana with the same byte values.
#pragma option -zCSCORE_RES_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif
#include "src/main/score/resource_names_c.h"
MainScoreResourceNames near main_score_resource_names = {
    "GENSOU.SCR",
    "ｬｸｷｽｲｷｾｮ"
};
