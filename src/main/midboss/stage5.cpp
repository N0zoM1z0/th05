// Natural TH05 stage-five callback at original MAIN 1527:1682.
#include "src/main/midboss/stage5.hpp"
#include "src/main/midboss/stage5_scratch.hpp"

// The native two-phase fight and the movement/attack substate use these
// exact selector bytes; the third slot drives the pattern helper's flight.
static const unsigned char MIDBOSS5_PHASE_ENTRANCE = 0;
static const unsigned char MIDBOSS5_PHASE_PATTERNS = 1;
static const unsigned char MIDBOSS5_MODE_FLYSTEP = 0;
static const unsigned char MIDBOSS5_MODE_ATTACK = 1;
#define midboss5_patterns_done midboss5_scratch.patterns_done
#define midboss5_pattern_phase midboss5_scratch.current_pattern_phase

void pascal far midboss5_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    gather_template.center = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case MIDBOSS5_PHASE_ENTRANCE:
        midboss.pos.update_seg3();
        midboss_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        if(midboss.phase_frame >= 192) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            midboss5_scratch.horizontal_step = 0;
            midboss5_pattern_phase = MIDBOSS5_MODE_ATTACK;
            midboss5_patterns_done = 0;
            midboss.pos.velocity.y.v = 0;
            midboss5_pattern_func = midboss5_pattern_blue_spread;
        }
        break;

    case MIDBOSS5_PHASE_PATTERNS:
        midboss.pos.prev = midboss.pos.cur;
        switch(midboss5_pattern_phase) {
        case MIDBOSS5_MODE_FLYSTEP:
            if(midboss5_flystep()) {
                midboss.phase_frame = 0;
                midboss5_patterns_done++;
                midboss5_pattern_func = MIDBOSS5_PATTERNS[midboss5_patterns_done % 3];
                midboss5_pattern_phase++;
                if(midboss5_patterns_done >= MIDBOSS5_PATTERNS_MAX) {
                    goto explode;
                }
            }
            break;
        case MIDBOSS5_MODE_ATTACK:
            midboss5_pattern_update();
            break;
        }
        stage5_midboss_hittest_shots(to_sp(24), to_sp(24));
        if(midboss.hp > 0) {
            break;
        }
        bullet_zap.active = true;
        midboss_score_bonus(30);
        items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_1UP);

    explode:
        midboss.phase = MIDBOSS5_PHASE_EXPLODE_BIG;
        midboss.sprite = MIDBOSS5_SPRITE_EXPLODE;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(8), 48);
        snd_se_play(12);
        break;

    default:
        midboss_defeat_update();
        hud_hp_update_and_render(midboss.hp, MIDBOSS5_HP_TOTAL);
        return;
    }

    hud_hp_update_and_render(midboss.hp, MIDBOSS5_HP_TOTAL);
    homing_target.x = midboss.pos.cur.x;
    homing_target.y = midboss.pos.cur.y;
}
