/* The three pause menu labels, two gaiji each: CHUUDAN (paused), SAIKAI
 * (resume) and SHUURYOU (quit). session_end.cpp declares the rows separately
 * as gsCHUUDAN, gsSAIKAI and gsSHUURYOU, ReC98's names. */
#pragma option -zCPAUSE_GAIJI_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C
#endif

enum PauseActionGaiji {
    PAUSE_GAIJI_CHUUDAN_FIRST = 0xF0,
    PAUSE_GAIJI_CHUUDAN_SECOND,
    PAUSE_GAIJI_SAIKAI_FIRST,
    PAUSE_GAIJI_SAIKAI_SECOND,
    PAUSE_GAIJI_SHUURYOU_FIRST,
    PAUSE_GAIJI_SHUURYOU_SECOND,
    PAUSE_GAIJI_TERMINATOR = 0
};

const unsigned char near pause_action_gaiji[3][3] = {
    { PAUSE_GAIJI_CHUUDAN_FIRST, PAUSE_GAIJI_CHUUDAN_SECOND, PAUSE_GAIJI_TERMINATOR },
    { PAUSE_GAIJI_SAIKAI_FIRST, PAUSE_GAIJI_SAIKAI_SECOND, PAUSE_GAIJI_TERMINATOR },
    { PAUSE_GAIJI_SHUURYOU_FIRST, PAUSE_GAIJI_SHUURYOU_SECOND, PAUSE_GAIJI_TERMINATOR }
};

typedef char pause_gaiji_action_size[(sizeof(pause_action_gaiji[0]) == 3) ? 1 : -1];
typedef char pause_gaiji_all_size[(sizeof(pause_action_gaiji) == 9) ? 1 : -1];
