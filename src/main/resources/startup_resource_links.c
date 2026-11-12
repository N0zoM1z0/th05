/* Two original far file pointers into independently accepted filename banks. */
#pragma option -zCSTARTUP_RESOURCE_LINKS_TEXT -zPmain_01
#ifdef __cplusplus
#error Startup resource pointer DATA requires a C compiler producer
#endif
#include "src/main/resources/resource_bank_c.h"
#include "src/main/resources/session_files_c.h"

/* The original second pointer is the public bbname consumed by the
 * existing PC-98 EMS path. Preserve its independently addressable C symbol. */
const char far *near stage_zero_song_name = main_resource_files.stage_bgm_base;
const char far *near bbname = main_session_files.bomb_background;

typedef char startup_resource_link_four[(sizeof(const char far *) == 4) ? 1 : -1];
typedef char startup_resource_links_eight[
    (sizeof(stage_zero_song_name) + sizeof(bbname) == 8) ? 1 : -1];
