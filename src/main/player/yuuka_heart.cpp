// Natural pixel-space radial heart animation; original coordinates are not Q12.4.
#pragma option -zCYUUKA_HEART_TEXT -zPmain_01
#include "src/main/player/yuuka_heart.hpp"
#pragma codeseg YUUKA_HEART_TEXT main_01

void near yuuka_heart_update_and_render(void)
{
    int i;
    if(bomb_frame == BOMB_CIRCLE_FRAMES) {
        bomb_anim.yuuka.distance = 16;
    }
    for(i = 0; i < 16; i++, bomb_anim.yuuka.angle += 0x10) {
        // The actual generic two-word point interface is also used for pixels.
        vector2_at(reinterpret_cast<SPPoint near &>(bomb_anim.yuuka.topleft),
            192, 160, bomb_anim.yuuka.distance, bomb_anim.yuuka.angle);
        if(bomb_anim.yuuka.topleft.x >= 0 &&
            bomb_anim.yuuka.topleft.x <= PLAYFIELD_RIGHT - 32 &&
            bomb_anim.yuuka.topleft.y >= 0 &&
            bomb_anim.yuuka.topleft.y <= PLAYFIELD_BOTTOM - 48) {
            super_roll_put_1plane(bomb_anim.yuuka.topleft.x,
                bomb_anim.yuuka.topleft.y, PAT_PLAYCHAR_BOMB_SHAPE, 0,
                BOMB_PLANE_PUT);
        }
    }
    bomb_anim.yuuka.angle += 2;
    bomb_anim.yuuka.distance += 2;
}
