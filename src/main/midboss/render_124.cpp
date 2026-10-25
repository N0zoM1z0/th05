// Actual layered stage1 and scrolling stage2/4 sprite/damage render behavior.
#pragma option -zCMID_FG_TEXT -zPmain_01
#include "src/main/midboss/render_124.hpp"
#pragma codeseg MID_FG_TEXT main_01

void pascal near midboss1_render(void)
{
    int left;
    int top;
    int patnum;
    if(midboss.phase < MIDBOSS5_PHASE_EXPLODE_BIG) {
        left = (midboss.pos.cur.x.v >> 4) + 16;
        top = scroll_subpixel_y_to_vram_seg1(midboss.pos.cur.y.v);
        patnum = midboss.sprite + stage_frame_mod16 / 4;
        super_roll_put(left, top, patnum);
        left = midboss.pos.cur.x.v >> 4;
        top = scroll_subpixel_y_to_vram_seg1(midboss.pos.cur.y.v - 16 * 16);
        if(midboss.phase == 2) {
            patnum = MID1_PHASE2_PAT + stage_frame_mod8 / 2;
            super_roll_put(left, top, patnum);
        } else if(midboss.phase == 3) {
            patnum = MID1_PHASE3_PAT + stage_frame_mod8 / 2;
            if(midboss.damage_this_frame == 0) {
                super_roll_put(left, top, patnum);
            } else {
                super_roll_put_1plane(left, top, patnum, 0, MID_FG_PUT_PLANES);
                midboss.damage_this_frame = 0;
            }
        }
    } else if(midboss.phase == MIDBOSS5_PHASE_EXPLODE_BIG) {
        midboss_defeat_render();
    }
}

void pascal near midboss2_render(void)
{
    int left;
    int top;
    int patnum;
    if(midboss.phase < MIDBOSS5_PHASE_EXPLODE_BIG) {
        if(midboss.pos.cur.y.v < 0) {
            return;
        }
        left = midboss.pos.cur.x.v >> 4;
        top = scroll_subpixel_y_to_vram_seg1(midboss.pos.cur.y.v - 16 * 16);
        if(midboss.sprite == MID2_STILL_PAT) {
            patnum = MID2_STILL_PAT + stage_frame_mod16 / 4;
        } else {
            patnum = MID2_MOVING_PAT + stage_frame_mod8 / 2;
        }
        if(midboss.damage_this_frame == 0) {
            super_roll_put(left, top, patnum);
        } else {
            super_roll_put_1plane(left, top, patnum, 0, MID_FG_PUT_PLANES);
            midboss.damage_this_frame = 0;
        }
    } else if(midboss.phase == MIDBOSS5_PHASE_EXPLODE_BIG) {
        midboss_defeat_render();
    }
}

void pascal near midboss4_render(void)
{
    int left;
    int top;
    int patnum;
    if(midboss.phase < MIDBOSS5_PHASE_EXPLODE_BIG) {
        if(midboss.pos.cur.y.v < 0) {
            return;
        }
        left = midboss.pos.cur.x.v >> 4;
        top = scroll_subpixel_y_to_vram_seg1(midboss.pos.cur.y.v - 16 * 16);
        patnum = midboss.sprite + stage_frame_mod16 / 4;
        if(midboss.damage_this_frame == 0 && boss_statebyte[15] != 0) {
            super_roll_put(left, top, patnum);
        } else {
            super_roll_put_1plane(left, top, patnum, 0, MID_FG_PUT_PLANES);
            midboss.damage_this_frame = 0;
        }
    } else if(midboss.phase == MIDBOSS5_PHASE_EXPLODE_BIG) {
        midboss_defeat_render();
    }
}
