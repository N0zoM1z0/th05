/* Original near 1-byte PC-98 displayed-page latch for MAINE All Cast. */
#pragma option -zCALLCAST_PAGE_LATCH_TEXT -zPgroup_01
#ifdef __cplusplus
#error The original initialized page latch requires native Borland C
#endif

#include "src/maine/allcast/page_shown.h"

unsigned char near page_shown = 0;
typedef char allcast_displayed_page_is_byte[(sizeof(page_shown) == 1) ? 1 : -1];
