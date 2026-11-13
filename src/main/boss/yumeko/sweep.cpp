// Natural sword sweep and accelerating aimed volleys, original TH05 behavior.
// ReC98 b6ba5b0a disassembly supports semantics; no instruction body is copied.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/sweep.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#include "src/main/boss/yumeko/sweep_combat_rules.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_sweep_spacing yumeko_pattern_scratch.pattern_byte15.sweep_spacing
#define yumeko_sweep_side boss_statebyte[14]
#define yumeko_sweep_round boss_statebyte[13]

void near yumeko_pattern_sword_sweep(void)
{
    if(boss.phase_frame < YSW_CHARGE_END_FRAME) {
        gather_add_only_3stack(boss.phase_frame - YSW_GATHER_LEAD_FRAMES, YSW_GATHER_COLOR_FIRST, YSW_GATHER_COLOR_SECOND);
        if(boss.phase_frame == YSW_CHARGE_SOUND_FRAME) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = YUMEKO_NO_DECELERATE;
            bullet_template.patnum = YSW_BULLET_PATNUM; // Blue directional bullet.
            bullet_template.group = BG_SPREAD;
            bullet_template.spread = YSW_VOLLEY_COUNT;
            bullet_template.spread_angle_delta = select_for_rank(YSW_EASY_ANGLE_STEP, YSW_NORMAL_ANGLE_STEP, YSW_HARD_ANGLE_STEP, YSW_LUNATIC_ANGLE_STEP);
            bullet_template.speed.v = YSW_BLUE_SPEED_SUBPX;
            snd_se_play(YSW_CHARGE_SOUND);
            sword_template.twirl_time = YSW_SWORD_TWIRL_TIME;
            sword_template.speed.v = YSW_SWORD_SPEED_SUBPX;
            boss2.pos.cur.y.v = randring2_next16_mod(to_sp(YSW_FIRST_Y_JITTER_PX));
            yumeko_sweep_spacing = select_for_rank(YSW_EASY_SWORD_SPACING_PX, YSW_NORMAL_SWORD_SPACING_PX, YSW_HARD_SWORD_SPACING_PX, YSW_LUNATIC_SWORD_SPACING_PX);
            yumeko_sweep_side = YSW_FIRST_SIDE;
            yumeko_sweep_round = YSW_FIRST_ROUND;
        }
        return;
    }
    if(yumeko_sweep_round == YSW_FIRST_ROUND) {
        if((boss.phase_frame % YSW_SWORD_VOLLEY_INTERVAL) == 0) {
            sword_template.angle = yumeko_sweep_side;
            if(yumeko_sweep_side == YSW_FIRST_SIDE) {
                sword_template.origin.x.v = to_sp(YSW_LEFT_SWORD_ORIGIN_PX);
            } else {
                sword_template.origin.x.v = to_sp(PLAYFIELD_W - YSW_RIGHT_SWORD_MARGIN_PX);
            }
            sword_template.origin.y = boss2.pos.cur.y;
            swords_add();
            boss2.pos.cur.y.v += (yumeko_sweep_spacing << YSW_SUBPIXEL_SHIFT);
            yumeko_sweep_side += YSW_OTHER_SIDE_ANGLE;
            if(boss2.pos.cur.y.v >= to_sp(YSW_SWEEP_Y_LIMIT_PX)) {
                boss2.pos.cur.y.v = randring2_next16_mod(to_sp(YSW_FIRST_Y_JITTER_PX));
                yumeko_sweep_round++;
            }
        }
    } else if((boss.phase_frame % YSW_AIMED_VOLLEY_INTERVAL) == 0) {
        if(bullet_template.speed.v > YSW_BURST_RECYCLE_THRESHOLD_SUBPX) {
            bullet_template.speed.v = YSW_BURST_RESTART_SPEED_SUBPX;
            snd_se_play(YSW_BURST_START_SOUND);
            yumeko_sweep_round++;
            if(yumeko_sweep_round > YSW_BURST_ROUND_LIMIT) {
                yumeko_sweep_round = YSW_FIRST_ROUND;
                return;
            }
            bullet_template.angle = player_angle_from(
                bullet_template.origin.x, bullet_template.origin.y, 0);
        }
        bullet_template.speed.v += YSW_BURST_ACCEL_PER_VOLLEY_SUBPX;
        bullets_add_regular();
    }
}
