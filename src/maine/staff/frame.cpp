// Complete original MAINE staff frame pump, E34E..E3A4.
#pragma option -zCSTAFF_FRAME_TEXT -zPgroup_01
#include "src/maine/staff/frame.hpp"

void near staff_frame_advance(void)
{
    staff_particles_update();
    staff_scene_render();
    frame_delay(1);
    outportb(0xA6, staff_back_page);
    staff_back_page = 1 - staff_back_page;
    outportb(0xA4, staff_back_page);
    if(staff_text_clear_requested) {
        text_clear();
        staff_text_clear_requested = 0;
    }
    staff_frame++;
    staff_bgm_measure = snd_bgm_measure();
    if(staff_bgm_measure < 0) {
        staff_bgm_measure = staff_frame / 22;
    }
}
