/* Two separately writable MAINE child filenames used by end_game/end_extra. */
#pragma option -zCEND_BINARY_NAMES_TEXT -zPmain_01
#ifdef __cplusplus
#error End-sequence filenames require the native C DATA initializer
#endif

char game_end_binary_name[] = "maine";
char extra_end_binary_name[] = "maine";

typedef char game_end_name_is_six[(sizeof(game_end_binary_name) == 6) ? 1 : -1];
typedef char extra_end_name_is_six[(sizeof(extra_end_binary_name) == 6) ? 1 : -1];
typedef char end_binary_names_are_twelve[
    (sizeof(game_end_binary_name) + sizeof(extra_end_binary_name) == 12) ? 1 : -1];
