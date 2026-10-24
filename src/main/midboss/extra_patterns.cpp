// Natural TH05 Extra movement and attack semantics, independently recovered
// from the original target; ReC98 b6ba5b0a disassembly is behavior evidence.
#pragma option -zCMIDBOSSX_TEXT -zPmain_03
#include "src/main/midboss/extra_patterns.hpp"
#pragma codeseg MIDBOSSX_TEXT main_03

#define midbossx_ring_rotation boss_statebyte[13]

bool pascal near midbossx_dash_update(int frame)
{
    if(frame >= -8) {
        if(frame < 0) {
            midboss.sprite = 221;
        } else if(frame < 30) {
            if(frame == 0) {
                snd_se_play(8);
            }
            frame *= 2;
            vector2_near(midboss.pos.velocity, midboss.angle, to_sp(4) - frame);
            midboss.pos.update_seg3();
            midboss.sprite = ((frame < 16) | (frame > 48)) ? 222 : 223;
        } else if(frame < 40) {
            if(frame == 30) {
                snd_se_play(15);
            }
            midboss.pos.prev = midboss.pos.cur;
            midboss.sprite = 221;
            midbossx_pattern();
        } else {
            midboss.sprite = 220;
            return midbossx_pattern();
        }
    }
    return false;
}

bool near midbossx_pattern_wait(void)
{
    if(midboss.phase_frame >= 112) {
        return true;
    }
    return false;
}

bool near midbossx_pattern_spread(void)
{
    if(midboss.phase_frame == 94) {
        midbossx_ring_rotation = randring2_next16_and(1) ? 1 : -1;
    }
    if(midboss.phase_frame <= 114) {
        bullet_template.spawn_type = 0x10; // No deceleration.
        bullet_special.speed_delta.v = 2;
        bullet_template.special_motion = BSM_SPEEDUP;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = (18 | (16 << 8));
        bullet_template.group = BG_RING;
        bullet_template.speed.v = 8;
        bullet_template.patnum = 47;
        bullet_template.angle += midbossx_ring_rotation;
        bullets_add_special();
    }
    if(midboss.phase_frame >= 128) {
        return true;
    }
    return false;
}

bool near midbossx_pattern_random(void)
{
    if(page_back != 0) {
        bullet_template.spawn_type = 0x12; // Forward cloud, no deceleration.
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.speed.v = 16;
        reinterpret_cast<uint16_t &>(bullet_template.spread) = (12 | (10 << 8));
        bullet_template.patnum = 0;
        bullets_add_regular();
    }
    if(midboss.phase_frame >= 128) {
        return true;
    }
    return false;
}

bool near midbossx_pattern_decelerate(void)
{
    if((midboss.phase_frame % 16) == 0) {
        bullet_template.spawn_type = 0x13; // Backward cloud, no deceleration.
        bullet_special.turns_max = 1;
        bullet_template.special_motion = BSM_DECELERATE_THEN_TURN;
        bullet_template.group = BG_SPREAD_STACK;
        reinterpret_cast<uint32_t &>(bullet_template.spread) =
            (5UL | (8UL << 8) | (4UL << 16) | (16UL << 24));
        bullet_template.speed.v = 24;
        bullet_template.patnum = 47;
        bullet_template.angle = 0x80;
        bullet_template_special_angle.turn_by = -0x38;
        bullets_add_special();
        bullet_template.angle = 0;
        bullet_template_special_angle.turn_by = 0x38;
        bullets_add_special();
        snd_se_play(3);
    }
    if(midboss.phase_frame >= 128) {
        return true;
    }
    return false;
}
