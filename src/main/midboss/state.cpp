// Midboss state transitions (ReC98 th05/midboss.cpp -> th04/main/midboss/
// midboss.cpp with GAME = 5).
#pragma option -zCMIDBOSS_TEXT -zPmain_03
#include "src/main/midboss/state.hpp"

void far midboss_reset(void)
{
    midboss_invalidate = nullfunc_near;
    midboss_render = nullfunc_near;
    midboss_update = nullfunc_far;
    midboss.hp = 0;
}

void far midboss_activate_if_stage_frame_is_midboss_start_frame(void)
{
    if(midboss.frames_until == stage_frame) {
        midboss_invalidate = midboss_invalidate_func;
        midboss_render = midboss_render_func;
        midboss_update = midboss_update_func;
        midboss.phase = 0;
        midboss.phase_frame = 0;
        midboss_active = true;
    }
}
