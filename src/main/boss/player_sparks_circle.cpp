// Spawns a ring of 24 sparks around the player, with a 12-pixel radius.
// The name is ours; ReC98 calls this function sub_158CC.
#pragma option -zCPLAYER_SPARK_RING_TEXT
#include "src/shared/geometry.hpp"
extern PlayfieldMotion player_pos;
#pragma codeseg PLAYER_SPARK_RING_TEXT main_03
void pascal near sparks_add_circle(Subpixel x, Subpixel y,
    subpixel_t radius, int count);
void far player_sparks_circle(void)
{
    // 192 subpixels = 12 pixels.
    sparks_add_circle(player_pos.cur.x, player_pos.cur.y, 192, 24);
}
