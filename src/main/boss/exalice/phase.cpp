// Full original bomb immunity wrapper and Extra-specific phase transition.
#pragma option -zCEXALICE_PHASE_TEXT -zPmain_03
#include "src/main/boss/late_game_state_publics.h"
#include "src/main/boss/exalice/phase.hpp"
#include "src/main/boss/exalice/update_phases.hpp"
#include "src/main/boss/exalice/bomb_phase_protocol.hpp"

int far exalice_hittest_shots(void)
{
    if(bombing) {
        exalice_bomb_invincibility = EXALICE_BOMB_INVINCIBILITY_RELOAD;
    }
    if(exalice_bomb_invincibility == EXALICE_BOMB_INVINCIBILITY_EXPIRED) {
        return boss_hittest_shots();
    }
    return EXALICE_SUPPRESSED_SHOT_RESULT;
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
    boss.phase_frame = EXALICE_NEW_PHASE_FIRST_FRAME;
    boss.mode = EXALICE_MODE_REPOSITION;
    boss.phase_state.patterns_seen = EXALICE_NEW_PHASE_PATTERN_COUNT;
    boss.hp = boss.phase_end_hp;
    boss.phase_end_hp = next_end_hp;
}
