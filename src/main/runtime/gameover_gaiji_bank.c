/* Gaiji strings of the game over screen and continue menu.
 * They are not const: Borland puts const and non-const data in a different
 * order, and only this order matches the original. */
#pragma option -zCGAMEOVER_GAIJI_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/main/hud/overlay_data.h"

/* The gaiji question mark, not ASCII '?'. */
enum GameoverGaijiSpecial { GAMEOVER_GAIJI_QUESTION = 8 };

char near gGAMEOVER[10] = {
    HG_BOLD_G, HG_BOLD_A, HG_BOLD_M, HG_BOLD_E,
    HG_BOLD_O, HG_BOLD_V, HG_BOLD_E, HG_BOLD_R, HG_NULL, HG_NULL
};
char near gCONTINUE_QUESTION[11] = {
    HG_BOLD_C, HG_BOLD_O, HG_BOLD_N, HG_BOLD_T, HG_BOLD_I,
    HG_BOLD_N, HG_BOLD_U, HG_BOLD_E, GAMEOVER_GAIJI_QUESTION,
    HG_NULL, HG_NULL
};
char near gYES[4] = {
    HG_BOLD_Y, HG_BOLD_E, HG_BOLD_S, HG_NULL
};
char near gNO[3] = { HG_BOLD_N, HG_BOLD_O, HG_NULL };
char near gCREDIT[7] = {
    HG_BOLD_C, HG_BOLD_R, HG_BOLD_E, HG_BOLD_D,
    HG_BOLD_I, HG_BOLD_T, HG_NULL
};
/* Erases the sliding G of the GAME OVER animation. The second copy,
 * gameover_erase_out, is in score_handoff_names.c. */
char near gameover_erase_in[3] = "  ";

typedef char gameover_six_c_objects_size[
    (sizeof(gGAMEOVER) + sizeof(gCONTINUE_QUESTION) + sizeof(gYES) +
     sizeof(gNO) + sizeof(gCREDIT) + sizeof(gameover_erase_in) == 38) ? 1 : -1];
