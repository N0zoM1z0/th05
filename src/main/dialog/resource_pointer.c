/* dialog_fn: far pointer to the .TX2 file name that dialog_load() patches. */
#pragma option -zCDIALOG_RESOURCE_TEXT -zPmain_01
#ifdef __cplusplus
#error Build this file as C
#endif
#include "src/main/dialog/resource_data.h"

char far *dialog_fn = dialog_resources.script_file;
typedef char dialog_script_pointer_is_far[(sizeof(dialog_fn) == 4) ? 1 : -1];
