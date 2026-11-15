/* Initialized staff roll state; see state_publics.h. The original has
 * word-alignment gaps between some of these variables, so each group is
 * its own file. */
#pragma option -zCSTAFF_1_STATE_TEXT -zPgroup_01
#ifdef __cplusplus
#error Compile this file as C
#endif

#include "src/maine/staff/state_publics.h"

unsigned char near staff_back_page = 0;
