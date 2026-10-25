// Complete natural TH05 glyph creation/target selection, original sub_BD46.
// Evidence: ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47 th05_maine.asm
// and its genuine full glyphball declaration in th05/regist.cpp.
#pragma option -zCREG_SPAWN_TEXT -zPGROUP_01
#include "src/maine/registration/spawn.hpp"
#pragma codeseg REG_SPAWN_TEXT GROUP_01

void pascal near glyphball_spawn(int x, int y, int place, playchar_t pc, uint8_t cursor)
{
    glyphball_t near *ball = &glyphballs[cursor];
    register int place_r = place;

    if(ball->phase != GBP_FREE) {
        ball->phase = GBP_REMOVE_REQUEST;
    }
    while(ball->phase != GBP_FREE) {
        registration_frame();
    }
    ball->phase = GBP_CLOUD_AT_ORIGIN;
    ball->phase_frame = 0;
    ball->glyph = gALPHABET[(y * REGISTRATION_ALPHABET_COLS) + x];
    if(ball->glyph == REGISTRATION_SPACE_GLYPH) {
        ball->glyph = REGISTRATION_EMPTY_GLYPH;
    }

    // Convert keyboard cells to screen subpixels, centered within a glyph.
    ball->pos.cur.x.v = (((x * 2) + 23) * 16 * 8) + (8 * 16);
    ball->pos.cur.y.v = ((y + 21) * 16 * 16) + (8 * 16);
    ball->angle = irand();
    ball->speed.v = (irand() % (4 * 16)) + (4 * 16);

    // The already-consumed cell coordinates become this character's score
    // panel origin. The default preserves them, matching the real byte domain.
    switch(pc) {
    case PLAYCHAR_REIMU:
        x = 8;
        y = (place_r == 0) ? 88 : ((place_r * 16) + 96);
        break;
    case PLAYCHAR_MARISA:
        x = 328;
        y = (place_r == 0) ? 88 : ((place_r * 16) + 96);
        break;
    case PLAYCHAR_MIMA:
        x = 8;
        y = (place_r == 0) ? 224 : ((place_r * 16) + 232);
        break;
    case PLAYCHAR_YUUKA:
        x = 328;
        y = (place_r == 0) ? 224 : ((place_r * 16) + 232);
        break;
    }
    ball->target.x.v = (x * 16) + (cursor * 16 * 16) + (8 * 16);
    ball->target.y.v = (y * 16) + (8 * 16);
}
