// Shared, unchanged complete Louise foreground definition.
#ifndef TH05_LOUISE_FG_BODY_INCLUDED
#define TH05_LOUISE_FG_BODY_INCLUDED
void pascal near louise_fg_render(void)
{
    int patnum;
    int left;
    int top;
    left = boss.pos.cur.x.v >> 4;
    top = (boss.pos.cur.y.v >> 4) - 16;
    if(boss.phase == BOSS_FG_PHASE_EXPLODE_BIG) {
        super_large_put(left, top, boss.sprite);
    } else {
        patnum = boss.sprite + stage_frame_mod16 / BOSS_FG_ANIMATION_FRAMES;
        if(boss.damage_this_frame == 0) {
            super_put(left, top, patnum);
        } else {
            super_put_1plane(left, top, patnum, 0, BOSS_FG_PUT_PLANES);
        }
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
}
#endif
