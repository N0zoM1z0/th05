// Natural sword sweep and accelerating aimed volleys, original TH05 behavior.
// ReC98 b6ba5b0a disassembly supports semantics; no instruction body is copied.
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#include "src/main/boss/yumeko/sweep.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_sweep_spacing boss_statebyte[15]
#define yumeko_sweep_side boss_statebyte[14]
#define yumeko_sweep_round boss_statebyte[13]

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
            bullet_template.speed.v = 8 * 16;
            snd_se_play(8);
            sword_template.twirl_time = 32;
            sword_template.speed.v = 4 * 16;
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
        if(bullet_template.speed.v > 6 * 16) {
            bullet_template.speed.v = 8;
            snd_se_play(15);
            yumeko_sweep_round++;
            if(yumeko_sweep_round > 5) {
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
