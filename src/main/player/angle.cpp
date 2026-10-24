// Candidate adapted from nmlgc/ReC98@b6ba5b0a; exactness requires local replay.
#include "src/main/player/player.hpp"

unsigned char pascal near player_angle_from(
	Subpixel x, Subpixel y, unsigned char plus_angle
)
{
	return (
		iatan2((player_pos.cur.y - y), (player_pos.cur.x - x)) + plus_angle
	);
}
#pragma codestring "\x90"
