void near staff_orb_particles_age(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->gather_frame++;
        if(((p->gather_frame % 8) == 0) && (p->patnum_tiny < 5)) {
            p->patnum_tiny++;
        }
    }
    // The same pointer now addresses the array's real final, large-orb element.
    if(p->al.radius < ORB_RADIUS_FULL) {
        p->al.radius += staff_back_page;
    }
}
