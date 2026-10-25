// Natural maintained TH04 stage_runtime_init with actual TH05 state fields.
#pragma option -zCSTAGE_RUNTIME_TEXT -zPmain_01
#include "src/main/runtime/stage_runtime_init.hpp"

void near stage_runtime_init(void)
{
    stage_state_init();
    stage_frame = 0;
    bombing_disabled = false;
    scroll_line = 0;
    tile_ring_scroll_row_prev = 0;
    scroll_line_on_page[0] = 0;
    scroll_line_on_page[1] = 0;
    scroll_subpixel_line.v = 0;
    scroll_row_advance_current = 0;
    scroll_row_advance_previous = 0;
    playfield_shake_x = 0;
    playfield_shake_y = 0;
    player_pos.cur.x.v = 192 * 16;
    player_pos.cur.y.v = 320 * 16;
    player_pos.prev.x.v = 192 * 16;
    player_pos.prev.y.v = 320 * 16;
    player_miss_animation_frame = 0;
    miss_time = 0;
    player_is_hit = false;
    player_invincibility_time = 64;
    stage_point_items_collected = 0;
    shot_time = 0;
    std_update = std_update_frames_then_animate_dialog_and_activate_boss_if_done;
    scroll_active = true;
    shot_level_update();
    randring_fill();
    items_init();
    bomb_reset();
    sparks_init();
    hud_score_put();
    pointnums_init();
    hud_put();
    bg_render_bombing_func = tiles_render_all;
    tiles_invalidate_reset();
}
