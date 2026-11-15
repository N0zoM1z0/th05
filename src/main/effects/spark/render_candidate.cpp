// Plain C++ attempt at sparks_render(), which draws every live spark in GRCG
// color 12 on the blue plane. Not built: the original is kept as assembly
// (scene_render.asm). Borland compiles this to 71 bytes instead of 60, with
// ENTER/LEAVE, stack temporaries for `top` and `left` and a DX reload.
// Pseudo-registers are used only where the callees take register arguments:
// AH for the color helper, ES for the VRAM plane and CL for the spark's cel.
#pragma option -zCSPARK_BATCH_TEXT -zPmain_01 -k-
#include "src/main/effects/spark/render_candidate.hpp"

#define SPARK_RENDER_COLOR 12

extern "C" void near sparks_render(void)
{
    register spark_t near *spark;
    register int sparks_left;
    vram_y_t top;
    screen_x_t left;

    _AH = SPARK_RENDER_COLOR;
    grcg_setcolor_direct_raw();
    _ES = SEG_PLANE_B;
    sparks_left = SPARK_COUNT;
    spark = sparks;
    do {
        if(spark->flag == F_ALIVE) {
            top = scroll_subpixel_y_to_vram_seg1(
                spark->center.cur.y.v + TO_SP(PLAYFIELD_TOP - (SPARK_H / 2)));
            left = (spark->center.cur.x.v +
                TO_SP(PLAYFIELD_LEFT - (SPARK_W / 2))) >> 4;
            _CL = spark->age;
            spark_render(left, top);
        }
        spark++;
    } while(--sparks_left > 0);
}
