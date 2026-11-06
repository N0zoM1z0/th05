/* Initial dialog script pointer, with the real four-byte large-model ABI. */
#pragma option -zCDIALOG_RESOURCE_TEXT -zPmain_01
#ifdef __cplusplus
#error This initialized pointer owner requires C mode
#endif
#include "src/main/dialog/resource_data.h"

char far *dialog_fn = dialog_resources.script_file;
typedef char dialog_script_pointer_is_far[(sizeof(dialog_fn) == 4) ? 1 : -1];
