#include "src/main/boss/yumeko/spread_choreography.hpp"
// The two attack families use the same initial sprite, spawn mode and
// spread group setup. The blue counter-rotation additionally sets the
// exact-linear motion before speed, so that remains at its real call site.
#define YUMEKO_SPREAD_CHARGE_START(spread_group) { \
    boss.sprite = YUMEKO_SPRITE_CHARGE; \
    bullet_template.spawn_type = YUMEKO_NO_DECELERATE; \
    bullet_template.group = spread_group; \
}

// Each spread restarts the Boss clock and enters its own next reposition.
#define YUMEKO_SPREAD_REPOSITION() { \
    boss.phase_frame = 0; \
    boss.mode = YSP_REENTER_REPOSITION_MODE; \
}

void near yumeko_pattern_counterrotating_spreads(void)
{
    if(boss.phase_frame < YSP_CHARGE_END_FRAME) {
        gather_add_only_3stack(boss.phase_frame - YSP_GATHER_LEAD_FRAME, YSP_GATHER_COLOR_A, YSP_GATHER_COLOR_B);
        if(boss.phase_frame == YSP_FIRST_CHARGE_FRAME) {
            YUMEKO_SPREAD_CHARGE_START(BG_SPREAD);
            bullet_template.special_motion = BSM_EXACT_LINEAR;
            bullet_template.speed.v = YSP_PROJECTILE_BASE_SPEED_SUBPX;
            reinterpret_cast<uint16_t &>(bullet_template.spread) = (YSP_BLUE_SPREAD_COUNT | (YSP_BLUE_SPREAD_STEP << 8));
            snd_se_play(YSP_CHARGE_SOUND);
            yumeko_angle_a = YSP_OUTER_START_ANGLE;
            yumeko_angle_b = YSP_INNER_START_ANGLE;
        }
        return;
    }
    if((boss.phase_frame % YSP_VOLLEY_INTERVAL) == 0) {
        bullet_template.patnum = YSP_BLUE_PATTERN; // Blue ball.
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(YSP_OUTER_RADIUS_PX), yumeko_angle_a);
        bullet_template.angle = yumeko_angle_a + yumeko_angle_b;
        bullets_add_special();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(YSP_OUTER_RADIUS_PX), static_cast<unsigned char>(yumeko_angle_a + YSP_REFLECTION_ANGLE));
        bullet_template.angle += YSP_REFLECTION_ANGLE;
        bullets_add_special();

        bullet_template.patnum = YSP_PELLET_PATTERN;
        yumeko_angle_a = -yumeko_angle_a;
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(YSP_INNER_RADIUS_PX), yumeko_angle_a);
        bullet_template.angle = yumeko_angle_a - yumeko_angle_b;
        bullets_add_special();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(YSP_INNER_RADIUS_PX), static_cast<unsigned char>(yumeko_angle_a + YSP_REFLECTION_ANGLE));
        bullet_template.angle += YSP_REFLECTION_ANGLE;
        bullets_add_special();
        yumeko_angle_a = -yumeko_angle_a;
        yumeko_angle_a -= YSP_OUTER_ROTATE_STEP;
        yumeko_angle_b -= YSP_INNER_ROTATE_STEP;
        snd_se_play(YSP_FIRE_SOUND);
    }
    if(boss.phase_frame == YSP_COUNTERROTATE_END_FRAME) {
        YUMEKO_SPREAD_REPOSITION();
    }
}

void near yumeko_pattern_mirrored_spreads(void)
{
    if(boss.phase_frame < YSP_CHARGE_END_FRAME) {
        gather_add_only_3stack(boss.phase_frame - YSP_GATHER_LEAD_FRAME, YSP_GATHER_COLOR_A, YSP_GATHER_COLOR_B);
        if(boss.phase_frame == YSP_FIRST_CHARGE_FRAME) {
            YUMEKO_SPREAD_CHARGE_START(BG_SPREAD_AIMED);
            bullet_template.speed.v = YSP_PROJECTILE_BASE_SPEED_SUBPX;
            bullet_template.spread_angle_delta = YSP_MIRROR_SPREAD_DELTA;
            bullet_template.angle = YSP_MIRROR_FIRST_ANGLE;
            bullet_template.patnum = YSP_MIRROR_PATTERN; // Green directional bullet.
            bullet_template_tune();
            snd_se_play(YSP_CHARGE_SOUND);
            yumeko_angle_a = YSP_MIRROR_START_ANGLE;
        }
        return;
    }
    if((boss.phase_frame % YSP_VOLLEY_INTERVAL) == 0) {
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(YSP_OUTER_RADIUS_PX), yumeko_angle_a);
        bullet_template.spread = YSP_MIRROR_FIRST_COUNT;
        bullets_add_regular();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(YSP_OUTER_RADIUS_PX), static_cast<unsigned char>(YSP_REFLECTION_ANGLE - yumeko_angle_a));
        bullet_template.spread = YSP_MIRROR_SECOND_COUNT;
        bullets_add_regular();
        yumeko_angle_a += YSP_MIRROR_ROTATE_STEP;
        snd_se_play(YSP_FIRE_SOUND);
    }
    if(boss.phase_frame == YSP_MIRROR_END_FRAME) {
        YUMEKO_SPREAD_REPOSITION();
    }
}

#undef YUMEKO_SPREAD_REPOSITION
#undef YUMEKO_SPREAD_CHARGE_START
