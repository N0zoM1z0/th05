// Natural ReC98 b6ba5b0a: th04/main/slowdown.cpp; maintained TH04 donor consulted.
#pragma option -zCSLOWDOWN_TEXT -zPmain_01
#include "src/main/runtime/small.hpp"

void near slowdown_frame_delay(void)
{
	while(vsync_Count1 < slowdown_factor) {
	}
	vsync_Count1 = 0;
	slowdown_factor = 1;
}
