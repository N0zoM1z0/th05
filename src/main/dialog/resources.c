/* Dialog file names and the Shift-JIS character buffer, in their original
 * data segment order. The faceset names are mutable templates: the face
 * loader patches the stage or character digit into them. */
#pragma option -zCDIALOG_RESOURCE_TEXT -zPmain_01
#ifdef __cplusplus
#error Build this file as C
#endif
#include "src/main/dialog/resource_data.h"

DialogResourceBank near dialog_resources = {
    0,
    "_DM00.TX2",
    "  ",   /* one fullwidth character, NUL-terminated */
    "st06.bb1",
    "st06.bb2",
    "st06b",
    "DEMO5.REC",
    "op",
    "BsS0.cD2",
    "KaO0.cD2",
    "bb0.cdg",
    "bb1.cdg",
    "bb2.cdg",
    "bb3.cdg",
    "st06_16.bft",
    "bomb3.bft",
    "bomb0.bft"
};
