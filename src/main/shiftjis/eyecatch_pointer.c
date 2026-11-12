/* Real far-DATA reference to the independently owned eyecatch resource name. */
#pragma option -zCEYECATCH_POINTER_TEXT -zPmain_01
#ifdef __cplusplus
#error Eyecatch pointer DATA requires a C compiler producer
#endif
#include "src/shared/abi.hpp"
extern char near EYECATCH_FN[8];

char far *near eyename = EYECATCH_FN;
typedef char eyename_pointer_four[(sizeof(eyename) == 4) ? 1 : -1];
