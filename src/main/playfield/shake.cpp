// Natural playfield shake adapted from nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/playfld.cpp ->
// th04/main/playfld.cpp, retaining the GAME=5 clipping and double-left behavior.
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
    // Both page-flipped buffers need a redraw to remove the previous shift.
    playfield_shake_redraw_time = PAGE_COUNT;
}

inline void shift_x(egc_shift_func_t *func, bool negate)
{
    shift(func, 0, (RES_Y - 1), negate, playfield_shake_x);
}

inline void shift_y(egc_shift_func_t *func, bool negate)
{
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
        // Preserve TH05's original second left shift, not just its animation.
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
