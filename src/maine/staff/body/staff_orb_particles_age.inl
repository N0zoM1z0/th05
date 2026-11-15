// Shrinks the gathering particles every 8 frames, and grows the orb by one
// pixel every second frame.
void near staff_orb_particles_age(void)
{
    orb_particle_t near *p = particles;
    int i;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p++) {
        p->gather_frame++;
        if(((p->gather_frame % 8) == 0) && (p->patnum_tiny < 5)) { // 5 = smallest cel
            p->patnum_tiny++;
        }
    }
    // [p] now points to the orb.
    if(p->al.radius < ORB_RADIUS_FULL) {
        p->al.radius += staff_back_page;
    }
}
