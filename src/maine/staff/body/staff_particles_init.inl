void near staff_particles_init(void)
{
    orb_particle_t near *p = particles;
    SPPoint near *trail_center = orb_trails_center;
    SPPoint near *star_center = stars_center;
    int i;

    space_window_set(320, 200, 384, 320);
    staff_particle_decay = 0;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->center.x.v = ((irand() % space_window_w) * 16) - (space_window_w * 8);
        p->center.y.v = ((irand() % space_window_h) * 16) - (space_window_h * 8);
        p->angle = irand();
        p->speed.v = 10; // 0.625 pixels/frame, in sixteenths.
        p->patnum_tiny = PAT_ORB_PARTICLE;
        p->al.rain_sway_x_direction = X_RIGHT;
        vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
    }
    // The array's final element is the large orb, following the 64 particles.
    p->center.x.v = STAFF_CENTER_NONE;
    p->al.radius = 0;
    p->velocity.x.v = 0;
    p->velocity.y.v = 0;
    space_camera_velocity.x.v = 0;
    space_camera_velocity.y.v = 0;

    for(i = 0; i < ORB_TRAIL_COUNT; i++, trail_center++) {
        trail_center->x.v = STAFF_CENTER_NONE;
    }
    for(i = 0; i < STAR_COUNT; i++, star_center++) {
        star_center->x.v = ((irand() % space_window_w) * 16) - (space_window_w * 8);
        star_center->y.v = ((irand() % space_window_h) * 16) - (space_window_h * 8);
    }
}
