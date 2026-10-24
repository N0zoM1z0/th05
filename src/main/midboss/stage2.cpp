// Natural TH05 stage-two midboss state machine, recovered from the original
// callback at 1527:0B7B. Foreign movement/pattern bodies remain separate owners.
#include "src/main/midboss/stage2.hpp"

void pascal far midboss2_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case 0:
        midboss.pos.update_seg3();
        midboss_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        if(midboss.phase_frame >= 256) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            boss_statebyte[15] = 0;
            boss_statebyte[14] = 0x20;
            midboss.pos.velocity.x.v = 0;
            midboss2_orbit_center.x.v = to_sp(192);
            midboss2_orbit_center.y = midboss.pos.cur.y;
        }
        break;

    case 1:
        midboss2_pattern();
        midboss2_move();
        stage2_midboss_hittest_shots(to_sp(24), to_sp(24));
        if(midboss.phase_frame < 1000) {
            if(midboss.hp > 400) {
                break;
            }
            midboss_score_bonus(5);
            if(bullet_clear_time < 20) {
                bullet_clear_time = 20;
            }
        }
        midboss.phase++;
        midboss.sprite = MIDBOSS2_SPRITE_DAMAGED;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(4), 32);
        snd_se_play(15);
        vector2_between_plus(midboss.pos.cur.x.v, midboss.pos.cur.y.v,
            to_sp(192), to_sp(64), 0,
            midboss.pos.velocity.x.v, midboss.pos.velocity.y.v, 1);
        break;

    case 2:
        midboss2_pattern_final();
        midboss.pos.update_seg3();
        stage2_midboss_hittest_shots(to_sp(24), to_sp(24));
        if(midboss.phase_frame < 800) {
            if(midboss.hp > 0) {
                break;
            }
            bullet_zap.active = true;
            midboss_score_bonus(15);
            items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_BOMB);
        }
        midboss.phase = MIDBOSS2_PHASE_EXPLODE_BIG;
        midboss.sprite = MIDBOSS2_SPRITE_EXPLODE;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(8), 48);
        snd_se_play(12);
        break;

    default:
        midboss_defeat_update();
        hud_hp_update_and_render(midboss.hp, MIDBOSS2_HP_TOTAL);
        return;
    }

    hud_hp_update_and_render(midboss.hp, MIDBOSS2_HP_TOTAL);
    homing_target.x = midboss.pos.cur.x;
    homing_target.y = midboss.pos.cur.y;
}
