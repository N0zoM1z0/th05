// Natural later Yumeko attacks recovered from original TH05 behavior.
// ReC98 b6ba5b0a disassembly is evidence; no compiler body is transcribed.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/phase_patterns.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_angle_a boss_statebyte[15]
#define yumeko_angle_b boss_statebyte[14]
#define yumeko_phase4_fast boss_statebyte[13]
#define yumeko_volley_frames boss_statebyte[12]
#define yumeko_sword_interval boss_statebyte[0]

void near yumeko_pattern_aimed_swords(void)
{
    unsigned char angle;
    int frame;
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 7, 6);
        if(boss.phase_frame == 16) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = 0x12; // Forward cloud, no deceleration.
            bullet_template.patnum = 84; // Red directional vector bullet.
            bullet_template.group = BG_SINGLE;
            bullet_template.speed.v = 6 * 16;
            bullet_template_tune();
            snd_se_play(8);
            sword_template.twirl_time = 32;
            sword_template.speed.v = 4 * 16 + 12;
            yumeko_phase4_fast = 0;
            yumeko_volley_frames = 32;
        }
        return;
    }
    frame = boss.phase_frame % 64;
    if((frame < yumeko_volley_frames) && ((frame & 1) == 0)) {
        bullet_template.origin.x.v -= to_sp(32);
        bullet_template.origin.y.v -= to_sp(16);
        if(frame == 0) {
            yumeko_angle_a = player_angle_from(
                bullet_template.origin.x, bullet_template.origin.y, 0);
            // Preserve the canonical Subpixel parameter type without adding
            // methods or constructors to the accepted shared geometry class.
            Subpixel right_x;
            right_x.v = bullet_template.origin.x.v + to_sp(64);
            yumeko_angle_b = player_angle_from(right_x, bullet_template.origin.y, 0);
        }
        bullet_template.angle = yumeko_angle_a;
        bullets_add_regular();
        bullet_template.origin.x.v += to_sp(64);
        bullet_template.angle = yumeko_angle_b;
        bullets_add_regular();
        snd_se_play(3);
    }
    if((boss.phase_frame % yumeko_sword_interval) == 0) {
        angle = randring2_next16_and(0x1F) - 0x0F;
        sword_template.origin.y.v = randring2_next16_mod(to_sp(96));
        sword_template.origin.x.v = randring2_next16_mod(to_sp(352)) + to_sp(16);
        sword_template.angle = player_angle_from(
            sword_template.origin.x, sword_template.origin.y, angle);
        swords_add();
    }
    if((boss.hp - boss.phase_end_hp < 600) && (yumeko_phase4_fast == 0)) {
        yumeko_phase4_fast = 1;
        yumeko_sword_interval = select_for_rank(16, 8, 4, 4);
        yumeko_volley_frames = select_for_rank(40, 48, 52, 52);
        boss_explode_small(ET_CIRCLE);
        if(bullet_clear_time < 20) {
            bullet_clear_time = 20;
        }
    }
}

#include "src/main/boss/yumeko/spreads.inl"
