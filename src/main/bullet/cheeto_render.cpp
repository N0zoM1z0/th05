// Render alternating Cheeto trail nodes and their heads without stage scroll.
#pragma option -zCCHEETO_RENDER_TEXT -zPmain_01 -G
#include <dos.h>
#include "src/main/bullet/cheeto.hpp"

#pragma codeseg CHEETO_RENDER_TEXT main_01
void near grcg_setcolor_direct_raw(void);
extern "C" void __fastcall near cheeto_put(int left, int top, int sprite);

#define cheeto_render_point(point_value, sprite_value) { \
    _DX = ((point_value).y.v >> 4); \
    _AX = ((point_value).x.v >> 4); \
    _AX += (32 - (CHEETO_W / 2)); \
    if(static_cast<int>(_DX) >= (16 - CHEETO_H) && \
       static_cast<int>(_DX) < 384 && \
       static_cast<int>(_AX) >= 0 && static_cast<int>(_AX) < 416) { \
        if(static_cast<int>(_DX) < 0) { _DX += 400; } \
        cheeto_put(_AX, _DX, sprite_value); \
    } \
}

extern "C" void pascal near cheetos_render(void)
{
    int bullet_i;
    int trail_sprite;
    cheeto_head_t near *head = cheeto_heads;
    cheeto_trail_t near *trail = cheeto_trails;
    register int node_i;
    _ES = 0xA800;
    for(bullet_i = 1; bullet_i < (1 + CHEETO_COUNT); bullet_i++, head++, trail++) {
        if(trail->flag == CF_FREE) {
            continue;
        }
        _AH = trail->col;
        grcg_setcolor_direct_raw();
        for(node_i = (CHEETO_TRAIL_NODE_COUNT - 1); node_i > 0; node_i -= 2) {
            trail_sprite = trail->node_sprite[node_i];
            cheeto_render_point(trail->node_pos[node_i], trail_sprite);
        }
        cheeto_render_point(head->pos.cur, head->sprite);
    }
}

#undef cheeto_render_point
