void pascal near space_window_set(
	screen_x_t center_x, screen_y_t center_y, pixel_t w, pixel_t h
)
{
	space_window_center.x = center_x;
	space_window_center.y = center_y;
	space_window_w = w;
	space_window_h = h;
	grc_setclip(
		(space_window_center.x - (space_window_w / 2)) - 8,
		(space_window_center.y - (space_window_h / 2)) - 8,
		(space_window_center.x + (space_window_w / 2)) + 7,
		(space_window_center.y + (space_window_h / 2)) + 7
	);
}
