/* Difficulty names shown at the bottom of the HUD, in the bold gaiji
 * alphabet. Each is padded with empty glyphs to 7 characters plus NUL. */
#pragma option -zCRANK_LABELS_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif
#include "src/main/hud/overlay_data.h"

const unsigned char near hud_rank_labels[5][8] = {
    { HG_BOLD_E, HG_BOLD_A, HG_BOLD_S, HG_BOLD_Y,
      HG_EMPTY, HG_EMPTY, HG_EMPTY, HG_NULL },
    { HG_BOLD_N, HG_BOLD_O, HG_BOLD_R, HG_BOLD_M,
      HG_BOLD_A, HG_BOLD_L, HG_EMPTY, HG_NULL },
    { HG_BOLD_H, HG_BOLD_A, HG_BOLD_R, HG_BOLD_D,
      HG_EMPTY, HG_EMPTY, HG_EMPTY, HG_NULL },
    { HG_BOLD_L, HG_BOLD_U, HG_BOLD_N, HG_BOLD_A,
      HG_BOLD_T, HG_BOLD_I, HG_BOLD_C, HG_NULL },
    { HG_BOLD_E, HG_BOLD_X, HG_BOLD_T, HG_BOLD_R,
      HG_BOLD_A, HG_EMPTY, HG_EMPTY, HG_NULL }
};
typedef char main_rank_label_stride[(sizeof(hud_rank_labels[0]) == 8) ? 1 : -1];
typedef char main_rank_label_size[(sizeof(hud_rank_labels) == 40) ? 1 : -1];
