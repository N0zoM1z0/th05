// Yumeko's sword sweep: swords flying across the playfield from alternating
// edges, followed by accelerating aimed bullet bursts.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/sweep.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_sweep_spacing yumeko_boss_scratch.sweep.pattern_byte15.sweep_spacing
#define yumeko_sweep_side yumeko_boss_scratch.sweep.pattern_byte14.sweep_side
#define yumeko_sweep_round yumeko_boss_scratch.sweep.pattern_byte13.sweep_round

// Aimed bursts restart at speed 8 once the bullet speed exceeds this value.
#define YSW_BURST_RECYCLE_THRESHOLD_SUBPX (6 * 16)

// One cycle of this attack consists of a sword sweep (round 0) and five
// aimed bullet bursts (rounds 1-5). A sweep spawns a horizontally flying sword
// every 8 frames, alternating between the left and right playfield edge and
// moving down by a rank-dependent spacing each time, until it reaches Y = 376. Each burst then
// fires a bullet every 4 frames, accelerating it by 8 subpixels per bullet
// from 16 to 104.
//
// ZUN quirk: Neither the side, the bullet speed nor the aimed angle are reset
// between cycles. The first cycle's first bullet therefore starts a burst
// immediately (the speed is still 128 from the charge), and only fires 4
// bursts; later cycles fire their first burst at the previous angle without
// a sound.
void near yumeko_pattern_sword_sweep(void)
{
    if(boss.phase_frame < 32) {
        gather_add_only_3stack(boss.phase_frame - 16, 7, 6);
        if(boss.phase_frame == 16) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_NO_DECELERATE;
            bullet_template.patnum = 52; // Blue directional bullet.
            bullet_template.group = BG_SPREAD;
            bullet_template.spread = 5;
            bullet_template.spread_angle_delta = select_for_rank(24, 16, 12, 10);
            bullet_template.speed.v = (8 * 16);
            snd_se_play(8);
            sword_template.twirl_time = 32;
            sword_template.speed.v = (4 * 16);
            boss2.pos.cur.y.v = randring2_next16_mod(to_sp(32));
            yumeko_sweep_spacing = select_for_rank(40, 30, 24, 16);
            yumeko_sweep_side = 0;
            yumeko_sweep_round = 0;
        }
        return;
    }
    if(yumeko_sweep_round == 0) {
        if((boss.phase_frame % 8) == 0) {
            sword_template.angle = yumeko_sweep_side;
            if(yumeko_sweep_side == 0) {
                sword_template.origin.x.v = to_sp(16);
            } else {
                sword_template.origin.x.v = to_sp(PLAYFIELD_W - 16);
            }
            sword_template.origin.y = boss2.pos.cur.y;
            swords_add();
            boss2.pos.cur.y.v += (yumeko_sweep_spacing << 4);
            yumeko_sweep_side += 0x80;
            if(boss2.pos.cur.y.v >= to_sp(376)) {
                boss2.pos.cur.y.v = randring2_next16_mod(to_sp(32));
                yumeko_sweep_round++;
            }
        }
    } else if((boss.phase_frame % 4) == 0) {
        if(bullet_template.speed.v > YSW_BURST_RECYCLE_THRESHOLD_SUBPX) {
            bullet_template.speed.v = 8;
            snd_se_play(15);
            yumeko_sweep_round++;
            if(yumeko_sweep_round > 5) {
                // Back to the sword sweep, without firing or aiming.
                yumeko_sweep_round = 0;
                return;
            }
            bullet_template.angle = player_angle_from(
                bullet_template.origin.x, bullet_template.origin.y, 0);
        }
        bullet_template.speed.v += 8;
        bullets_add_regular();
    }
}

#undef YSW_BURST_RECYCLE_THRESHOLD_SUBPX
