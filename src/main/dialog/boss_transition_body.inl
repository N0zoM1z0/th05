// STD update callbacks for the end of a stage's scrolling part. Included by
// boss_transition.cpp and opcode_full_context.cpp.

// Installed once the boss fight has started: nothing left to do.
bool near std_update_done(void)
{
    return false;
}

// Waits until scrolling has stopped and the back page is page 1, then runs
// the pre-boss dialog and switches all render/update callbacks to the boss.
// Returns true on the frame that happens.
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
