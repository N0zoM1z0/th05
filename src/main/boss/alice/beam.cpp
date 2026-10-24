// Alice's stationary-puppet beam: charge, contract, animate and fire.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/boss/alice/beam.hpp"

void near alice_puppet_beam_pattern(void)
{
    int damage;

    // The full four-byte coordinates have no padding. Compare the complete
    // position storage so movement of either component delays beam charging.
    if(reinterpret_cast<const uint32_t &>(alice_puppet0.pos.cur) !=
        reinterpret_cast<const uint32_t &>(alice_puppet0.pos.prev) ||
        reinterpret_cast<const uint32_t &>(alice_puppet1.pos.cur) !=
        reinterpret_cast<const uint32_t &>(alice_puppet1.pos.prev)) {
        return;
    }
    alice_beam_frame++;
    if(alice_beam_frame < 16) {
        return;
    }
    if(alice_beam_frame == 16) {
        boss_statebyte[9] = 1;
        alice_puppet0.radius.radius_gather = alice_puppet1.radius.radius_gather = 64;
        boss_statebyte[8] = -60;
        alice_beam_burst_window += 32;
        return;
    }
    if(alice_beam_frame < 32) {
        return;
    }
    if(alice_beam_frame < 64) {
        boss_statebyte[9] = 2;
        alice_puppet0.radius.radius_gather = alice_puppet1.radius.radius_gather =
            ((64 - alice_beam_frame) * 2);
        return;
    }
    if(alice_beam_frame < 80) {
        if(alice_beam_frame == 64) {
            snd_se_play(8);
        }
        boss_statebyte[9] = 3;
        if(alice_beam_frame == 71 || alice_beam_frame == 79) {
            boss_statebyte[8] += 2;
        }
        return;
    }

    bullet_template.spawn_type = 0x02 | 0x10; // Forward cloud, no deceleration.
    bullet_template.patnum = 0;
    bullet_template.speed.v = to_sp(1) + 8;
    bullet_template.group = BG_SINGLE;
    bullet_template_tune();

    shot_hitbox_radius.x.v = to_sp(56);
    shot_hitbox_radius.y.v = to_sp(8);
    shot_hitbox_center = alice_puppet0.pos.cur;
    shot_hitbox_center.x.v += to_sp(64);
    damage = shots_hittest_laser();
    if(damage != 0) {
        snd_se_play(9);
    }

    // Inclusive left edge, exclusive right/bottom edges, with16-bit unsigned
    // wraparound retaining the original behavior outside the horizontal beam.
    if(static_cast<unsigned int>(player_pos.cur.x.v - alice_puppet0.pos.cur.x.v) < to_sp(128) &&
        static_cast<unsigned int>(alice_puppet0.pos.cur.y.v - player_pos.cur.y.v + to_sp(4)) < to_sp(8)) {
        player_is_hit = true;
    }

    if((boss.phase_frame % 16) == 0 &&
        (boss.phase_frame % 256) < alice_beam_burst_window) {
        bullet_template.patnum = 44; // Blue round bullet.
        bullet_template.group = BG_STACK_AIMED;
        bullet_template.angle = 0;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(-8);
        // Real adjacent semantic fields: eight bullets and six speed units.
        reinterpret_cast<uint16_t &>(bullet_template.stack) = 8 | (6 << 8);
        bullet_template.speed.v = to_sp(2);
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(3);
    }
}
