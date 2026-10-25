int near staff_orb_opening_update(void)
{
    int elapsed;
    int horizontal_offset;
    staff_orb_opening_frame++;
    if(staff_orb_opening_frame >= 80) {
        if(staff_orb_opening_frame < 176) {
            space_camera_velocity.y.v++;
        } else if(staff_orb_opening_frame < 344) {
            space_camera_velocity.y.v += staff_back_page;
        } else if(staff_camera_accel_phase == 0) {
            space_camera_velocity.y.v += ((staff_frame % 16) == 0);
            if(space_camera_velocity.y.v > ((11 * 16) + 6)) {
                staff_camera_accel_phase++;
            }
        } else {
            space_camera_velocity.y.v -= ((staff_frame % 16) == 0);
            if(space_camera_velocity.y.v < ((11 * 16) + 2)) {
                staff_camera_accel_phase--;
            }
        }

        if(staff_orb_opening_frame >= 234) {
            if(staff_orb_opening_frame < 512) {
                elapsed = staff_orb_opening_frame - 234;
                horizontal_offset = (elapsed > 88) ? (elapsed - 88) : 0;
                space_window_set(320 - horizontal_offset, 200,
                    384 - (elapsed / 2), 320 + (elapsed / 8));
            } else {
                if((staff_orb_opening_frame >= 992) &&
                    (staff_orb_opening_frame <= 1024)) {
                    particles[ORB_INDEX].velocity.x.v--;
                }
                if((staff_orb_opening_frame >= 1008) &&
                    (staff_orb_opening_frame <= 1040)) {
                    space_camera_velocity.x.v--;
                }
                return 1;
            }
        }
    }
    return 0;
}
