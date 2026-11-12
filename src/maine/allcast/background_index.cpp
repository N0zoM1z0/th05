// Four real All Cast background programs; a null slot ends each program.
#pragma option -zCALLCAST_BG_INDEX_TEXT -zPgroup_01
#include "src/maine/allcast/background_index.hpp"

const char far *BG_FN[4][8] = {
    {
        allcast_background_filenames[0][0], allcast_background_filenames[0][1],
        allcast_background_filenames[0][2], allcast_background_filenames[0][3],
        allcast_background_filenames[0][4], allcast_background_filenames[0][5],
        allcast_background_filenames[0][6], 0
    },
    {
        allcast_background_filenames[1][0], allcast_background_filenames[1][1],
        allcast_background_filenames[1][2], allcast_background_filenames[1][3],
        allcast_background_filenames[1][4], allcast_background_filenames[1][5],
        allcast_background_filenames[1][6], 0
    },
    {
        allcast_background_filenames[2][0], allcast_background_filenames[2][1],
        allcast_background_filenames[2][2], allcast_background_filenames[2][3],
        allcast_background_filenames[2][4], allcast_background_filenames[2][5],
        allcast_background_filenames[2][6], 0
    },
    {
        allcast_background_filenames[3][0], allcast_background_filenames[3][1],
        allcast_background_filenames[3][2], allcast_background_filenames[3][3],
        allcast_background_filenames[3][4], allcast_background_filenames[3][5],
        allcast_background_filenames[3][6], 0
    }
};

int BG_QUARTER[4][8] = {
    { 1, 0, 1, 3, 0, 0, 0, 0 },
    { 1, 0, 1, 2, 1, 1, 1, 0 },
    { 1, 2, 0, 1, 0, 2, 2, 0 },
    { 1, 0, 0, 2, 0, 3, 3, 0 }
};

typedef char allcast_bg_fn_size128[(sizeof(BG_FN) == 128) ? 1 : -1];
typedef char allcast_bg_quarter_size64[(sizeof(BG_QUARTER) == 64) ? 1 : -1];
