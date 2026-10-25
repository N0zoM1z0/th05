// Window background, star field, orb trails, particles and the window border.
#pragma option -zCSTAFF_DRAW_TEXT -zPgroup_01
#include "src/maine/staff/render.hpp"

void near staff_scene_render(void)
{
    int x;
    int y;
    int trail_color;
    SPPoint near *trail_center;
    SPPoint near *star_center;
    orb_particle_t near *p = &particles[ORB_INDEX];
    int i;

    trail_center = &orb_trails_center[ORB_TRAIL_COUNT - 1];
    star_center = stars_center;
    grcg_setcolor(STAFF_GRCG_RMW, 0);
    grcg_boxfill(space_window_center.x - (space_window_w / 2),
        space_window_center.y - (space_window_h / 2),
        space_window_center.x + (space_window_w / 2) - 1,
        space_window_center.y + (space_window_h / 2) - 1);
    outportb(0x7C, 0);

    for(i = 0; i < STAR_COUNT; i++, star_center++) {
        x = (star_center->x.v / 16) + space_window_center.x - 4;
        y = (star_center->y.v / 16) + space_window_center.y - 4;
        super_put_tiny_small(x, y, STAFF_STAR_BIG + (i % 2));
    }
    trail_color = 6;
    for(i = 0; i < ORB_TRAIL_COUNT; i++, trail_center--) {
        if(trail_center->x.v != STAFF_CENTER_NONE) {
            x = (trail_center->x.v / 16) + space_window_center.x;
            y = (trail_center->y.v / 16) + space_window_center.y;
            grcg_setcolor(STAFF_GRCG_RMW, trail_color++);
            grcg_circlefill(x, y, ORB_RADIUS_FULL);
            outportb(0x7C, 0);
        }
    }
    if(p->center.x.v != STAFF_CENTER_NONE) {
        x = static_cast<int>(p->center.x.v / 16L) +
            space_window_center.x - (STAFF_ORB_W / 2);
        y = static_cast<int>(p->center.y.v / 16L) +
            space_window_center.y - (STAFF_ORB_H / 2);
        if(p->al.radius >= ORB_RADIUS_FULL) {
            i = STAFF_ORB_FIRST + ((staff_orb_sprite_frame / 4) % 4);
            super_put_rect(x, y, i);
            staff_orb_sprite_frame++;
        } else {
            grcg_setcolor(STAFF_GRCG_RMW, 15);
            grcg_circlefill(x + (STAFF_ORB_W / 2),
                y + (STAFF_ORB_H / 2), p->al.radius);
            outportb(0x7C, 0);
        }
    }
    p--;
    for(i = 0; i < ORB_PARTICLE_COUNT; i++, p--) {
        if((p->center.x.v != STAFF_CENTER_NONE) &&
            (p->center.x.v > (-space_window_w * 8) - (4 * 16)) &&
            (p->center.x.v < (space_window_w * 8) + (4 * 16)) &&
            (p->center.y.v > (-space_window_h * 8) - (4 * 16)) &&
            (p->center.y.v < (space_window_h * 8) + (4 * 16))) {
            x = static_cast<int>(p->center.x.v / 16L) + space_window_center.x - 4;
            y = static_cast<int>(p->center.y.v / 16L) + space_window_center.y - 4;
            super_put_tiny_small(x, y, p->patnum_tiny);
        }
    }

    grcg_setcolor(STAFF_GRCG_RMW, 1);
    grcg_boxfill(space_window_center.x - (space_window_w / 2) - 8,
        space_window_center.y - (space_window_h / 2),
        space_window_center.x - (space_window_w / 2) - 1,
        space_window_center.y + (space_window_h / 2) - 1);
    grcg_boxfill(space_window_center.x + (space_window_w / 2),
        space_window_center.y - (space_window_h / 2),
        space_window_center.x + (space_window_w / 2) + 7,
        space_window_center.y + (space_window_h / 2) - 1);
    grcg_boxfill(space_window_center.x - (space_window_w / 2) - 8,
        space_window_center.y - (space_window_h / 2) - 8,
        space_window_center.x + (space_window_w / 2) + 7,
        space_window_center.y - (space_window_h / 2) - 1);
    grcg_boxfill(space_window_center.x - (space_window_w / 2) - 8,
        space_window_center.y + (space_window_h / 2),
        space_window_center.x + (space_window_w / 2) + 7,
        space_window_center.y + (space_window_h / 2) + 7);
    outportb(0x7C, 0);
}
