// Two complete natural hit/state wrappers, original MAIN177F0..1785F.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/hittest.hpp"

int pascal near yuki_hittest_shots_damage(subpixel_t radius_x,
    subpixel_t radius_y, int effect)
{
    shots_hittest_against_boss = true;
    shot_hitbox_radius.x.v = radius_x;
    shot_hitbox_radius.y.v = radius_y;
    shot_hitbox_center = boss2.pos.cur;
    int damage = shots_hittest();
    if(damage) {
        snd_se_play(effect);
    }
    shots_hittest_against_boss = false;
    return damage;
}

unsigned char near mai_yuki_hittest_shots(void)
{
    if(boss_hittest_shots()) {
        return MY_HIT_MAI_DEFEATED;
    }
    boss2.damage_this_frame = yuki_hittest_shots_damage(to_sp(24), to_sp(24), 4);
    boss2.hp -= boss2.damage_this_frame;
    if(boss2.hp <= boss2.phase_end_hp) {
        return MY_HIT_YUKI_DEFEATED;
    }
    return MY_HIT_NONE;
}
