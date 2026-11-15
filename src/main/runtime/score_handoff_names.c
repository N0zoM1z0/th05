/* The second erase string of the GAME OVER animation, and the MAINE filename
 * that gameover_run() passes to GameExecl() for the score screen. */
#pragma option -zCSCORE_HANDOFF_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C
#endif

/* ZUN bloat: an identical copy of gameover_erase_in. */
char near gameover_erase_out[3] = "  ";
/* ZUN bloat: the third copy of this filename (see end_binary_names.c). */
char near maine_binary[6] = "maine";

typedef char score_handoff_blank_is_three[
    (sizeof(gameover_erase_out) == 3) ? 1 : -1];
typedef char score_handoff_name_is_six[
    (sizeof(maine_binary) == 6) ? 1 : -1];
typedef char score_handoff_combined_nine[
    (sizeof(gameover_erase_out) + sizeof(maine_binary) == 9) ? 1 : -1];
