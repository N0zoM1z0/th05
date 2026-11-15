// Standalone build of reg_name_put() and registration_place_put(), which are
// adjacent in the original (see full_context.cpp).
#pragma option -zCREG_DISPLAY_TEXT -zPGROUP_01
#include "src/maine/registration/display.hpp"
#pragma codeseg REG_DISPLAY_TEXT GROUP_01
#pragma option -a
#include "src/maine/registration/name.inl"
#include "src/maine/registration/place.inl"
