// Natural Extra midboss state machine reconstructed from original TH05
// behavior, using TH04 maintained mx_update.cpp state-machine conventions.
// ReC98 b6ba5b0a th05_main.asm is disassembly evidence, not source acceptance.
#pragma option -zCMIDBOSSX_TEXT -zPmain_03
#include "src/main/midboss/extra.hpp"
#include "src/main/midboss/extra_scratch.hpp"
#pragma codeseg MIDBOSSX_TEXT main_03

#define midbossx_second_half midboss_extra_scratch.second_pattern_set
#define midbossx_patterns_done midboss_extra_scratch.completed_dashes
#define midbossx_dashing midboss_extra_scratch.dash_animation_active

void pascal far midbossx_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    gather_template.center = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case MIDBOSSX_PHASE_ENTRANCE_DASH:
        midboss_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        midboss.angle = 0x40;
        if(midbossx_dash_update(midboss.phase_frame)) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            midbossx_dashing = 0;
            midbossx_patterns_done = 0;
            midbossx_second_half = 0;
            midbossx_pattern = midbossx_pattern_spread;
        }
        break;

    case MIDBOSSX_PHASE_ATTACK_DASHES:
        if(midbossx_dash_update(midboss.phase_frame - MIDBOSSX_ATTACK_DASH_FRAME_BIAS)) {
            if(midbossx_second_half == 0 && midboss.hp < 1000) {
                midboss_score_bonus(10);
                if(bullet_clear_time < 20) {
                    bullet_clear_time = 20;
                }
                snd_se_play(15);
                midbossx_second_half++;
            }
            midbossx_dashing = MIDBOSSX_DASH_ACTIVE;
            midboss.phase_frame = 0;
            midboss.angle = midbossx_dash_angles[midbossx_patterns_done & MIDBOSSX_DASH_ANGLE_TABLE_MASK];
            midbossx_patterns_done++;
            midbossx_pattern = midbossx_patterns[midbossx_second_half]
                [midbossx_patterns_done % MIDBOSSX_ATTACK_CHOICE_MODULUS];
        }
        midboss.damage_this_frame =
            midboss_hittest_shots_damage(to_sp(24), to_sp(24), 4);
        midboss.hp -= midboss.damage_this_frame;
        if(midbossx_patterns_done < MIDBOSSX_MAX_COMPLETED_DASHES) {
            if(midboss.hp > 0) {
                break;
            }
            bullet_zap.active = true;
            midboss_score_bonus(30);
            items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_1UP);
        }
        midboss.phase = MIDBOSSX_PHASE_LARGE_EXPLOSION;
        midboss.sprite = 4;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(8), 48);
        snd_se_play(12);
        break;

    default:
        midboss_defeat_update();
        hud_hp_update_and_render(midboss.hp, 3000);
        return;
    }
    hud_hp_update_and_render(midboss.hp, 3000);
    homing_target.x = midboss.pos.cur.x;
    homing_target.y = midboss.pos.cur.y;
}
