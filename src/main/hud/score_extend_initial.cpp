// ReC98 th04/score[data].asm: adjacent ordinary extend and high-score latches.
#pragma option -zCSCORE_EXTEND_FLAGS_TEXT -zPmain_01

unsigned char extends_gained = 0;
unsigned char hiscore_popup_shown = 0;

typedef char score_extend_flag_is_byte[(sizeof(extends_gained) == 1) ? 1 : -1];
typedef char score_hiscore_popup_flag_is_byte[(sizeof(hiscore_popup_shown) == 1) ? 1 : -1];
