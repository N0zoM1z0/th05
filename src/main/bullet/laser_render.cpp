// Natural semantic ReC98 b6ba5b0a TH05 laser rendering.
#pragma option -zCLASER_RENDER_TEXT -zPmain_01 -G
#include <dos.h>
#include "src/main/bullet/laser.hpp"
#define SUBPIXEL_BITS 4
#define V_WHITE 15
typedef int screen_x_t;
extern PlayfieldPoint drawpoint;
void near grcg_setcolor_direct_raw(void);
// Genuine foreign hardware helper takes its color in AH; it has no C stack
// parameter. Keep that explicit protocol at the boundary.
#define grcg_setcolor_direct(col) _AH = col; grcg_setcolor_direct_raw()
extern "C" void pascal far grcg_circlefill(int x, int y, int radius);
extern "C" void pascal far grcg_line(int x1, int y1, int x2, int y2);
int pascal near laser_render_ray(const laser_coords_t near &coords);
inline int laser_screen_left(const PlayfieldPoint &point) {
    return ((point.x.v >> 4) + 32);
}
inline int laser_screen_top(const PlayfieldPoint &point) {
    return ((point.y.v >> 4) + 16);
}

inline void laser_line_put(PlayfieldPoint& start, PlayfieldPoint& end) {
	start.x.v = laser_screen_left(start);
	start.y.v = laser_screen_top(start);
	end.x.v = laser_screen_left(end);
	end.y.v = laser_screen_top(end);
	grcg_line(start.x, start.y, end.x, end.y);
}

void near lasers_render(void)
{
	extern PlayfieldPoint laser_line_endpoint;

	Laser near *laser;
	int i;
	for((laser = lasers, i = 0); i < LASER_COUNT; (i++, laser++)) {
		if(laser->flag == LF_FREE) {
			continue;
		}
		screen_x_t circle_center_x;
		screen_x_t circle_center_y;
		Subpixel end_distance_orig;

		// ZUN bloat: Only needed because we mutate [coords] for rendering the
		// inner ray.
		pixel_length_8_t width_orig = laser->coords.width.nonshrink;

		pixel_length_8_t radius = laser->coords.width.nonshrink;

		vector2_at(
			drawpoint,
			laser->coords.origin.x,
			laser->coords.origin.y,
			LASER_DISTANCE_MIN,
			laser->coords.angle
		);
		circle_center_x = laser_screen_left(drawpoint);
		circle_center_y = laser_screen_top(drawpoint);

		if(laser->flag != LF_SHOOTOUT_DECAY) {
			if(radius < 2) {
				radius = 2;
			}
			if(laser->coords.width.nonshrink >= 3) {
				// Outer circle
				grcg_setcolor_direct(laser->col);
				if(laser->coords.starts_at_distance.v <= LASER_DISTANCE_MIN) {
					grcg_circlefill(circle_center_x, circle_center_y, radius);
					radius -= 2; // Preparing for the inner circle already...
				}
				if(laser->coords.ends_at_distance.v > to_sp(2.0f)) {
					// Outer ray
					end_distance_orig = laser->coords.ends_at_distance;
					laser->coords.ends_at_distance.v -= to_sp(2.0f);
					laser_render_ray(laser->coords);
					laser->coords.ends_at_distance = end_distance_orig;
				}

				// Inner circle and ray
				laser->coords.width.nonshrink = (
					(laser->coords.width.nonshrink >= 5)
						? (laser->coords.width.nonshrink - 4)
						: (laser->coords.width.nonshrink - 2)
				);
			}
			grcg_setcolor_direct(V_WHITE);
			if(laser->coords.starts_at_distance.v <= LASER_DISTANCE_MIN) {
				grcg_circlefill(circle_center_x, circle_center_y, radius);
			}
			if(laser->coords.width.nonshrink <= 1) {
				// Laser is a single 1-pixel line
				vector2_at(
					drawpoint,
					laser->coords.origin.x,
					laser->coords.origin.y,
					laser->coords.starts_at_distance,
					laser->coords.angle
				);
				vector2_at(
					laser_line_endpoint,
					laser->coords.origin.x,
					laser->coords.origin.y,
					laser->coords.ends_at_distance,
					laser->coords.angle
				);
				laser_line_put(drawpoint, laser_line_endpoint);
			} else {
				if(laser_render_ray(laser->coords)) {
					laser->flag = LF_FREE;
				}
			}
		} else {
			grcg_setcolor_direct(V_WHITE);

			// Same transformation as in laser_render_ray(). Note that we only
			// get here for widths < LASER_SHOOTOUT_DECAY_WIDTH_MAX, so this
			// 8-bit shift doesn't reduce the number of possible widths for
			// other types.
			radius <<= (SUBPIXEL_BITS - 1);

			// ZUN bloat: Would have made more sense inside the loop...
			vector2_at(
				drawpoint,
				laser->coords.origin.x,
				laser->coords.origin.y,
				radius,
				(laser->coords.angle + 0x40)
			);
			for(int decay_line = 0; decay_line < 2; decay_line++) {
				vector2_at(
					laser_line_endpoint,
					drawpoint.x,
					drawpoint.y,
					laser->coords.ends_at_distance,
					laser->coords.angle
				);
				vector2_at(
					drawpoint,
					drawpoint.x,
					drawpoint.y,
					laser->coords.starts_at_distance,
					laser->coords.angle
				);
				laser_line_put(drawpoint, laser_line_endpoint);

				// ZUN bloat: ...replacing this one.
				vector2_at(
					drawpoint,
					laser->coords.origin.x,
					laser->coords.origin.y,
					radius,
					(laser->coords.angle - 0x40)
				);
			}
		}
		laser->coords.width.nonshrink = width_orig;
	}
}
