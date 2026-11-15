// Spawns a new sword from [sword_template] into the first free slot of the
// sword pool, together with a shrinking circle at its origin.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/swords_add.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define YMS_SPAWN_CIRCLE_COLOR 9

extern "C" void pascal near swords_add(void)
{
    subpixel_t speed;
    sword_t near *sword;
    int i;
    speed = playperf_speedtune(sword_template.speed.v);
    circles_color = YMS_SPAWN_CIRCLE_COLOR;
    for((sword = swords, i = 1); i < (1 + SWORD_COUNT); (i++, sword++)) {
        if(sword->flag != F_FREE) {
            continue;
        }
        sword->flag = F_ALIVE;
        sword->pos.cur = sword_template.origin;
        circles_add_shrinking(sword_template.origin.x.v, sword_template.origin.y.v);
        vector2_near(sword->pos.velocity, sword_template.angle, speed);
        sword->angle = sword_template.angle;
        sword->patnum_tiny = bullet_patnum_for_angle(193, sword_template.angle); // First sword sprite.
        sword->speed.v = speed;
        sword->twirl_time = sword_template.twirl_time;
        break;
    }
}

#undef YMS_SPAWN_CIRCLE_COLOR
