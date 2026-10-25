int near staff_rain_update(void)
{
    orb_particle_t near *p = particles;
    int i;
    if(space_camera_velocity.x.v < 0) {
        space_camera_velocity.x.v += staff_back_page;
    }
    staff_rain_frame++;
    if(staff_rain_frame >= 32) {
        if(staff_rain_frame < 128) {
            space_camera_velocity.y.v--;
        } else if(staff_rain_frame < 308) {
            space_camera_velocity.y.v -= staff_back_page;
        } else {
            if((space_window_center.x + (space_window_w / 2)) < 630) {
                space_window_set(space_window_center.x + 4, 200,
                    space_window_w, space_window_h);
            }
            staff_particle_decay = 0;
            if((staff_rain_frame % 8) == 0) {
                staff_rain_spawn();
                for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
                    if(p->al.rain_sway_x_direction == X_RIGHT) {
                        p->angle++;
                        if(p->angle >= 0x60) {
                            p->al.rain_sway_x_direction = X_LEFT;
                        }
                    } else {
                        p->angle--;
                        if(p->angle <= 0x20) {
                            p->al.rain_sway_x_direction = X_RIGHT;
                        }
                    }
                    vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
                }
            }
            if(staff_rain_frame >= 30000) {
                staff_rain_frame = 29992;
            }
            if((space_window_center.x + (space_window_w / 2)) >= 630) {
                return 1;
            }
        }
        if(((staff_rain_frame % 4) == 0) && (Palettes.colors[0].c.b < 96)) {
            Palettes.colors[0].c.b++;
            palette_show();
        }
    }
    return 0;
}
