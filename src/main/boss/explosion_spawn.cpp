// Boss explosion creation; semantics shared with TH04's explosion family.
#pragma option -zCBOSS_EXP_SPAWN_TEXT
#pragma option -zPmain_03

#include "src/main/boss/explosion.hpp"
#include "src/main/stage/setup.hpp"

#pragma codeseg BOSS_EXP_SPAWN_TEXT main_03

enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7FFF
};

extern "C" void pascal far snd_se_play(int effect);

void far explosions_small_reset(void)
{
    explosions_small[0].alive = false;
    explosions_small[1].alive = false;
}

void pascal near boss_explode_small(explosion_type_t type)
{
    Explosion near *p = explosions_small;
    if(p->alive) {
        p++;
    }
    p->alive = true;
    p->age = 0;
    p->center.x.v = boss.pos.cur.x.v;
    p->center.y.v = boss.pos.cur.y.v;
    p->radius_cur.x.v = 8;
    p->radius_cur.y.v = 8;
    p->radius_delta.x.v = (11 << 4);
    p->radius_delta.y.v = (11 << 4);
    p->angle_offset = 0;
    switch(type) {
    case ET_NW_SE:
        p->angle_offset = 0x20;
        break;
    case ET_SW_NE:
        p->angle_offset = 0xE0;
        break;
    case ET_HORIZONTAL:
        p->radius_delta.x.v = (13 << 4);
        p->radius_delta.y.v = (7 << 4);
        break;
    case ET_VERTICAL:
        p->radius_delta.x.v = (7 << 4);
        p->radius_delta.y.v = (13 << 4);
        break;
    }
    snd_se_play(15);
}

void pascal near boss2_explode_small(unsigned int type)
{
    subpixel_t x = boss.pos.cur.x.v;
    subpixel_t y = boss.pos.cur.y.v;
    boss.pos.cur = boss2.pos.cur;
    boss_explode_small(static_cast<explosion_type_t>(type));
    boss.pos.cur.x.v = x;
    boss.pos.cur.y.v = y;
}

void near boss_explode_big_circle(void)
{
    Explosion near *p = &explosions_big;
    p->alive = true;
    p->age = 0;
    p->center.x.v = boss.pos.cur.x.v;
    p->center.y.v = boss.pos.cur.y.v;
    p->radius_cur.x.v = 8;
    p->radius_cur.y.v = 8;
    p->radius_delta.x.v = (12 << 4);
    p->radius_delta.y.v = (12 << 4);
    p->angle_offset = 0;
    snd_se_play(12);
}

void near boss2_explode_big_circle(void)
{
    subpixel_t x = boss.pos.cur.x.v;
    subpixel_t y = boss.pos.cur.y.v;
    boss.pos.cur = boss2.pos.cur;
    boss_explode_big_circle();
    boss.pos.cur.x.v = x;
    boss.pos.cur.y.v = y;
}
