// Score flags: the number of extends gained from point items, and whether
// the "HiScore Entry" popup was already shown this game. See ReC98's
// th04/score[data].asm.
#pragma option -zCSCORE_EXTEND_FLAGS_TEXT -zPmain_01

unsigned char extends_gained = 0;
unsigned char hiscore_popup_shown = 0;

typedef char score_extend_flag_is_byte[(sizeof(extends_gained) == 1) ? 1 : -1];
typedef char score_hiscore_popup_flag_is_byte[(sizeof(hiscore_popup_shown) == 1) ? 1 : -1];
