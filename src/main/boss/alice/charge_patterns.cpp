// Three consecutive natural Alice charge/fire patterns, after the puppet beam.
#pragma option -zCALICE_CHG_TEXT -zPmain_03
#include "src/main/boss/alice/charge_patterns.hpp"

void near alice_pattern_laser_fan(void)
{
    if(boss.phase_frame < 64) {
        gather_add_only_3stack(boss.phase_frame - 40, 9, 8);
        boss.sprite = 184;
        if(boss.phase_frame == 40) {
            snd_se_play(8);
        }
        return;
    }
    if(boss.phase_frame == 64) {
        laser_template.col = 6;
        laser_template.coords.width.nonshrink = 8;
        laser_template.coords.origin = bullet_template.origin;
        laser_template.active_at_age.moveout = 40;
        laser_template.shootout_speed.v = to_sp(5);
        laser_template.coords.angle = iatan2(
            player_pos.cur.y.v - laser_template.coords.origin.y.v,
            player_pos.cur.x.v - laser_template.coords.origin.x.v);
        lasers_shootout_add();
        laser_template.coords.angle += 16;
        lasers_shootout_add();
        laser_template.coords.angle -= 32;
        lasers_shootout_add();

        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.patnum = 44;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = 20 | (8 << 8);
        bullet_template.speed.v = to_sp(1) + 8;
        bullet_template.angle = 0;
        bullet_template_tune();
        bullets_add_regular();
        boss.sprite = 180;
        return;
    }
    if(boss.phase_frame == 96) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}

void near alice_pattern_paired_stacks(void)
{
    if(boss.phase_frame < 64) {
        gather_add_only_3stack(boss.phase_frame - 40, 9, 8);
        boss.sprite = 184;
        boss_statebyte[15] = 8;
        if(boss.phase_frame == 40) {
            snd_se_play(8);
        }
        return;
    }
    if((boss.phase_frame % 4) == 0) {
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_STACK_AIMED;
        bullet_template.patnum = 44;
        reinterpret_cast<uint16_t &>(bullet_template.stack) = 8 | (7 << 8);
        bullet_template.speed.v = to_sp(1) + 8;
        bullet_template_tune();
        bullet_template.angle = boss_statebyte[15];
        bullets_add_regular();
        bullet_template.angle = -bullet_template.angle;
        bullets_add_regular();
        boss_statebyte[15] += 5;
        boss.sprite = 180;
        snd_se_play(15);
    }
    if(boss.phase_frame == 96) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}

void near alice_pattern_rotating_ring(void)
{
    if(boss.phase_frame < 64) {
        gather_add_only_3stack(boss.phase_frame - 40, 9, 8);
        boss.sprite = 184;
        boss_statebyte[15] = 0;
        if(boss.phase_frame == 40) {
            snd_se_play(8);
        }
        return;
    }
    if((boss.phase_frame % 4) == 0) {
        bullet_template.spawn_type = 0x02 | 0x10;
        bullet_template.group = BG_RING;
        bullet_template.patnum = 48;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = 20 | (7 << 8);
        bullet_template.speed.v = to_sp(2) + 8;
        bullet_template_tune();
        bullet_template.angle = boss_statebyte[15];
        bullets_add_regular();
        boss_statebyte[15] += 2;
        boss.sprite = 180;
        snd_se_play(3);
    }
    if(boss.phase_frame == 96) {
        boss.phase_frame = 0;
        boss.mode = 0;
    }
}
