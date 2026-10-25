void near staff_particles_gather(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->angle = iatan2(-p->center.y.v, -p->center.x.v);
        p->speed.v = ihypot(p->center.x.v, p->center.y.v) / 32;
        p->gather_frame = 0;
        vector2_at(p->velocity, 0, 0, p->speed.v, p->angle);
    }
    p->center.x.v = 0;
    p->center.y.v = 0;
    p->al.radius = 1;
}
