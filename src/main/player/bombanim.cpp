// Natural TH05 Reimu bomb star algorithm from ReC98 b6ba5b0a.
// Original manual emitted circle-call bytes replaced by the genuine typed API.
#pragma option -zCBOMBANIM_TEXT -zPmain_01
#include "src/main/player/bombanim.hpp"
#pragma codeseg BOMBANIM_TEXT main_01

// Master.lib erase mode plus the inverted four-bit color plane mask.
#define reimu_star_put(star_ptr, color_value) \
    super_roll_put_1plane( \
        (star_ptr)->topleft.screen_x.v / 16, \
        (star_ptr)->topleft.screen_y.v / 16, \
        PAT_PLAYCHAR_BOMB_SHAPE, 0, \
        static_cast<unsigned int>(0x00C0 + (15 - (color_value))) \
    );

void near reimu_stars_update_and_render(void)
{
	reimu_star_t near *head;
	reimu_star_t near *trail;
	Subpixel speed;
	int i;
	unsigned char angle;

	if(bomb_frame == BOMB_CIRCLE_FRAMES) {
		head = &bomb_anim.reimu[0][0];
		trail = &bomb_anim.reimu[0][REIMU_STAR_NODE_COUNT - 1];
		i = 0;
		while(i < REIMU_STAR_TRAILS) {
			//  head == [0 |  8 | 16 | 24 | 32 | 40]
			// trail == [7 | 11 | 15 | 19 | 23 | 27]
			head->topleft.screen_x.v = (TO_SP(PLAYFIELD_LEFT) + randring1_next16_mod(TO_SP(320)));
			head->topleft.screen_y.v = randring1_next16_mod(TO_SP(BOMB_SCREEN_H - (REIMU_STAR_H / 2)));

			// MODDERS: REIMU_STAR_NODE_COUNT times
			/*    */	trail->topleft = head->topleft;
			trail--;	trail->topleft = head->topleft;
			trail--;	trail->topleft = head->topleft;
			trail--;	trail->topleft = head->topleft;
			trail--;	trail->topleft = head->topleft;
			trail--;	trail->topleft = head->topleft;
			trail--;	trail->topleft = head->topleft;
			trail += 10; // ZUN quirk

			speed.v = (TO_SP(10) + randring1_next16_and((TO_SP(18) - TO_SP(10)) - 1));
			angle = (0x40 + static_cast<unsigned char>(randring1_next16_mod(0x30) - 0x18));

			vector2(head->velocity.x.v, head->velocity.y.v, angle, speed);

			i++;
			head += REIMU_STAR_NODE_COUNT;
		}
	}
	head = &bomb_anim.reimu[0][REIMU_STAR_NODE_COUNT - 2];
	trail = &bomb_anim.reimu[0][REIMU_STAR_NODE_COUNT - 1];
	for(i = 0; i < REIMU_STAR_TRAILS; i++) {
		//  head == [6 | 14 | 22 | 30 | 38 | 46]
		// trail == [7 | 15 | 23 | 31 | 39 | 47]

		// MODDERS: (REIMU_STAR_NODE_COUNT - 1) times
		/*            */	trail->topleft = head->topleft;
		head--; trail--;	trail->topleft = head->topleft;
		head--; trail--;	trail->topleft = head->topleft;
		head--; trail--;	trail->topleft = head->topleft;
		head--; trail--;	trail->topleft = head->topleft;
		head--; trail--;	trail->topleft = head->topleft;
		head--; trail--;	trail->topleft = head->topleft;
		//  head == [0 |  8 | 16 | 24 | 32 | 40]
		// trail == [1 |  9 | 17 | 25 | 33 | 41]

		head->topleft.screen_x.v += head->velocity.x.v;
		head->topleft.screen_y.v += head->velocity.y.v;

		if(
			head->topleft.screen_x.v <= to_sp(PLAYFIELD_LEFT) ||
			head->topleft.screen_x.v >= to_sp(PLAYFIELD_RIGHT - REIMU_STAR_W)
		) {
			head->velocity.x.v = -head->velocity.x.v;
		}
		if(head->topleft.screen_y.v >= to_sp(BOMB_SCREEN_H)) {
			head->topleft.screen_y.v -= to_sp(BOMB_SCREEN_H);
		}

		trail += ((REIMU_STAR_NODE_COUNT - 1) - 2);
		// trail == [6 | 14 | 22 | 30 | 38 | 46]

		/*       */	reimu_star_put(trail, 6);
		trail -= 2;	reimu_star_put(trail, 6);
		trail -= 2;	reimu_star_put(trail, 6);
		/*       */	reimu_star_put(head, 7);

		// trail == [2 | 10 | 18 | 26 | 34 | 42]

		// ZUN bug: Should perhaps be done after the conditional branch below,
		// to avoid the out-of-bounds memory access on the last iteration of
		// this loop...
		trail += (((REIMU_STAR_NODE_COUNT * 2) - 2) - 1);
		head += ((REIMU_STAR_NODE_COUNT * 2) - 2);

		if((bomb_frame <= 112) && (stage_frame_mod8 == i)) {
            circles_add_growing(
                head->topleft.screen_x.v,
                head->topleft.screen_y.v + TO_SP(PLAYFIELD_TOP)
            );
		}
	}
}
