// Spawns a rain particle at the top edge of the window, falling down at a
// random angle between 45° and 135°.
void near staff_rain_spawn(void)
{
    orb_particle_t near *p = &particles[staff_rain_cursor];
    // ZUN quirk: Compares the incremented cursor, so particle 63 is never
    // spawned. Writing the increment inside the condition is needed to match
    // the original code.
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
