// Yumeko's two spread attacks from the second mobile wave. Both charge for
// 16 frames, then fire a volley every 8 frames from points on a circle around
// Yumeko, whose angles rotate between volleys.

// Both attacks share the same charge sprite, spawn type and spread group
// setup. The counterrotating one additionally sets its special motion right
// after this, before the speed.
#define YUMEKO_SPREAD_CHARGE_START(spread_group) { \
    boss.sprite = YUMEKO_SPRITE_CHARGE; \
    bullet_template.spawn_type = YUMEKO_NO_DECELERATE; \
    bullet_template.group = spread_group; \
}

// Restart the phase clock and fly to the next position.
#define YUMEKO_SPREAD_REPOSITION() { \
    boss.phase_frame = 0; \
    boss.mode = 0; \
}

// Last frame of the counterrotating spreads.
#define YSP_COUNTERROTATE_END_FRAME 256

// Two pairs of point-symmetric spreads: blue balls from a 48-pixel circle and
// pellets from a 32-pixel circle, with the pellet circle mirrored and both
// circles rotating in opposite directions.
void near yumeko_pattern_counterrotating_spreads(void)
{
    if(boss.phase_frame < 16) {
        gather_add_only_3stack(boss.phase_frame - 1, 7, 6);
        if(boss.phase_frame == 4) {
            YUMEKO_SPREAD_CHARGE_START(BG_SPREAD);
            bullet_template.special_motion = BSM_EXACT_LINEAR;
            bullet_template.speed.v = (3 * 16 + 8);
            // Writes [spread] = 5 and the adjacent [spread_angle_delta] = 2
            // with a single word store.
            reinterpret_cast<uint16_t &>(bullet_template.spread) = (5 | (2 << 8));
            snd_se_play(8);
            yumeko_angle_a = 0x60;
            yumeko_angle_b = 0x40;
        }
        return;
    }
    if((boss.phase_frame % 8) == 0) {
        bullet_template.patnum = 44; // Blue ball.
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), yumeko_angle_a);
        bullet_template.angle = yumeko_angle_a + yumeko_angle_b;
        bullets_add_special();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), static_cast<unsigned char>(yumeko_angle_a + 0x80));
        bullet_template.angle += 0x80;
        bullets_add_special();

        bullet_template.patnum = 0; // Pellet.
        yumeko_angle_a = -yumeko_angle_a;
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(32), yumeko_angle_a);
        bullet_template.angle = yumeko_angle_a - yumeko_angle_b;
        bullets_add_special();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(32), static_cast<unsigned char>(yumeko_angle_a + 0x80));
        bullet_template.angle += 0x80;
        bullets_add_special();
        yumeko_angle_a = -yumeko_angle_a;
        yumeko_angle_a -= 8;
        yumeko_angle_b -= 6;
        snd_se_play(3);
    }
    if(boss.phase_frame == YSP_COUNTERROTATE_END_FRAME) {
        YUMEKO_SPREAD_REPOSITION();
    }
}

#undef YSP_COUNTERROTATE_END_FRAME

// Aimed 5- and 4-way spreads of green bullets, fired from two points on a
// 48-pixel circle that are mirrored along Yumeko's vertical axis.
void near yumeko_pattern_mirrored_spreads(void)
{
    if(boss.phase_frame < 16) {
        gather_add_only_3stack(boss.phase_frame - 1, 7, 6);
        if(boss.phase_frame == 4) {
            YUMEKO_SPREAD_CHARGE_START(BG_SPREAD_AIMED);
            bullet_template.speed.v = (3 * 16 + 8);
            bullet_template.spread_angle_delta = 20;
            bullet_template.angle = 0;
            bullet_template.patnum = 68; // Green directional bullet.
            bullet_template_tune();
            snd_se_play(8);
            yumeko_angle_a = 0x80;
        }
        return;
    }
    if((boss.phase_frame % 8) == 0) {
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), yumeko_angle_a);
        bullet_template.spread = 5;
        bullets_add_regular();
        vector2_at(bullet_template.origin, boss.pos.cur.x.v, boss.pos.cur.y.v,
            to_sp(48), static_cast<unsigned char>(0x80 - yumeko_angle_a));
        bullet_template.spread = 4;
        bullets_add_regular();
        yumeko_angle_a += 8;
        snd_se_play(3);
    }
    if(boss.phase_frame == 192) {
        YUMEKO_SPREAD_REPOSITION();
    }
}

#undef YUMEKO_SPREAD_REPOSITION
#undef YUMEKO_SPREAD_CHARGE_START
