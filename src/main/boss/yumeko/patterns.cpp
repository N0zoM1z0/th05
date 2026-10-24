// Natural movement and attack behavior independently recovered from original
// TH05. ReC98 b6ba5b0a disassembly supports semantics, not source acceptance.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/patterns.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_fan_mirrored boss_statebyte[15]

bool pascal near yumeko_flystep_bounce(subpixel_t length, int end_frame)
{
    unsigned char angle;
    if(boss.phase_frame == 1) {
        angle = randring2_next16();
        vector2(boss.pos.velocity.x.v, boss.pos.velocity.y.v, angle, length);
        boss.sprite = YUMEKO_SPRITE_MOVE;
    }
    boss.pos.cur.x.v += boss.pos.velocity.x.v;
    boss.pos.cur.y.v += boss.pos.velocity.y.v;
    if((boss.pos.cur.x.v <= to_sp(48)) || (boss.pos.cur.x.v >= to_sp(336))) {
        boss.pos.velocity.x.v *= -1;
    }
    if((boss.pos.cur.y.v <= to_sp(48)) || (boss.pos.cur.y.v >= to_sp(128))) {
        boss.pos.velocity.y.v *= -1;
    }
    if(boss.phase_frame >= end_frame) {
        boss.sprite = YUMEKO_SPRITE_STILL;
        return true;
    }
    return false;
}

void near yumeko_pattern_sword_fan(void)
{
    if(boss.phase_frame == 16) {
        boss.sprite = YUMEKO_SPRITE_CHARGE;
        sword_template.twirl_time = 48;
        sword_template.speed.v = 5 * 16;
        sword_template.angle = 0x70;
        yumeko_fan_mirrored = randring2_next16_and(1);
        return;
    }
    if((boss.phase_frame > 32) && ((boss.phase_frame % 2) == 0)) {
        if(yumeko_fan_mirrored != 0) {
            sword_template.angle = 0x80 - sword_template.angle;
        }
        vector2_at(sword_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), sword_template.angle);
        swords_add();
        if(yumeko_fan_mirrored != 0) {
            sword_template.angle = 0x80 - sword_template.angle;
        }
        sword_template.angle -= 6;
        if(sword_template.angle <= 0x0C) {
            boss.phase_frame = 0;
            boss.mode = 0;
        }
    }
}

void near yumeko_pattern_red_ring(void)
{
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 7, 6);
        if(boss.phase_frame == 16) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_CLOUD_BACKWARDS | YUMEKO_NO_DECELERATE;
            bullet_template.patnum = YUMEKO_BALL_RED;
            bullet_template.group = BG_RING;
            bullet_template.speed.v = 3 * 16 + 12;
            bullet_template.spread = 16;
            bullet_template_tune();
            snd_se_play(8);
        }
        return;
    }
    if((boss.phase_frame % 4) == 0) {
        bullet_template.angle = randring2_next16();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            randring2_next16_mod(to_sp(32)), bullet_template.angle);
        bullets_add_regular();
        snd_se_play(3);
    }
    if(boss.phase_frame == 80) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}
