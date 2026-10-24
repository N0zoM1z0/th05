// Scalar playfield-shake ABI from ReC98 th04/main/playfld.hpp, GAME=5.
#ifndef TH05_MAIN_PLAYFIELD_SHAKE_HPP
#define TH05_MAIN_PLAYFIELD_SHAKE_HPP

#include "src/shared/abi.hpp"

typedef uint8_t bool;
#define false 0
#define true 1
typedef int screen_x_t;
typedef int vram_y_t;

static const screen_x_t PLAYFIELD_LEFT = 32;
static const screen_x_t PLAYFIELD_RIGHT = 416;
static const vram_y_t PLAYFIELD_TOP = 16;
static const vram_y_t PLAYFIELD_BOTTOM = 384;
static const pixel_t RES_Y = 400;
static const int PAGE_COUNT = 2;

extern pixel_t playfield_shake_x;
extern pixel_t playfield_shake_y;
extern int playfield_shake_anim_time;
extern char playfield_shake_redraw_time;
extern vram_y_t scroll_line;
extern uint8_t stage_frame_mod2;
extern uint8_t stage_frame_mod4;

typedef void pascal far egc_shift_func_t(
    screen_x_t x1, vram_y_t y1, screen_x_t x2, vram_y_t y2, pixel_t dots
);
extern "C" {
    void pascal far egc_shift_left(screen_x_t x1, vram_y_t y1,
        screen_x_t x2, vram_y_t y2, pixel_t dots);
    void pascal far egc_shift_right(screen_x_t x1, vram_y_t y1,
        screen_x_t x2, vram_y_t y2, pixel_t dots);
    void pascal far egc_shift_up(screen_x_t x1, vram_y_t y1,
        screen_x_t x2, vram_y_t y2, pixel_t dots);
    void pascal far egc_shift_down(screen_x_t x1, vram_y_t y1,
        screen_x_t x2, vram_y_t y2, pixel_t dots);
}
void near tiles_invalidate_all(void);
void near playfield_shake_update_and_render(void);

#endif
