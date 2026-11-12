// The four All Cast programs: seven genuine PI names plus one null sentinel.
// Distinct filename bytes are owned in background_filenames.c.
#pragma option -zCALLCAST_BG_INDEX_TEXT -zPgroup_01
#include "src/maine/allcast/background_index.hpp"

// The preceding source-defined C bank owns the actual editable filename bytes.
// Keep the C symbol rather than fabricating 28 literal far addresses.


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

// Each background picture is assigned a quarter-screen entry position.
int BG_QUARTER[4][8] = {
    { 1, 0, 1, 3, 0, 0, 0, 0 },
    { 1, 0, 1, 2, 1, 1, 1, 0 },
    { 1, 2, 0, 1, 0, 2, 2, 0 },
    { 1, 0, 0, 2, 0, 3, 3, 0 }
};

#undef ALLCAST_BACKGROUNDS_FOR

typedef char allcast_bg_index_pointer_width[(sizeof(AllCastBackgroundFilename) == 4) ? 1 : -1];
typedef char allcast_bg_index_ptr_size[(sizeof(BG_FN) == 128) ? 1 : -1];
typedef char allcast_bg_index_quarter_size[(sizeof(BG_QUARTER) == 64) ? 1 : -1];
