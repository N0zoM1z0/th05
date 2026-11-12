/* Original mutable byte shared by Shinki's two rotating background rings. */
#pragma option -zCSHINKI_LINESET_COUNTER_TEXT -zPmain_01
#ifdef __cplusplus
#error The original Shinki background DATA public is compiled as C
#endif

/* Starts at zero: each radius-224 reset advances this phase counter. */
unsigned char near shinki_bg_linesets_zoomed_out = 0;
typedef char shinki_lineset_counter_is_byte[
    (sizeof(shinki_bg_linesets_zoomed_out) == 1) ? 1 : -1];
