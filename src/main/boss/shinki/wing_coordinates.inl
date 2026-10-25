inline subpixel_t shinki_wing_random_x(void) {
	return (
		randring2_next16_mod(to_sp(SHINKI_WING_W)) +
		boss.pos.cur.x.v -
		to_sp(SHINKI_WING_W / 2)
	);
}

// Limited to the top 3/2rds of the wing area.
inline subpixel_t shinki_wing_random_y(void) {
	return (
		boss.pos.cur.y.v -
		randring2_next16_mod((to_sp(SHINKI_WING_H) / 3) * 2) +
		to_sp((SHINKI_WING_H - BOSS_H) / 2)
	);
}
