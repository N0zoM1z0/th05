// Natural TH05 stage-five callback at original MAIN 1527:1682.
#include "src/main/midboss/stage5.hpp"

#define midboss5_patterns_done boss_statebyte[13]
#define midboss5_pattern_phase boss_statebyte[14]

void pascal far midboss5_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    gather_template.center = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case 0:
        midboss.pos.update_seg3();
        midboss_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        if(midboss.phase_frame >= 192) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            boss_statebyte[15] = 0;
            midboss5_pattern_phase = 1;
            midboss5_patterns_done = 0;
            midboss.pos.velocity.y.v = 0;
            midboss5_pattern_func = midboss5_pattern_blue_spread;
        }
        break;

    case 1:
        midboss.pos.prev = midboss.pos.cur;
        switch(midboss5_pattern_phase) {
        case 0:
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
        case 1:
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
