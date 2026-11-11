// Natural phase/pattern state machine at original MAIN 1527:6A92.
#include "src/main/midboss/stage3.hpp"
#include "src/main/midboss/stage3_scratch.hpp"

// The original four-word switch table has a real even-word boundary and one
// compiler zero after the complete function's final RETF. All ABI types above
// are already complete before applying the table-alignment option.
#pragma option -a2

#define midboss3_patterns_done midboss3_scratch.patterns_finished
#define midboss3_pattern midboss3_scratch.active_attack

void pascal far midboss3_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    gather_template.center = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case MIDBOSS3_PHASE_ENTRANCE:
        midboss.pos.update_seg3();
        midboss_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        if(midboss.phase_frame >= 192) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            midboss3_scratch.reposition_returning = 0;
            midboss3_pattern = MIDBOSS3_ATTACK_SPREAD_STACKS;
            midboss3_patterns_done = 1;
            midboss.pos.velocity.x.v = 0;
        }
        break;

    case MIDBOSS3_PHASE_ATTACKS:
        midboss.pos.prev = midboss.pos.cur;
        switch(midboss3_pattern) {
        case MIDBOSS3_ATTACK_REPOSITION:
            if(midboss.phase_frame >= MIDBOSS3_REPOSITION_TRANSITION_FRAMES) {
                midboss3_pattern = (midboss3_patterns_done % 3) + MIDBOSS3_ATTACK_SPREAD_STACKS;
                midboss3_patterns_done++;
                midboss.phase_frame = 0;
                if(midboss3_patterns_done >= (MIDBOSS3_PATTERNS_MAX + 1)) {
                    goto explode;
                }
            }
            break;
        case MIDBOSS3_ATTACK_SPREAD_STACKS:
            midboss3_pattern_1();
            break;
        case MIDBOSS3_ATTACK_AIMED_STACKS:
            midboss3_pattern_2();
            break;
        case MIDBOSS3_ATTACK_DIAMOND_SPREADS:
            midboss3_pattern_3();
            break;
        }
        if(midboss.sprite < MIDBOSS3_SPRITE_INVINCIBLE) {
            stage3_midboss_hittest_shots(to_sp(24), to_sp(24));
        }
        if(midboss.hp > 0) {
            break;
        }
        bullet_zap.active = true;
        midboss_score_bonus(15);
        items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_1UP);

    explode:
        midboss.phase = MIDBOSS3_PHASE_EXPLODE_BIG;
        midboss.sprite = MIDBOSS3_SPRITE_EXPLODE;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(8), 48);
        snd_se_play(12);
        break;

    default:
        midboss_defeat_update();
        hud_hp_update_and_render(midboss.hp, MIDBOSS3_HP_TOTAL);
        return;
    }

    hud_hp_update_and_render(midboss.hp, MIDBOSS3_HP_TOTAL);
    homing_target.x = midboss.pos.cur.x;
    homing_target.y = midboss.pos.cur.y;
}
