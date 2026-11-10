// Complete original 186-byte Mai/Yuki tracking laser callback.
// Preserve the near AL angular difference with one genuine register SUB.
#include <dos.h>
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
            _AL = lasers[0].coords.angle;
            asm { sub angle_delta,al; }
            if(angle_delta > 0) {
                ++_AL;
                lasers[0].coords.angle = _AL;
            } else if(angle_delta < 0) {
                _AL = lasers[0].coords.angle;
                _AL += -1;
                lasers[0].coords.angle = _AL;
            }
        }
    }
    if(boss.phase_frame == 160) {
        laser_stop(0);
        return true;
    }
    return false;
}
