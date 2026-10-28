// Natural scalar consumer of the real DX:AX PlayfieldPoint return.
#pragma option -zCB6_BALLS_TEXT -zPmain_03
#include "src/main/boss/shinki/shinki.hpp"
#pragma codeseg B6_BALLS_TEXT main_03
void near b6balls_update(void)
{
	typedef char b6ball_backing_capacity_fits[
		((sizeof(b6ball_t) * B6BALL_COUNT) <=
		(sizeof(custom_t) * CUSTOM_COUNT)) ? 1 : -1];

	b6ball_t near *p;
	int i;
	for((p = b6balls, i = 1); i < (1 + B6BALL_COUNT); (i++, p++)) {
		if(p->flag == B6BF_FREE) {
			continue;
		}
		if(p->flag == B6BF_CLOUD) {
			p->cloud_radius.v -= to_sp(2.0f);
			if(p->cloud_radius.v < to_sp(B6BALL_W / 2)) {
				static_cast<unsigned char>(p->flag)++;
			} else {
				continue;
			}
		}

		if(bullet_clear_time || bullet_zap.active) {
			p->flag = B6BF_DECAY;
		}

		p->age++;
		p->pos.update_seg3();
        // The returned coordinates are borrowed only by these immediate bounds.
		if(!playfield_encloses(_AX, _DX, B6BALL_W, B6BALL_H)) {
			p->flag = B6BF_FREE;
		} else if(p->flag != B6BF_DECAY) {
            // Finish unpacking at the collision consumer; arithmetic uses locals.
            subpixel_t x = static_cast<subpixel_t>(_AX) - player_pos.cur.x.v;
            subpixel_t y = static_cast<subpixel_t>(_DX) - player_pos.cur.y.v;
			if(overlap_wh_inplace_fast(
				x, y, to_sp(B6BALL_W / 2), to_sp(B6BALL_H / 2)
			)) {
				player_is_hit = true;
				p->flag = B6BF_DECAY;
				continue;
			}
		} else if(p->patnum_tiny < PAT_DECAY_B6BALL) {
			// Rather brave to assume that the regular patnums of this entity
			// can't be smaller. You know how you properly DRY decay state
			// initialization? By moving it into a function...
			p->patnum_tiny = PAT_DECAY_B6BALL;
			p->pos.velocity.x.v /= 2;
			p->pos.velocity.y.v /= 2;
			p->decay_frame = 0;
		} else /* if(p->flag == B6BF_DECAY) */ {
			p->decay_frame++;
			if((p->decay_frame % 4) == 0) {
				p->patnum_tiny++;
				if(p->patnum_tiny >= (PAT_DECAY_B6BALL_last + 1)) {
					p->flag = B6BF_FREE;
				}
			}
		}
	}
}
