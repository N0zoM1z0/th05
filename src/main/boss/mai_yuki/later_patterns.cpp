// Eleven complete natural attack functions before the real Mai/Yuki update.
#include "src/main/boss/mai_yuki/later_patterns.hpp"

bool near mai_pattern_tracking_laser(void)
{
    signed char angle_delta;
    if(boss.phase_frame == 48) {
        laser_template.coords.origin = boss.pos.cur;
        laser_template.coords.angle = iatan2(
            player_pos.cur.y.v - laser_template.coords.origin.y.v,
            player_pos.cur.x.v - laser_template.coords.origin.x.v);
        laser_template.col = 8;
        laser_template.coords.width.nonshrink = 8;
        laser_manual_fixed_spawn(0);
    }
    if(boss.phase_frame == 80) {
        laser_manual_grow(0);
    }
    if((boss.phase_frame % 4) == 0) {
        if(((boss.phase_frame >= 80) && (boss.phase_frame < 144)) ||
           ((boss.phase_frame % 8) == 0)) {
            angle_delta = iatan2(
                player_pos.cur.y.v - laser_template.coords.origin.y.v,
                player_pos.cur.x.v - laser_template.coords.origin.x.v);
            angle_delta -= lasers[0].coords.angle;
            if(angle_delta > 0) {
                lasers[0].coords.angle++;
            } else if(angle_delta < 0) {
                lasers[0].coords.angle--;
            }
        }
    }
    if(boss.phase_frame == 160) {
        laser_stop(0);
        return true;
    }
    return false;
}

#include "src/main/boss/mai_yuki/remaining_patterns.inl"
