// Natural C++ adapted from nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/main/bullet/clip.cpp.
#pragma option -zCBULLET_A_TEXT -zPmain_03 -k-
#include <dos.h>
#include "src/main/bullet/tune.hpp"
#include "src/main/player/player.hpp"

typedef unsigned char bool;
enum { false = 0, true = 1 };

extern unsigned char bullet_clear_time;
extern bool group_fixedspeed;
extern bool player_is_hit;
extern "C" subpixel_length_8_t __fastcall near playperf_speedtune(
    subpixel_length_8_t speed);

// Clip the center against the playfield expanded by half a 16-pixel sprite.
// Coordinates and collision extents retain the original Q12.4 units.
#define clip_playfield_encloses(x, y) ( \
    (static_cast<subpixel_t>(x) > -128) && \
    (static_cast<subpixel_t>(x) < (384 + 8) * 16) && \
    (static_cast<subpixel_t>(y) > -128) && \
    (static_cast<subpixel_t>(y) < (368 + 8) * 16) \
)
#define clip_overlaps_player(delta) ( \
    (unsigned int)((delta) += 64, delta) <= 128 \
)

bool near bullet_template_clip(void)
{
    if ((bullet_clear_time != 0) && (bullet_clear_time < 17)) {
clipped:
        return true;
    }
    _AX = bullet_template.origin.x;
    _DX = bullet_template.origin.y;
    if (!clip_playfield_encloses(_AX, _DX)) {
        goto clipped;
    }
    _AX -= player_pos.cur.x;
    if (clip_overlaps_player(_AX)) {
        _DX -= player_pos.cur.y;
        if (clip_overlaps_player(_DX)) {
            player_is_hit = true;
        }
    }
    if (!group_fixedspeed) {
        bullet_template.speed.v = playperf_speedtune(bullet_template.speed.v);
    }
    return false;
}
