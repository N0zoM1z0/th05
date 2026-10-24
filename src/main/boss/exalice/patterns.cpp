// Natural EX-Alice charge, random fan and alternating turning rings.
#pragma option -zCEXALICE_PAT_TEXT -zPmain_03
#include "src/main/boss/exalice/patterns.hpp"

bool near exalice_charge_update(void)
{
    gather_add_only_3stack(boss.phase_frame - 48, 6, 7);
    if(boss.phase_frame == 48) {
        boss.sprite = 181;
        snd_se_play(8);
    }
    if(boss.phase_frame >= 64) {
        if(exalice_pattern()) {
            boss.phase_frame = 0;
            boss.mode = 0;
            return true;
        }
    }
    return false;
}

bool near exalice_pattern_random_fan(void)
{
    bullet_template.spawn_type = 0x10;
    bullet_template.speed.v = randring2_next16_and(0x1F) + to_sp(2.5f);
    bullet_template.angle = (randring2_next16_and(0x7F) & ~7) - 0x40;
    bullet_template.group = BG_SPREAD_AIMED;
    bullet_template.patnum = EXALICE_PAT_V_RED;
    exalice_set_spread(5, 12);
    bullets_add_regular();
    if((boss.phase_frame % 4) == 0) {
        snd_se_play(3);
    }
    return (boss.phase_frame == 128);
}

bool near exalice_pattern_turning_rings(void)
{
    if(boss.phase_frame == 64) {
        boss_statebyte[15] = 1 - boss_statebyte[15];
    }
    if((boss.phase_frame % 4) == 0) {
        bullet_template.spawn_type = 0x13;
        bullet_template.speed.v = to_sp(4);
        bullet_template.angle = boss_statebyte[15]
            ? bullet_template.angle + 2 : bullet_template.angle - 2;
        bullet_template.group = BG_RING;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN_AIMED;
        bullet_special.turns_max = 1;
        exalice_set_spread(12, 10);
        bullet_template.patnum = 48;
        if((boss.phase_frame % 8) == 0) {
            bullets_add_regular();
        } else {
            exalice_set_spread(8, 10);
            bullet_template.patnum = EXALICE_PAT_V_RED;
            bullets_add_special();
        }
        snd_se_play(3);
    }
    boss_flystep_random(boss.phase_frame - 100);
    return (boss.phase_frame == 128);
}
