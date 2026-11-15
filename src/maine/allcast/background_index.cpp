// Per-character All Cast background picture file names and the quarter of
// each .PI image to show. The file name strings are in background_filenames.c.
#pragma option -zCALLCAST_BG_INDEX_TEXT -zPgroup_01
#include "src/maine/allcast/background_index.hpp"

typedef const char far *AllCastBackgroundFilename;

#define ALLCAST_BACKGROUNDS_FOR(character) { \
    &allcast_background_filenames[character][0][0], \
    &allcast_background_filenames[character][1][0], \
    &allcast_background_filenames[character][2][0], \
    &allcast_background_filenames[character][3][0], \
    &allcast_background_filenames[character][4][0], \
    &allcast_background_filenames[character][5][0], \
    &allcast_background_filenames[character][6][0], \
    0 \
}

AllCastBackgroundFilename BG_FN[4][8] = {
    ALLCAST_BACKGROUNDS_FOR(0),
    ALLCAST_BACKGROUNDS_FOR(1),
    ALLCAST_BACKGROUNDS_FOR(2),
    ALLCAST_BACKGROUNDS_FOR(3)
};

// Every .PI image holds four 320x200 pictures; this selects the one shown on
// each screen.
int BG_QUARTER[4][8] = {
    { 1, 0, 1, 3, 0, 0, 0, 0 },
    { 1, 0, 1, 2, 1, 1, 1, 0 },
    { 1, 2, 0, 1, 0, 2, 2, 0 },
    { 1, 0, 0, 2, 0, 3, 3, 0 }
};

#undef ALLCAST_BACKGROUNDS_FOR
