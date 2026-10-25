void near staff_particles_scatter(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        // These initial polar values really precede the random replacement.
        p->angle = iatan2(-p->center.y.v, -p->center.x.v);
        p->speed.v = ihypot(p->center.x.v, p->center.y.v) / 32;
        p->patnum_tiny = PAT_ORB_PARTICLE;
        p->angle = irand() & 0x7F;
        p->speed.v = (irand() % (4 * 16)) + ((5 * 16) + 12);
        vector2_at(staff_spawn_point, particles[ORB_INDEX].center.x.v,
            particles[ORB_INDEX].center.y.v, 12 * 16, p->angle);
        vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
        p->center.x.v = staff_spawn_point.x.v;
        p->center.y.v = staff_spawn_point.y.v;
    }
    p->center.x.v = STAFF_CENTER_NONE;
    staff_particle_decay = 1;
}
