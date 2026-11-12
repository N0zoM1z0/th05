/* Original mutable Shinki C/D backdrop gates and EX-Alice rotation flag. */
#pragma option -zCSHINKI_BG_LATE_FLAGS_TEXT -zPmain_01
#ifdef __cplusplus
#error Original three adjacent background DATA flags use a C producer
#endif

#include "src/main/boss/shinki/background_rules.h"

/* C runs only after B's upward-motion preparation; D starts smoke once. */
unsigned char near shinki_bg_type_c_initialized = 0;
unsigned char near shinki_bg_type_d_initialized = 0;
/* This is a separate, later Extra Alice hexagram state in the same DATA run. */
unsigned char near hexagrams_flag = 0;

typedef char bg_c_flag_is_byte[(sizeof(shinki_bg_type_c_initialized) == 1) ? 1 : -1];
typedef char bg_d_flag_is_byte[(sizeof(shinki_bg_type_d_initialized) == 1) ? 1 : -1];
typedef char hexagram_flag_is_byte[(sizeof(hexagrams_flag) == 1) ? 1 : -1];
typedef char three_real_flags_total_three[
    (sizeof(shinki_bg_type_c_initialized) + sizeof(shinki_bg_type_d_initialized) +
     sizeof(hexagrams_flag) == 3) ? 1 : -1];
