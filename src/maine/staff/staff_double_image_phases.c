/* Initialized staff roll state; see state_publics.h. The original has
 * word-alignment gaps between some of these variables, so each group is
 * its own file. */
#pragma option -zCSTAFF_6_STATE_TEXT -zPgroup_01
#ifdef __cplusplus
#error Compile this file as C
#endif

#include "src/maine/staff/state_publics.h"

int near staff_image_phase_a = 0;
int near staff_image_phase_b = 0;
