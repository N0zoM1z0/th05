/* Far pointers to the two filenames that are changed in place at run time. */
#pragma option -zCSTARTUP_RESOURCE_LINKS_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/main/resources/resource_bank_c.h"
#include "src/main/resources/session_files_c.h"

/* bbname is used by bomb_bg_load__ems_preload_playchar_cdgs(), which writes
 * the player digit into "BB0.CDG". The first pointer has no known name. */
char far *near stage_zero_song_name = main_resource_files.stage_bgm_base;
char far *near bbname = main_session_files.bomb_background;

typedef char startup_resource_link_four[(sizeof(char far *) == 4) ? 1 : -1];
typedef char startup_resource_links_eight[
    (sizeof(stage_zero_song_name) + sizeof(bbname) == 8) ? 1 : -1];
