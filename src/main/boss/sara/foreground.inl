// Canonical complete foreground definition.
void pascal near sara_fg_render(void)
{
    int left;
    int top;
    int patnum;
    left = boss.pos.cur.x.v >> 4;
    top = (boss.pos.cur.y.v >> 4) - 16;
    if(boss.phase == BOSS_FG_PHASE_EXPLODE_BIG) {
        super_large_put(left, top, boss.sprite);
    } else {
        if(boss.sprite == SARA_FG_PAT_RIGHT || boss.sprite == SARA_FG_PAT_LEFT) {
            patnum = boss.sprite + stage_frame_mod8 / BOSS_FG_ANIMATION_FRAMES;
        } else if(boss.sprite == SARA_FG_PAT_STAY) {
            patnum = boss.sprite + stage_frame_mod16 / BOSS_FG_ANIMATION_FRAMES;
        } else {
            patnum = boss.sprite;
        }
        if(boss.damage_this_frame == 0) {
            super_put(left, top, patnum);
        } else {
            super_put_1plane(left, top, patnum, 0, BOSS_FG_PUT_PLANES);
        }
    }
    explosions_small_update_and_render();
    explosions_big_update_and_render();
}
