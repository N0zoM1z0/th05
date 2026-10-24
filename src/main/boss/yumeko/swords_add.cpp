// Natural allocator semantics from original TH05 sword pool behavior.
// ReC98 b6ba5b0a swords_add_update.asm is corroborating disassembly evidence.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/swords_add.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

extern "C" void pascal near swords_add(void)
{
    subpixel_t speed;
    sword_t near *sword;
    int i;
    speed = playperf_speedtune(sword_template.speed.v);
    circles_color = 9;
    for((sword = swords, i = 1); i < (1 + SWORD_COUNT); (i++, sword++)) {
        if(sword->flag != F_FREE) {
            continue;
        }
        sword->flag = F_ALIVE;
        sword->pos.cur = sword_template.origin;
        circles_add_shrinking(sword_template.origin.x.v, sword_template.origin.y.v);
        vector2_near(sword->pos.velocity, sword_template.angle, speed);
        sword->angle = sword_template.angle;
        sword->patnum_tiny = bullet_patnum_for_angle(193, sword_template.angle);
        sword->speed.v = speed;
        sword->twirl_time = sword_template.twirl_time;
        break;
    }
}
