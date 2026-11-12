// Alice's stationary-puppet beam: charge, contract, animate and fire.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/boss/alice/beam.hpp"
#include "src/main/boss/alice/beam_phase.hpp"
#include "src/main/boss/alice/beam_weapon_rules.hpp"
#include "src/main/boss/alice/scratch.hpp"

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
    if(alice_beam_frame < ALICE_BEAM_CHARGE_START) {
        return;
    }
    if(alice_beam_frame == ALICE_BEAM_CHARGE_START) {
        alice_scratch.beam_phase = ALICE_BEAM_CHARGE_CIRCLES;
        alice_puppet0.radius.radius_gather = alice_puppet1.radius.radius_gather = ABW_GATHER_RADIUS_INITIAL;
        alice_scratch.beam_sprite_patnum = ABW_SPRITE_OFFSET_INITIAL;
        alice_beam_burst_window += ABW_WINDOW_EXTENSION;
        return;
    }
    if(alice_beam_frame < ALICE_BEAM_CONTRACT_START) {
        return;
    }
    if(alice_beam_frame < ALICE_BEAM_SPRITES_START) {
        alice_scratch.beam_phase = ALICE_BEAM_CONTRACTING;
        alice_puppet0.radius.radius_gather = alice_puppet1.radius.radius_gather =
            ((ABW_GATHER_RADIUS_INITIAL - alice_beam_frame) * ABW_GATHER_CONTRACTION);
        return;
    }
    if(alice_beam_frame < ALICE_BEAM_FIRE_START) {
        if(alice_beam_frame == ALICE_BEAM_SPRITES_START) {
            snd_se_play(ABW_BEAM_SPRITE_SE);
        }
        alice_scratch.beam_phase = ALICE_BEAM_SPRITES;
        if(alice_beam_frame == ABW_SPRITE_FRAME_FIRST || alice_beam_frame == ABW_SPRITE_FRAME_SECOND) {
            alice_scratch.beam_sprite_patnum += ABW_SPRITE_STEP;
        }
        return;
    }

    bullet_template.spawn_type = (ABW_CLOUD_FORWARD_FLAG | ABW_NO_DECELERATION_FLAG); // Forward cloud, no deceleration.
    bullet_template.patnum = ABW_LASER_BULLET_PATNUM;
    bullet_template.speed.v = ABW_LASER_BULLET_SPEED_SUBPX;
    bullet_template.group = BG_SINGLE;
    bullet_template_tune();

    shot_hitbox_radius.x.v = to_sp(ABW_LASER_SHOT_RADIUS_X_PX);
    shot_hitbox_radius.y.v = to_sp(ABW_LASER_SHOT_RADIUS_Y_PX);
    shot_hitbox_center = alice_puppet0.pos.cur;
    shot_hitbox_center.x.v += to_sp(ABW_BEAM_CENTER_OFFSET_PX);
    damage = shots_hittest_laser();
    if(damage != 0) {
        snd_se_play(ABW_LASER_HIT_SE);
    }

    // Inclusive left edge, exclusive right/bottom edges, with16-bit unsigned
    // wraparound retaining the original behavior outside the horizontal beam.
    if(static_cast<unsigned int>(player_pos.cur.x.v - alice_puppet0.pos.cur.x.v) < to_sp(ABW_PLAYER_HIT_WIDTH_PX) &&
        static_cast<unsigned int>(alice_puppet0.pos.cur.y.v - player_pos.cur.y.v  + to_sp(ABW_PLAYER_HIT_Y_LEAD_PX)) < to_sp(ABW_PLAYER_HIT_HEIGHT_PX)) {
        player_is_hit = true;
    }

    if((boss.phase_frame % ABW_BURST_INTERVAL_FRAMES) == 0 &&
        (boss.phase_frame % ABW_BURST_PERIOD_FRAMES) < alice_beam_burst_window) {
        bullet_template.patnum = ABW_AIMED_BULLET_PATNUM; // Blue round bullet.
        bullet_template.group = BG_STACK_AIMED;
        bullet_template.angle = 0;
        bullet_template.origin.x = boss.pos.cur.x;
        bullet_template.origin.y.v = boss.pos.cur.y.v + to_sp(ABW_AIMED_BULLET_BOSS_Y_OFFSET_PX);
        // Real adjacent semantic fields: eight bullets and six speed units.
        reinterpret_cast<uint16_t &>(bullet_template.stack) = ABW_AIMED_BULLET_COUNT | (ABW_AIMED_BULLET_SPEED_STEP << 8);
        bullet_template.speed.v = to_sp(ABW_AIMED_BULLET_SPEED_PX);
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(ABW_AIMED_BULLET_SE);
    }
}
