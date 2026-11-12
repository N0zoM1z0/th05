#include "src/main/boss/defeat_combat_rules.hpp"
// Original TH05 boss/player collision: AX holds X and DX holds Y.
// ReC98 th04/main/boss/boss.cpp preserves both DOS register lvalues.
// The entire source is shared by the natural single-function wrapper and
// the canonical generic Boss translation unit, with no duplicate body.
void near boss_hittest_player(void)
{
    _AX = boss.pos.cur.x.v;
    _DX = boss.pos.cur.y.v;
    _AX -= player_pos.cur.x.v;
    _DX -= player_pos.cur.y.v;
    if(overlap_wh_inplace_fast(
        _DX, _AX, to_sp(GDEF_CONTACT_HEIGHT_RADIUS_PX),
        to_sp(GDEF_CONTACT_WIDTH_RADIUS_PX)
    )) {
        player_is_hit = true;
    }
}
