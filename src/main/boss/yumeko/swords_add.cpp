// Natural allocator semantics from original TH05 sword pool behavior.
// ReC98 b6ba5b0a swords_add_update.asm is corroborating disassembly evidence.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/swords_add.hpp"
#include "src/main/boss/yumeko/sword_pool_rules.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

extern "C" void pascal near swords_add(void)
{
    subpixel_t speed;
    sword_t near *sword;
    int i;
    speed = playperf_speedtune(sword_template.speed.v);
    circles_color = YMS_SPAWN_CIRCLE_COLOR;
    for((sword = swords, i = YMS_FIRST_ACTIVE_SLOT); i < (YMS_FIRST_ACTIVE_SLOT + SWORD_COUNT); (i++, sword++)) {
        if(sword->flag != F_FREE) {
            continue;
        }
        sword->flag = F_ALIVE;
        sword->pos.cur = sword_template.origin;
        circles_add_shrinking(sword_template.origin.x.v, sword_template.origin.y.v);
        vector2_near(sword->pos.velocity, sword_template.angle, speed);
        sword->angle = sword_template.angle;
        sword->patnum_tiny = bullet_patnum_for_angle(YMS_DIRECTIONAL_SPRITE_BASE, sword_template.angle);
        sword->speed.v = speed;
        sword->twirl_time = sword_template.twirl_time;
        break;
    }
}
