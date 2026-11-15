// Empty callbacks, assigned to function pointers to disable a stage,
// overlay or midboss hook. -k- avoids a stack frame.
#pragma option -zCNULL_NEAR_TEXT -zPmain_01 -k-
#include "src/shared/abi.hpp"
#pragma codeseg NULL_NEAR_TEXT main_01

extern "C" void pascal near nullfunc_near(void)
{
}

#pragma codeseg NULL_FAR_TEXT main_01
extern "C" void pascal far nullfunc_far(void)
{
}
