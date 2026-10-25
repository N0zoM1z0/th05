// Large-bullet clouds and normal/clearing pellet rendering in true pool order.
#pragma option -zCBULLET_RENDER_TEXT -zPmain_01
#include "src/main/bullet/render.hpp"
#pragma codeseg BULLET_RENDER_TEXT main_01

extern "C" void pascal near bullets_render(void)
{
    int i;
    int patnum;
    bullet_t near *bullet;
    _ES = SEG_PLANE_B;
    bullet = &bullets[BULLET_COUNT - 1];
    for(i = 0; i < BULLET16_COUNT; i++, bullet--) {
        if(bullet->flag == F_ALIVE) {
            if(bullet->spawn_flag <= BSF_CLOUD_BACKWARDS) {
                z_super_roll_put_tiny_16x16(
                    (bullet->pos.cur.x.v >> 4) + 24,
                    scroll_subpixel_y_to_vram_seg1(bullet->pos.cur.y.v + TO_SP(8)),
                    bullet->patnum);
            } else if(bullet->pos.cur.y.v >= 0 &&
                bullet->pos.cur.y.v < TO_SP(PLAYFIELD_H) &&
                bullet->pos.cur.x.v >= 0 &&
                bullet->pos.cur.x.v < TO_SP(PLAYFIELD_W + 16)) {
                if(bullet->patnum < BR_PAT_N_RED ||
                    (bullet->patnum >= PAT_BULLET16_D_BLUE &&
                     bullet->patnum < PAT_BULLET16_D_GREEN) ||
                    (bullet->patnum >= PAT_BULLET16_V_BLUE &&
                     bullet->patnum < BR_CLOUD_PELLET + BULLET_CLOUD_CELS)) {
                    patnum = BR_CLOUD_BLUE - 1;
                } else {
                    patnum = BR_CLOUD_RED - 1;
                }
                patnum += bullet->spawn_flag / BR_CLOUD_RATE;
                bullet_render_tiny32((bullet->pos.cur.x.v >> 4) + 16,
                    scroll_subpixel_y_to_vram_seg1(bullet->pos.cur.y.v), patnum);
            }
        }
    }
    if(bullet_zap.active == 0 && bullet_clear_time == 0) {
        // The postdecrement is real: the final zero test leaves the count -1.
        while(pellet_clouds_render_count-- != 0) {
            bullet = pellet_clouds_render[pellet_clouds_render_count];
            patnum = (BR_CLOUD_PELLET - 1) + bullet->spawn_flag / BR_CLOUD_RATE;
            z_super_roll_put_tiny_16x16((bullet->pos.cur.x.v >> 4) + 24,
                scroll_subpixel_y_to_vram_seg1(bullet->pos.cur.y.v + TO_SP(8)), patnum);
        }
        bullet_render_color(15);
        pellets_render_top();
        bullet_render_color(pellet_bottom_col);
        pellets_render_bottom();
    } else {
        // The first loop left the real iterator at the final pellet slot.
        for(i = 0; i < PELLET_COUNT; i++, bullet--) {
            if(bullet->flag == F_ALIVE) {
                z_super_roll_put_tiny_16x16((bullet->pos.cur.x.v >> 4) + 24,
                    scroll_subpixel_y_to_vram_seg1(bullet->pos.cur.y.v + TO_SP(8)),
                    bullet->patnum);
            }
        }
    }
}
