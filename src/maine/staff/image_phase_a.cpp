// Natural staff image reveal/hold/hide state machine, original DD01..DE79.
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47 th05_maine.asm sub_DCFC
// supplies semantic corroboration; the original decoded image determines ABI.
#pragma option -zCSTAFF_IMAGE_A_TEXT -zPgroup_01
#include "src/maine/staff/image_phase.hpp"
#pragma codeseg STAFF_IMAGE_A_TEXT group_01

#include "src/maine/staff/body/staff_image_update_a.inl"
