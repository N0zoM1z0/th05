// Complete high-level motion candidate; exact acceptance is reviewed separately.
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
