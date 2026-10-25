void near staff_orb_trail_update(void)
{
    int i;
    for(i = ORB_TRAIL_COUNT - 2; i >= 0; i--) {
        orb_trails_center[i + 1].x.v = orb_trails_center[i].x.v;
        orb_trails_center[i + 1].y.v = orb_trails_center[i].y.v;
    }
    orb_trails_center[0].x.v = particles[ORB_INDEX].center.x.v;
    orb_trails_center[0].y.v = particles[ORB_INDEX].center.y.v;
}
