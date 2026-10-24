// Natural TH05 gather behavior. The genuine ASM structure-copy routines
// remain external; no replacement instructions are provided by this owner.
#pragma option -zCGATHER_ADD_TEXT

#include "src/main/gather/gather.hpp"

#define gather_init(gather) { \
	gather->center.cur.x = gather_template.center.x; \
	gather->center.cur.y = gather_template.center.y; \
	gather->radius_cur = gather_template.radius; \
	gather->radius_prev = gather_template.radius; \
	gather->center.velocity.x = gather_template.velocity.x; \
	gather->center.velocity.y = gather_template.velocity.y; \
	gather->angle_cur = 0x00; \
	gather->angle_delta = gather_template.angle_delta; \
	gather->col = gather_template.col; \
	gather->ring_points = gather_template.ring_points; \
	gather->radius_delta.v = (gather_template.radius.v / GATHER_FRAMES); \
}

void near gather_add_bullets(void)
{
	gather_t near *gather;
	int i;
	for((gather = gather_circles, i = 0); i < GATHER_CAP; (i++, gather++)) {
		if(gather->flag != F_FREE) {
			continue;
		}
		gather->flag = F_ALIVE;
		set_gather_template_to_bullet_template(*gather);
		gather_init(gather);
		return;
	}
}

void near gather_add_only(void)
{
	gather_t near *gather;
	int i;
	for((gather = gather_circles, i = 0); i < GATHER_CAP; (i++, gather++)) {
		if(gather->flag != F_FREE) {
			continue;
		}
		gather->flag = F_ALIVE;
		gather->bullet_template.spawn_type = BST_GATHER_ONLY;
		gather_init(gather);
		return;
	}
}

void pascal near gather_add_only_3stack(
	int frame, vc2 col_for_0, vc2 col_for_2_and_4
)
{
	switch(frame) {
	case 0:
		gather_template.col = col_for_0;
		gather_add_only();
		break;
	case 2:
		gather_template.col = col_for_2_and_4;
		gather_add_only();
		break;
	case 4:
		gather_add_only();
	}
}

#pragma codeseg GATHER_RUN_TEXT main_03

void gather_update(void)
{
	gather_t near *gather;
	int i;
	for((gather = gather_circles, i = 0); i < GATHER_CAP; (i++, gather++)) {
		if(gather->flag == F_FREE) {
			continue;
		} else if(gather->flag >= F_REMOVE) {
			gather->flag = F_FREE;
			continue;
		}
		gather->center.update_seg3();
		gather->radius_prev = gather->radius_cur;
		gather->radius_cur.v -= gather->radius_delta.v;
		gather->angle_cur += gather->angle_delta;
		if(gather->radius_cur.v < GATHER_RADIUS_END) {
			gather->flag = F_REMOVE;
			if(gather->bullet_template.spawn_type != BST_GATHER_ONLY) {
				set_bullet_template_to_gather_template(*gather);
				bullet_template.origin.x = gather->center.cur.x;
				bullet_template.origin.y = gather->center.cur.y;
				if(
					bullet_template.spawn_type < BST_GATHER_NORMAL_SPECIAL_MOVE
				) {
					bullets_add_regular();
				} else {
					bullet_template.spawn_type = BST_NORMAL;
					bullets_add_special();
				}
			}
		}
	}
}

bool near gather_point_on_playfield()
{
	return playfield_encloses_point(drawpoint, GATHER_POINT_W, GATHER_POINT_H);
}

void gather_render(void)
{
	_ES = SEG_PLANE_B;

	gather_t near *gather;
	int circle_i;
	unsigned char angle;
	vc_t col_cur;

	col_cur = -1;
	gather = gather_circles;

	for(circle_i = 0; circle_i < GATHER_CAP; circle_i++, gather++) {
		if(gather->flag != F_ALIVE) {
			continue;
		}
		if(gather->col != col_cur) {
			col_cur = gather->col;
			_AH = col_cur;
			// MODDERS: Replace with grcg_setcolor_direct_inlined(), and remove
			// the translation unit that defines this function.
			grcg_setcolor_direct_seg3_raw();
		}
		for(int point_i = 0; gather->ring_points > point_i; point_i++) {
			angle = (
				((point_i * 0x100) / gather->ring_points) + gather->angle_cur
			);
			vector2_at(
				drawpoint,
				gather->center.cur.x,
				gather->center.cur.y,
				gather->radius_cur,
				angle
			);
			if(!gather_point_on_playfield()) {
				continue;
			}
			_DX = gather_vram_top_scrolled(drawpoint, GATHER_POINT_H);
			_AX = gather_screen_left(drawpoint, GATHER_POINT_W);
			gather_point_render(_AX, _DX);
		}
	}
}
