// Plain C++ version of PlayfieldMotion::update_seg1(). Not built: Borland
// returns `cur` through memory, keeps a BP frame and SI, and reloads the
// result with EAX/SHLD, giving 42 bytes instead of the original 32. The
// built version is motion_seg1_register.cpp. Kept for comparison.
#pragma option -zCMOTION_SEG1_TEXT -zPmain_01 -k-
#include "src/shared/geometry.hpp"

#pragma codeseg MOTION_SEG1_TEXT main_01

PlayfieldPoint pascal near PlayfieldMotion::update_seg1()
{
    prev.x = cur.x;
    cur.x.v += velocity.x.v;
    prev.y = cur.y;
    cur.y.v += velocity.y.v;
    return cur;
}
