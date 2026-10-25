void near staff_orb_spark_add(void)
{
    orb_particle_t near *p = &particles[staff_spark_cursor++];
    p->patnum_tiny = PAT_ORB_PARTICLE;
    p->angle = irand() & 0x7F;
    p->speed.v = 3 * 16;
    vector2_at(staff_spawn_point, particles[ORB_INDEX].center.x.v,
        particles[ORB_INDEX].center.y.v, 12 * 16, p->angle);
    p->center.x.v = staff_spawn_point.x.v;
    p->center.y.v = staff_spawn_point.y.v;
    if(staff_spark_cursor >= ORB_PARTICLE_COUNT) {
        staff_spark_cursor = 0;
    }
}
