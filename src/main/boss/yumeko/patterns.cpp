// Yumeko's random bouncing movement and the two attacks of her first mobile
// wave: a mirrored sword fan and a ring of red balls.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/patterns.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_fan_mirrored yumeko_pattern_scratch.pattern_byte15.fan_mirrored_side

// Both attacks end by restarting the phase clock and flying to the next
// position.
#define YUMEKO_PATTERNS_ENTER_REPOSITION() { \
    boss.phase_frame = 0; \
    boss.mode = YUMEKO_MODE_REPOSITION; \
}

// On the mirrored side, the fan's angle is reflected along the vertical axis
// before the sword is spawned, and reflected back afterwards.
#define YUMEKO_SWORD_FAN_MIRROR() \
    if(yumeko_fan_mirrored != YUMEKO_FAN_NORMAL_SIDE) { \
        sword_template.angle = 0x80 - sword_template.angle; \
    }

// Yumeko bounces off the edges of this inclusive rectangle.
#define YM_BOUNCE_LEFT_PX 48
#define YM_BOUNCE_RIGHT_PX 336
#define YM_BOUNCE_TOP_PX 48
#define YM_BOUNCE_BOTTOM_PX 128

// Flies into a random direction at the given speed, bouncing off the edges of
// the rectangle above. Returns true once [end_frame] has been reached.
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
    if((boss.pos.cur.x.v <= to_sp(YM_BOUNCE_LEFT_PX)) || (boss.pos.cur.x.v >= to_sp(YM_BOUNCE_RIGHT_PX))) {
        boss.pos.velocity.x.v *= -1;
    }
    if((boss.pos.cur.y.v <= to_sp(YM_BOUNCE_TOP_PX)) || (boss.pos.cur.y.v >= to_sp(YM_BOUNCE_BOTTOM_PX))) {
        boss.pos.velocity.y.v *= -1;
    }
    if(boss.phase_frame >= end_frame) {
        boss.sprite = YUMEKO_SPRITE_STILL;
        return true;
    }
    return false;
}

// A fan of swords on a 48-pixel circle, sweeping from angle 0x70 down to 0x0C
// on a randomly picked side.
void near yumeko_pattern_sword_fan(void)
{
    if(boss.phase_frame == 16) {
        boss.sprite = YUMEKO_SPRITE_CHARGE;
        sword_template.twirl_time = 48;
        sword_template.speed.v = (5 * 16);
        sword_template.angle = 0x70;
        yumeko_fan_mirrored = randring2_next16_and(1);
        return;
    }
    if((boss.phase_frame > 32) && ((boss.phase_frame % 2) == 0)) {
        YUMEKO_SWORD_FAN_MIRROR();
        vector2_at(sword_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), sword_template.angle);
        swords_add();
        YUMEKO_SWORD_FAN_MIRROR();
        sword_template.angle -= 6;
        if(sword_template.angle <= 0x0C) {
            YUMEKO_PATTERNS_ENTER_REPOSITION();
        }
    }
}

// 16-way rings of red balls, fired every 4 frames into a random direction
// from a random point within 32 pixels of Yumeko.
void near yumeko_pattern_red_ring(void)
{
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 7, 6);
        if(boss.phase_frame == 16) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_CLOUD_BACKWARDS | YUMEKO_NO_DECELERATE;
            bullet_template.patnum = YUMEKO_BALL_RED;
            bullet_template.group = BG_RING;
            bullet_template.speed.v = (3 * 16 + 12);
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
        YUMEKO_PATTERNS_ENTER_REPOSITION();
    }
}

#undef YM_BOUNCE_BOTTOM_PX
#undef YM_BOUNCE_TOP_PX
#undef YM_BOUNCE_RIGHT_PX
#undef YM_BOUNCE_LEFT_PX
#undef YUMEKO_SWORD_FAN_MIRROR
#undef YUMEKO_PATTERNS_ENTER_REPOSITION
