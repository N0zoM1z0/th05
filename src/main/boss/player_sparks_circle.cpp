// Source-backed full 22-byte far player-centered spark burst wrapper.
// ReC98 th05_main.asm sub_158CC; near Pascal spark callee stays foreign.
#pragma option -zCPLAYER_SPARK_RING_TEXT
#include "src/shared/geometry.hpp"
extern PlayfieldMotion player_pos;
#pragma codeseg PLAYER_SPARK_RING_TEXT main_03
void pascal near sparks_add_circle(Subpixel x, Subpixel y,
    subpixel_t radius, int count);
void far player_sparks_circle(void)
{
    sparks_add_circle(player_pos.cur.x, player_pos.cur.y, 192, 24);
}
