/* Original Game Over / Continue UI selectors, not font bitmaps. */
#pragma option -zCGAMEOVER_GAIJI_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Gameover semantic initialized DATA is compiled as C
#endif
#include "src/main/hud/overlay_data.h"

enum GameoverGaijiSpecial { GAMEOVER_GAIJI_QUESTION = 8 };
typedef struct GameoverGaijiBank {
    unsigned char gameover[10];
    unsigned char continue_question[11];
    unsigned char yes[4];
    unsigned char no[3];
    unsigned char credit[7];
    char erase_first[3];
} GameoverGaijiBank;

GameoverGaijiBank near gameover_gaiji_bank = {
    { HG_BOLD_G, HG_BOLD_A, HG_BOLD_M, HG_BOLD_E,
      HG_BOLD_O, HG_BOLD_V, HG_BOLD_E, HG_BOLD_R, HG_NULL, HG_NULL },
    { HG_BOLD_C, HG_BOLD_O, HG_BOLD_N, HG_BOLD_T, HG_BOLD_I,
      HG_BOLD_N, HG_BOLD_U, HG_BOLD_E, GAMEOVER_GAIJI_QUESTION,
      HG_NULL, HG_NULL },
    { HG_BOLD_Y, HG_BOLD_E, HG_BOLD_S, HG_NULL },
    { HG_BOLD_N, HG_BOLD_O, HG_NULL },
    { HG_BOLD_C, HG_BOLD_R, HG_BOLD_E, HG_BOLD_D,
      HG_BOLD_I, HG_BOLD_T, HG_NULL },
    "  "
};

typedef char gameover_bank_size[(sizeof(GameoverGaijiBank) == 38) ? 1 : -1];
typedef char gameover_continue_offset[(offsetof(GameoverGaijiBank, continue_question) == 10) ? 1 : -1];
typedef char gameover_yes_offset[(offsetof(GameoverGaijiBank, yes) == 21) ? 1 : -1];
typedef char gameover_no_offset[(offsetof(GameoverGaijiBank, no) == 25) ? 1 : -1];
typedef char gameover_credit_offset[(offsetof(GameoverGaijiBank, credit) == 28) ? 1 : -1];
typedef char gameover_erase_offset[(offsetof(GameoverGaijiBank, erase_first) == 35) ? 1 : -1];
