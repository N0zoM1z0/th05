// Draws all five rows of [pc]'s currently loaded score table.
void pascal near places_put(int pc)
{
    register int place;
    for(place = 0; place < SCOREDAT_PLACES; place++) {
        registration_place_put(place, pc);
    }
}
