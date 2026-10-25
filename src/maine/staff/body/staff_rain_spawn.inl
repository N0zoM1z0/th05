void near staff_rain_spawn(void)
{
    orb_particle_t near *p = &particles[staff_rain_cursor];
    if(++staff_rain_cursor < ORB_PARTICLE_COUNT) {
        p->speed.v = (irand() % 24) + 8;
        p->angle = (irand() % 64) + 32;
        p->patnum_tiny = irand() % 6;
        p->center.x.v = ((irand() % space_window_w) * 16) - (space_window_w * 8);
        p->center.y.v = (-space_window_h * 8) - (4 * 16);
        p->al.rain_sway_x_direction = (p->angle < 0x40) ? X_RIGHT : X_LEFT;
        vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
    }
}
