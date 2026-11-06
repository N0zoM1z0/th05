void pascal near zunsoft_pyro_new(
	int origin_x, int origin_y, int n, char patnum_base
)
{
	register pyro_t near *pyro;
	register int origin_x_scaled = origin_x;
	int i;
	int pyros_created = 0;
	origin_y *= SUBPIXEL_FACTOR;
	origin_x_scaled *= SUBPIXEL_FACTOR;
	pyro = pyros;
	for(i = 0; i < 256; i++, pyro++) {
		if(!pyro->alive) {
			pyro->alive = true;
			pyro->age = 0;
			pyro->origin.x.v = origin_x_scaled;
			pyro->origin.y.v = origin_y;
			pyro->distance.v = 0;
			pyro->distance_prev.v = 0;
			pyro->speed.v = ((irand() % 224) + 64);
			pyro->angle = irand();
			pyro->patnum_base = patnum_base;
			pyros_created++;
			if(pyros_created >= n) {
				break;
			}
		}
	}
}
