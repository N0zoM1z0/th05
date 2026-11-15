/* Far pointer to EYECATCH_FN (eyecatch_filename.c), used by the EMS
 * eyecatch preloading code. */
#pragma option -zCEYECATCH_POINTER_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C
#endif
#include "src/shared/abi.hpp"
extern char near EYECATCH_FN[8];

char far *near eyename = EYECATCH_FN;
typedef char eyename_pointer_four[(sizeof(eyename) == 4) ? 1 : -1];
