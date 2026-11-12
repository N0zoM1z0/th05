/* Distinct writable text and child executable objects for the score handoff. */
#pragma option -zCSCORE_HANDOFF_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Score and child program data must have a native C producer
#endif

/* The two Game Over erase fields are physically independent allocations. */
char near gameover_erase_out[3] = "  ";
/* The original third MAINE child filename, referenced by GameExecl(). */
char near maine_binary[6] = "maine";

typedef char score_handoff_blank_is_three[
    (sizeof(gameover_erase_out) == 3) ? 1 : -1];
typedef char score_handoff_name_is_six[
    (sizeof(maine_binary) == 6) ? 1 : -1];
typedef char score_handoff_combined_nine[
    (sizeof(gameover_erase_out) + sizeof(maine_binary) == 9) ? 1 : -1];
