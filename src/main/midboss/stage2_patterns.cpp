// Natural TH05 stage-two movement and attack behavior. Pinned ReC98
// b6ba5b0a TH05 disassembly is evidence; no acceptance transfers from TH04.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/midboss/stage2_patterns.hpp"
#pragma codeseg B4_UPDATE_TEXT main_03

#define midboss2_orbit_speed boss_statebyte[14]
#define midboss2_orbit_contracting boss_statebyte[15]

void near midboss2_move(void)
{
    midboss.pos.prev = midboss.pos.cur;
    vector2_at(midboss.pos.cur, midboss2_orbit_center.x.v,
        midboss2_orbit_center.y.v, midboss.pos.velocity.x.v, midboss.angle);
    midboss2_orbit_center.x.v += static_cast<signed char>(midboss2_orbit_speed);
    if(midboss2_orbit_center.x.v < to_sp(128)) {
        midboss2_orbit_speed += 2;
    } else if(midboss2_orbit_center.x.v > to_sp(256)) {
        midboss2_orbit_speed -= 2;
    }
    if(midboss2_orbit_contracting == 0) {
        midboss.pos.velocity.x.v += to_sp(1);
        if(midboss.pos.velocity.x.v > to_sp(64)) {
            midboss2_orbit_contracting = 1;
        }
    } else {
        midboss.pos.velocity.x.v -= to_sp(1);
        if(midboss.pos.velocity.x.v <= to_sp(1)) {
            midboss2_orbit_contracting = 0;
        }
    }
    midboss.angle -= 2;
}

void near midboss2_pattern(void)
{
    if(stage_frame_mod16 == 0) {
        bullet_template.spawn_type = 0x10; // No deceleration.
        bullet_template.patnum = 48; // Red ball.
        bullet_template.group = BG_STACK;
        reinterpret_cast<uint16_t &>(bullet_template.stack) = (3 | (8 << 8));
        bullet_template.speed.v = 24;
        bullet_template.angle = randring2_next16();
        bullet_template_tune();
        bullets_add_regular();

        bullet_template.spawn_type = 0x12; // Forward cloud, no deceleration.
        bullet_template.patnum = 0;
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.spread = 3;
        if(midboss.hp <= 600) {
            bullet_template.spread = 6;
        } else if(midboss.hp <= 800) {
            bullet_template.spread = 4;
        }
        bullet_template.speed.v = 24;
        bullet_template.angle = randring2_next16();
        bullet_template_tune();
        bullets_add_regular();
    }
}

void near midboss2_pattern_final(void)
{
    if(stage_frame_mod4 == 0) {
        bullet_template.spawn_type = 0x10; // No deceleration.
        bullet_template.patnum = 44; // Blue ball.
        bullet_template.group = BG_STACK;
        reinterpret_cast<uint16_t &>(bullet_template.stack) = (3 | (15 << 8));
        bullet_template.speed.v = 24;
        bullet_template.angle = randring2_next16();
        bullet_template_tune();
        bullets_add_regular();
    }
}
