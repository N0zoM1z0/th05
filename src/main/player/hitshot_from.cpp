// Turn a colliding shot into a hit animation, after ReC98
// th05/main/player/hitshot_from.asm (the original TCC body).
#pragma option -zCSHOT_RUNTIME_MAIN01_CONTEXT -zPmain_01
#include "src/main/player/shot_runtime.hpp"
#pragma codeseg SHOT_RUNTIME_MAIN01_CONTEXT main_01

extern unsigned int hitshot_next_free_id;

static const int HITSHOT_BRAKE_DIVISOR = 6;

extern "C" void pascal near hitshot_from(Shot near *shot)
{
    hitshot_t near *p = &hitshots[hitshot_next_free_id];
    if(hitshot_next_free_id < (HITSHOT_COUNT - 1)) {
        hitshot_next_free_id++;
    } else {
        hitshot_next_free_id = 0;
    }
    shot->flag = F_REMOVE;
    if(p->age != 0) { // ZUN bug: the slot is never reused while occupied.
        return;
    }
    p->age = 1;
    // The original compares the patnum as an unsigned byte.
    if(static_cast<unsigned char>(shot->patnum_base) == 20) {
        p->patnum = 28;
    } else {
        p->patnum = 32;
    }
    p->pos.cur = shot->pos.cur;
    p->pos.prev = shot->pos.prev;
    p->pos.velocity.x.v = (shot->pos.velocity.x.v / HITSHOT_BRAKE_DIVISOR);
    p->pos.velocity.y.v = (shot->pos.velocity.y.v / HITSHOT_BRAKE_DIVISOR);
}
