// pointnums_init(), built on its own from init.inl. The alignment NOP after it
// in the original is not part of this unit.
#pragma option -zCPOINTNUM_LIFE_TEXT -zPmain_01 -k-
#include "src/main/pointnum/lifecycle.hpp"
#pragma codeseg POINTNUM_LIFE_TEXT main_01
#include "src/main/pointnum/init.inl"
