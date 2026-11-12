// Complete natural C++ hexagram geometry from the maintained boss background.
#pragma option -zCEXALICE_HEX_TEXT -zPmain_01
#include <dos.h>
#include "src/main/boss/background.hpp"
#include "src/main/boss/exalice/hexagram_rules.hpp"

static const screen_x_t HEXAGRAM_CENTER_X = (
	PLAYFIELD_LEFT + (PLAYFIELD_W / 2)
);
static const vram_y_t HEXAGRAM_CENTER_Y = (PLAYFIELD_TOP + (PLAYFIELD_H / 2));

#define exalice_hexagram_point_set(ret, radius, angle) \
	vector2_at( \
		ret, to_sp(HEXAGRAM_CENTER_X), to_sp(HEXAGRAM_CENTER_Y), radius, angle \
	)

void pascal near exalice_grcg_hexagram_put(subpixel_t radius, int angle)
{
	#define tri_point_0 drawpoint
	extern SPPoint tri_point_1;
	extern SPPoint tri_point_2;

	grcg_circle(HEXAGRAM_CENTER_X, HEXAGRAM_CENTER_Y, TO_PIXEL(radius));
	int i = 0;
	while(i < XHG_TRIANGLE_COUNT) {
		exalice_hexagram_point_set(tri_point_0, radius, angle);
		exalice_hexagram_point_set(tri_point_1, radius, (angle + XHG_VERTEX_ANGLE));
		exalice_hexagram_point_set(tri_point_2, radius, (angle - XHG_VERTEX_ANGLE));

		TO_PIXEL_INPLACE(tri_point_0.x.v);
		TO_PIXEL_INPLACE(tri_point_0.y.v);
		TO_PIXEL_INPLACE(tri_point_1.x.v);
		TO_PIXEL_INPLACE(tri_point_1.y.v);
		TO_PIXEL_INPLACE(tri_point_2.x.v);
		TO_PIXEL_INPLACE(tri_point_2.y.v);

		grcg_line(
			tri_point_0.x.v, tri_point_0.y.v, tri_point_1.x.v, tri_point_1.y.v
		);
		grcg_line(
			tri_point_1.x.v, tri_point_1.y.v, tri_point_2.x.v, tri_point_2.y.v
		);
		grcg_line(
			tri_point_0.x.v, tri_point_0.y.v, tri_point_2.x.v, tri_point_2.y.v
		);

		i++;
		angle += XHG_TRIANGLE_ROTATION;
	}

	#undef tri_point_0
}
