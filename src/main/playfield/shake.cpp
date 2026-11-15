// Playfield shake: shifts the active VRAM page by a few pixels with the EGC
// and schedules a tile redraw to undo it. Same code as ReC98's
// th04/main/playfld.cpp built with GAME=5.
#pragma option -zCPLAYFLD_TEXT -zPmain_01
#include "src/main/playfield/shake.hpp"

inline void shift(
    egc_shift_func_t *func,
    vram_y_t top,
    vram_y_t bottom,
    bool negate,
    const pixel_t &dots
) {
    func(PLAYFIELD_LEFT, top, (PLAYFIELD_RIGHT - 1), bottom,
        (negate) ? -dots : dots);
    // Only the active VRAM page was shifted, but with page flipping both pages
    // need a redraw to undo it, so always redraw the next two frames.
    playfield_shake_redraw_time = PAGE_COUNT;
}

inline void shift_x(egc_shift_func_t *func, bool negate)
{
    shift(func, 0, (RES_Y - 1), negate, playfield_shake_x);
}

inline void shift_y(egc_shift_func_t *func, bool negate)
{
    // Micro-optimization: during boss fights (no scrolling), only the
    // playfield area needs to move.
    if(scroll_line == 0) {
        shift(func, PLAYFIELD_TOP, (PLAYFIELD_BOTTOM - 1), negate,
            playfield_shake_y);
        return;
    }
    shift(func, 0, (RES_Y - 1), negate, playfield_shake_y);
}

void near playfield_shake_update_and_render(void)
{
    if(playfield_shake_anim_time) {
        playfield_shake_x = (stage_frame_mod2 == 0) ? -2 : 2;
        playfield_shake_y = (stage_frame_mod4 <= 1) ? -2 : 2;
        playfield_shake_anim_time--;
    }

    if(playfield_shake_x < 0) {
        // ZUN quirk: TH05 shifts left twice, so left shakes move twice as
        // far as right ones.
        egc_shift_left(PLAYFIELD_LEFT, 0, (PLAYFIELD_RIGHT - 1), (RES_Y - 1),
            -playfield_shake_x);
        shift_x(egc_shift_left, true);
    } else if(playfield_shake_x > 0) {
        shift_x(egc_shift_right, false);
    }
    if(playfield_shake_y < 0) {
        shift_y(egc_shift_up, true);
    } else if(playfield_shake_y > 0) {
        shift_y(egc_shift_down, false);
    }

    if(playfield_shake_redraw_time) {
        playfield_shake_redraw_time--;
        tiles_invalidate_all();
        playfield_shake_x = 0;
        playfield_shake_y = 0;
    }
}
