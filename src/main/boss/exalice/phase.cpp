// Full original bomb immunity wrapper and Extra-specific phase transition.
#pragma option -zCEXALICE_PHASE_TEXT -zPmain_03
#include "src/main/boss/exalice/phase.hpp"

int far exalice_hittest_shots(void)
{
    if(bombing) {
        exalice_bomb_invincibility = 39;
    }
    if(exalice_bomb_invincibility == 0) {
        return boss_hittest_shots();
    }
    return 0;
}

void pascal near exalice_phase_next(explosion_type_t type, int next_end_hp)
{
    if(type != ET_NONE) {
        boss_explode_small(type);
        if(!boss_phase_timed_out) {
            bullet_zap_drop_point_items = true;
            bullet_zap.active = true;
            boss_items_drop();
        }
    }
    boss_phase_timed_out = true;
    boss.phase++;
    boss.phase_frame = 0;
    boss.mode = 0;
    boss.phase_state.patterns_seen = 0;
    boss.hp = boss.phase_end_hp;
    boss.phase_end_hp = next_end_hp;
}
