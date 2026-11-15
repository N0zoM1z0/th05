// Kills the player if they touch the boss. AX and DX hold the X and Y
// distance; ZUN wrote this function with these register pseudo-variables.
void near boss_hittest_player(void)
{
    #define delta_x _AX
    #define delta_y _DX

    delta_x = boss.pos.cur.x.v;
    delta_y = boss.pos.cur.y.v;
    delta_x -= player_pos.cur.x.v;
    delta_y -= player_pos.cur.y.v;

    // ZUN quirk: Tests Y before X. Each extent is the full width of the
    // overlap range, so the player dies within +-16 pixels of the boss
    // center in each dimension, inclusive.
    if(overlap_wh_inplace_fast(
        delta_y, delta_x, to_sp(BOSS_H / 2), to_sp(BOSS_W / 2)
    )) {
        player_is_hit = true;
    }

    #undef delta_y
    #undef delta_x
}
