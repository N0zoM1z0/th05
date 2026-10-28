// Genuine earlier STD callbacks and the dialog interpreter in source order.
// Foreign graphics/box procedures occupy the intervening native link scopes.
#pragma option -zCDIALOG_OP_TEXT -zPmain_01
#include <string.h>
#include "src/main/dialog/runtime.hpp"
#include "src/main/dialog/boss_transition.hpp"
#pragma codeseg STD_ACTIVATE_TEXT main_01
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

#pragma codeseg DIALOG_OP_TEXT main_01
#pragma option -a2
#include "src/main/dialog/opcode.inl"
