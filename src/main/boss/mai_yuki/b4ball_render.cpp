// Animate and draw all 63 live B4 balls through the real tiny-sprite ABI.
#pragma option -zCYUKI_SOLO_RENDER_TEXT -zPmain_01
#include "src/main/boss/mai_yuki/b4ball_render.hpp"
#pragma codeseg YUKI_SOLO_RENDER_TEXT main_01

static const int B4_RENDER_SNOW_HIT = 220;
static const int B4_RENDER_DAMAGE_CELS = 8;
static const int B4_RENDER_ANIMATION_CELS = 4;

extern "C" void pascal near b4balls_render(void)
{
    int i;
    int patnum;
    b4ball_t near *ball;
    _ES = B4_RENDER_VRAM_SEGMENT;
    ball = b4balls;
    for(i = 1; i < 1 + B4BALL_COUNT; i++, ball++) {
        if(ball->flag != 0) {
            patnum = ball->patnum_tiny_base;
            if(patnum < B4_RENDER_SNOW_HIT) {
                patnum += ball->age & (B4_RENDER_ANIMATION_CELS - 1);
                if(ball->damaged_this_frame != 0) {
                    patnum += B4_RENDER_DAMAGE_CELS;
                }
                ball->damaged_this_frame = 0;
            }
            b4_render_tiny32((ball->pos.cur.x.v >> 4) + 16,
                scroll_subpixel_y_to_vram_seg1(ball->pos.cur.y.v), patnum);
        }
    }
}
