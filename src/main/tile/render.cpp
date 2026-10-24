// Natural ReC98 b6ba5b0a: th04/main/tile/tile.cpp.
// The preceding REP STOSD invalidate helpers remain foreign and uncredited.
#pragma option -zCTILE_TEXT -zPmain_01
#include "src/main/runtime/small.hpp"
void pascal near tiles_render(void)
{
	overlay_titles_invalidate();
	player_invalidate();
	shots_invalidate();
	enemies_invalidate();
	bullets_and_gather_invalidate();
	items_invalidate();
	sparks_invalidate();
	pointnums_invalidate();
	midboss_invalidate();
	stage_invalidate();

	tiles_redraw_invalidated();
}

static void pascal near tiles_render_all_timed(void)
{
	tiles_render_all();
	tile_render_all_time--;
	if(tile_render_all_time == 0) {
		bg_render_not_bombing = tiles_render;
	}
}

void tiles_activate(void)
{
	bg_render_not_bombing = tiles_render;
}

void pascal tiles_activate_and_render_all_for_next_N_frames(uint8_t n)
{
	tile_render_all_time = n;
	bg_render_not_bombing = tiles_render_all_timed;
}
