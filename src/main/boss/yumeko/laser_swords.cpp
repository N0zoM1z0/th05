// Yumeko's second stationary attack: paired aimed volleys, plus a shootout
// laser and two swords at a regular interval. Same structure as the aimed-sword
// attack in aimed_swords.inl.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/laser_swords.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_laser_interval yumeko_boss_scratch.laser_swords.laser_spawn_interval
#define yumeko_volley_frames yumeko_boss_scratch.laser_swords.volley_frames
#define yumeko_laser_fast yumeko_boss_scratch.laser_swords.pattern_byte13.laser_swords_accelerated
#define yumeko_angle_b yumeko_boss_scratch.laser_swords.pattern_byte14.paired_angle_b
#define yumeko_angle_a yumeko_boss_scratch.laser_swords.pattern_byte15.sword_pattern_angle_a

// Remaining HP before the phase ends at which the attack speeds up.
#define YLS_NEAR_HP_GATE 500

void near yumeko_pattern_laser_swords(void)
{
    unsigned char angle;
    int i;
    int frame;
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 7, 6);
        if(boss.phase_frame == 16) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = (0x02 | YUMEKO_NO_DECELERATE); // Forward cloud.
            bullet_template.patnum = 116; // Blue directional vector bullet.
            bullet_template.group = BG_SINGLE;
            bullet_template.speed.v = (6 * 16);
            bullet_template_tune();
            snd_se_play(8);
            laser_template.age = 24;
            laser_template.shootout_speed.v = (6 * 16 + 4);
            laser_template.coords.width.nonshrink = 6;
            laser_template.col = 8;
            laser_template.active_at_age.grow = 28;
            yumeko_laser_fast = 0;
            yumeko_volley_frames = 32;
            sword_template.twirl_time = 32;
            sword_template.speed.v = (4 * 16 + 12);
        }
        return;
    }
    // Pairs of aimed bullets on every second frame of a 64-frame cycle, from
    // two points 64 pixels apart above Yumeko. Both angles are aimed once at
    // the start of each cycle.
    frame = boss.phase_frame % 64;
    if(frame < yumeko_volley_frames && (frame & 1) == 0) {
        bullet_template.origin.x.v -= to_sp(32);
        bullet_template.origin.y.v -= to_sp(16);
        if(frame == 0) {
            yumeko_angle_a = player_angle_from(
                bullet_template.origin.x, bullet_template.origin.y, 0);
            yumeko_angle_b = yumeko_angle_from_xy(
                bullet_template.origin.x.v + to_sp(64), bullet_template.origin.y.v, 0);
        }
        bullet_template.angle = yumeko_angle_a;
        bullets_add_regular();
        bullet_template.origin.x.v += to_sp(64);
        bullet_template.angle = yumeko_angle_b;
        bullets_add_regular();
        snd_se_play(3);
    }
    // An aimed shootout laser from a random point near the top, plus two
    // swords aimed at the player with a random deviation of up to 15 angle
    // units either way.
    if((boss.phase_frame % yumeko_laser_interval) == 0) {
        laser_template.coords.origin.y.v = to_sp(32);
        laser_template.coords.origin.x.v = randring2_next16_mod(to_sp(256)) + to_sp(64);
        laser_template.coords.angle = player_angle_from(
            laser_template.coords.origin.x, laser_template.coords.origin.y, 0);
        lasers_shootout_add();
        for(i = 0; i < 2; i++) {
            angle = randring2_next16_and(0x1F) - 0x0F;
            sword_template.origin.y.v = randring2_next16_mod(to_sp(96));
            sword_template.origin.x.v = randring2_next16_mod(to_sp(352)) + to_sp(16);
            sword_template.angle = player_angle_from(
                sword_template.origin.x, sword_template.origin.y, angle);
            swords_add();
        }
    }
    if(boss.hp - boss.phase_end_hp < YLS_NEAR_HP_GATE && yumeko_laser_fast == 0) {
        yumeko_laser_fast = 1;
        yumeko_laser_interval = select_for_rank(34, 28, 20, 20);
        // ZUN quirk: Lunatic gets a shorter volley window than Hard.
        yumeko_volley_frames = select_for_rank(40, 48, 52, 48);
        boss_explode_small(ET_CIRCLE);
        if(bullet_clear_time < 20) {
            bullet_clear_time = 20;
        }
    }
}

#undef YLS_NEAR_HP_GATE
