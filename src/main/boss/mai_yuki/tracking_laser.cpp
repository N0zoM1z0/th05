// Complete original 186-byte Mai/Yuki tracking laser callback.
// Preserve the near AL angular difference with one genuine register SUB.
#include <dos.h>
#include "src/main/boss/mai_yuki/later_patterns.hpp"
#include "src/main/boss/mai_yuki/tracking_laser_rules.hpp"

bool near mai_pattern_tracking_laser(void)
{
    signed char angle_delta;
    if(boss.phase_frame == MY_TRACK_AIM_FRAME) {
        laser_template.coords.origin = boss.pos.cur;
        laser_template.coords.angle = iatan2(
            player_pos.cur.y.v - laser_template.coords.origin.y.v,
            player_pos.cur.x.v - laser_template.coords.origin.x.v);
        laser_template.col = MY_TRACK_LASER_COLOR;
        laser_template.coords.width.nonshrink = MY_TRACK_LASER_WIDTH_PX;
        laser_manual_fixed_spawn(MY_TRACK_LASER_SLOT);
    }
    if(boss.phase_frame == MY_TRACK_GROW_FRAME) {
        laser_manual_grow(MY_TRACK_LASER_SLOT);
    }
    if((boss.phase_frame % MY_TRACK_EVERY_FOUR_FRAMES) == 0) {
        if(((boss.phase_frame >= MY_TRACK_GROW_FRAME) && (boss.phase_frame < MY_TRACK_FAST_TRACK_END_FRAME)) ||
           ((boss.phase_frame % MY_TRACK_OUTSIDE_WINDOW_INTERVAL) == 0)) {
            angle_delta = iatan2(
                player_pos.cur.y.v - laser_template.coords.origin.y.v,
                player_pos.cur.x.v - laser_template.coords.origin.x.v);
            _AL = lasers[MY_TRACK_LASER_SLOT].coords.angle;
            asm { sub angle_delta,al; }
            if(angle_delta > 0) {
                ++_AL;
                lasers[MY_TRACK_LASER_SLOT].coords.angle = _AL;
            } else if(angle_delta < 0) {
                _AL = lasers[MY_TRACK_LASER_SLOT].coords.angle;
                _AL += -1;
                lasers[MY_TRACK_LASER_SLOT].coords.angle = _AL;
            }
        }
    }
    if(boss.phase_frame == MY_TRACK_STOP_FRAME) {
        laser_stop(MY_TRACK_LASER_SLOT);
        return true;
    }
    return false;
}
