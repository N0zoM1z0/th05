// Whether stage_session_init() has to load the player character's sprites,
// which it does at the start of a new game (Stage 1 or the Extra Stage).
#pragma option -zCLOAD_PLAYCHAR_INIT_TEXT -zPmain_01

int load_playchar_resources = 0;
typedef char load_playchar_is_original_word[(sizeof(load_playchar_resources) == 2) ? 1 : -1];
