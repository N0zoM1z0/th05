// Reimu's bomb: six star trails that bounce across the screen and spawn
// circles (ReC98 th05/main/player/bombanim.cpp).
#pragma option -zCBOMBANIM_TEXT -zPmain_01
#include "src/main/player/bombanim.hpp"
#pragma codeseg BOMBANIM_TEXT main_01

// Master.lib erase mode plus the inverted four-bit color plane mask.
#include "src/main/player/bomb_body/reimu_stars.inl"
