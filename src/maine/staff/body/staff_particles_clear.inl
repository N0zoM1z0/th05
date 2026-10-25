void near staff_particles_clear(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->center.x.v = STAFF_CENTER_NONE;
    }
    p->al.radius = ORB_RADIUS_FULL;
    staff_particle_decay = 1;
}
