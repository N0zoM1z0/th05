// Complete mixed aimed volleys, laser shootouts and twirling swords.
#ifndef TH05_YUMEKO_COMBINED_CONTEXT
#pragma option -zCB5_UPDATE_TEXT -zPmain_03
#endif
#include "src/main/boss/yumeko/laser_swords.hpp"
#include "src/main/boss/yumeko/final_ring_scratch.hpp"
#include "src/main/boss/yumeko/laser_swords_timing.hpp"
#pragma codeseg B5_UPDATE_TEXT main_03

#define yumeko_laser_interval boss_statebyte[1]
#define yumeko_volley_frames boss_statebyte[12]
#define yumeko_laser_fast boss_statebyte[13]
#define yumeko_angle_b boss_statebyte[14]
#define yumeko_angle_a yumeko_pattern_scratch.pattern_byte15.sword_pattern_angle_a

void near yumeko_pattern_laser_swords(void)
{
    unsigned char angle;
    int i;
    int frame;
    if(boss.phase_frame < YLS_CHARGE_FRAMES) {
        gather_add_only_3stack(boss.phase_frame - YLS_CHARGE_SOUND_FRAME, YLS_CHARGE_GATHER_COLOR, YLS_CHARGE_GATHER_OTHER_COLOR);
        if(boss.phase_frame == YLS_CHARGE_SOUND_FRAME) {
            boss.sprite = YUMEKO_SPRITE_CHARGE;
            bullet_template.spawn_type = (YLS_BULLET_CLOUD_FORWARD | YUMEKO_NO_DECELERATE);
            bullet_template.patnum = YLS_BULLET_PATNUM;
            bullet_template.group = BG_SINGLE;
            bullet_template.speed.v = YLS_INITIAL_BULLET_SPEED;
            bullet_template_tune();
            snd_se_play(YLS_CHARGE_SE);
            laser_template.age = YLS_LASER_INITIAL_AGE;
            laser_template.shootout_speed.v = YLS_LASER_SHOOTOUT_SPEED;
            laser_template.coords.width.nonshrink = YLS_LASER_WIDTH;
            laser_template.col = YLS_LASER_COLOR;
            laser_template.active_at_age.grow = YLS_LASER_GROW_AGE;
            yumeko_laser_fast = YLS_UNACCELERATED;
            yumeko_volley_frames = YLS_START_VOLLEY_FRAMES;
            sword_template.twirl_time = YLS_START_SWORD_TWIRL;
            sword_template.speed.v = YLS_START_SWORD_SPEED;
        }
        return;
    }
    frame = boss.phase_frame % YLS_VOLLEY_REPEAT_FRAMES;
    if(frame < yumeko_volley_frames && (frame & YLS_VOLLEY_EVERY_OTHER) == 0) {
        bullet_template.origin.x.v -= to_sp(YLS_VOLLEY_LEFT_OFFSET_PX);
        bullet_template.origin.y.v -= to_sp(YLS_VOLLEY_Y_OFFSET_PX);
        if(frame == 0) {
            yumeko_angle_a = player_angle_from(
                bullet_template.origin.x, bullet_template.origin.y, 0);
            yumeko_angle_b = yumeko_angle_from_xy(
                bullet_template.origin.x.v + to_sp(64), bullet_template.origin.y.v, 0);
        }
        bullet_template.angle = yumeko_angle_a;
        bullets_add_regular();
        bullet_template.origin.x.v += to_sp(YLS_VOLLEY_PAIR_SPACING_PX);
        bullet_template.angle = yumeko_angle_b;
        bullets_add_regular();
        snd_se_play(YLS_VOLLEY_SHOT_SE);
    }
    if((boss.phase_frame % yumeko_laser_interval) == 0) {
        laser_template.coords.origin.y.v = to_sp(YLS_LASER_ORIGIN_Y_PX);
        laser_template.coords.origin.x.v = randring2_next16_mod(to_sp(YLS_LASER_RANDOM_X_PX)) + to_sp(YLS_LASER_MIN_X_PX);
        laser_template.coords.angle = player_angle_from(
            laser_template.coords.origin.x, laser_template.coords.origin.y, 0);
        lasers_shootout_add();
        for(i = 0; i < YLS_SWORDS_PER_VOLLEY; i++) {
            angle = randring2_next16_and(YLS_SWORD_AIM_JITTER_MASK) - YLS_SWORD_AIM_JITTER_CENTER;
            sword_template.origin.y.v = randring2_next16_mod(to_sp(YLS_SWORD_RANDOM_Y_PX));
            sword_template.origin.x.v = randring2_next16_mod(to_sp(YLS_SWORD_RANDOM_X_PX)) + to_sp(YLS_SWORD_MIN_X_PX);
            sword_template.angle = player_angle_from(
                sword_template.origin.x, sword_template.origin.y, angle);
            swords_add();
        }
    }
    if(boss.hp - boss.phase_end_hp < YLS_NEAR_HP_GATE && yumeko_laser_fast == YLS_UNACCELERATED) {
        yumeko_laser_fast = YLS_ACCELERATED;
        yumeko_laser_interval = select_for_rank(YLS_LASER_EASY, YLS_LASER_NORMAL, YLS_LASER_HARD, YLS_LASER_LUNATIC);
        yumeko_volley_frames = select_for_rank(YLS_VOLLEY_EASY, YLS_VOLLEY_NORMAL, YLS_VOLLEY_HARD, YLS_VOLLEY_LUNATIC);
        boss_explode_small(ET_CIRCLE);
        if(bullet_clear_time < YLS_BULLET_CLEAR_MIN_FRAMES) {
            bullet_clear_time = YLS_BULLET_CLEAR_MIN_FRAMES;
        }
    }
}
