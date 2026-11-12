/* Real writable MAINE score, timer and slow-mode warning resources. */
#pragma option -zCSCORE_RESOURCE_TEXT -zPgroup_01
#ifdef __cplusplus
#error Native score DATA uses a C compiler producer
#endif

/* All four original SCORE file opens keep independent mutable names. */
char SCOREDAT_FN[] = "GENSOU.SCR";
char SCOREDAT_FN_0[] = "GENSOU.SCR";
char SCOREDAT_FN_1[] = "GENSOU.SCR";
char SCOREDAT_FN_2[] = "GENSOU.SCR";

char hi_score_picture_name[] = "hi01.pi";
char score_digits_font_name[] = "scnum.bft";
char score_timer_font_0_name[] = "sctm0.bft";
char score_timer_font_1_name[] = "sctm1.bft";

/* The two independent warning objects are deliberately writable. */
char slow_mode_score_warning[] =
    "スローモードでのプレイでは、スコアは記録されません";
char slow_mode_score_warning_repeat[] =
    "スローモードでのプレイでは、スコアは記録されません";

char score_name_field_label[] = "name";

typedef char score_file_size_11[(sizeof(SCOREDAT_FN) == 11) ? 1 : -1];
typedef char score_picture_size_8[(sizeof(hi_score_picture_name) == 8) ? 1 : -1];
typedef char score_font_size_10[(sizeof(score_digits_font_name) == 10) ? 1 : -1];
typedef char score_warning_size_51[(sizeof(slow_mode_score_warning) == 51) ? 1 : -1];
typedef char score_label_size_5[(sizeof(score_name_field_label) == 5) ? 1 : -1];
typedef char all_score_resources_size_189[(
    sizeof(SCOREDAT_FN) + sizeof(SCOREDAT_FN_0) +
    sizeof(SCOREDAT_FN_1) + sizeof(SCOREDAT_FN_2) +
    sizeof(hi_score_picture_name) + sizeof(score_digits_font_name) +
    sizeof(score_timer_font_0_name) + sizeof(score_timer_font_1_name) +
    sizeof(slow_mode_score_warning) +
    sizeof(slow_mode_score_warning_repeat) +
    sizeof(score_name_field_label) == 189
) ? 1 : -1];
