// TH05 original DATA at 209D:00A0, before the pause-action glyphs.
// The historical TASM source emits two adjacent `db 0` bytes.
#pragma option -zCLOAD_PLAYCHAR_INIT_TEXT -zPmain_01

int load_playchar_resources = 0;
typedef char load_playchar_is_original_word[(sizeof(load_playchar_resources) == 2) ? 1 : -1];
