// Shinki's cloud circles and 32x32 ball bullets, followed by Cheeto trails.
#pragma option -zCMAIN_0_TEXT -zPmain_01

#include <dos.h>
#include "src/main/boss/shinki/shinki.hpp"

#pragma codeseg MAIN_0_TEXT main_01
void near grcg_setcolor_direct_raw(void);
extern "C" {
    void pascal far grcg_circlefill(int x, int y, int radius);
    void pascal near z_super_roll_put_tiny_32x32_raw(int sprite);
    void pascal near cheetos_render(void);
}

void pascal near shinki_custombullets_render(void)
{
    b6ball_t near *p;
    int i;
    for(p = b6balls, i = 1; i < (1 + B6BALL_COUNT); i++, p++) {
        if(p->flag == B6BF_FREE) {
            continue;
        }
        if(p->flag == B6BF_CLOUD) {
            _AH = 15;
            grcg_setcolor_direct_raw();
            grcg_circlefill(
                (p->pos.cur.x.v >> 4) + 32,
                (p->pos.cur.y.v >> 4) + 16,
                p->cloud_radius.v / 16
            );
        } else {
            _ES = 0xA800;
            _DX = (p->pos.cur.y.v >> 4);
            _AX = (p->pos.cur.x.v >> 4) + (32 - (B6BALL_W / 2));
            if(static_cast<int>(_DX) < 0) {
                continue;
            }
            z_super_roll_put_tiny_32x32_raw(p->patnum_tiny);
        }
    }
    cheetos_render();
}
