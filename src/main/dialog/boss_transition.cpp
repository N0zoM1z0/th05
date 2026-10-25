// Semantic dialog-to-boss callbacks, corroborated by ReC98 dialog/shared.cpp.
#pragma option -zCSTD_ACTIVATE_TEXT -zPmain_01
#include "src/main/dialog/boss_transition.hpp"

bool near std_update_done(void)
{
    return false;
}

bool near std_update_frames_then_animate_dialog_and_activate_boss_if_done(void)
{
    if((scroll_speed == 0) && (page_back == 1)) {
        dialog_animate();
        std_update = std_update_done;
        bg_render_not_bombing = boss_bg_render_func;
        boss_update = boss_update_func;
        boss_fg_render = boss_fg_render_func;
        overlay1 = overlay_boss_bgm_update_and_render;
        return true;
    }
    total_std_frames++;
    return false;
}
