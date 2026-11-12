/* Writable two-byte Shift-JIS glyph buffer and its original string end. */
#pragma option -zCCUTSCENE_KANJI_BUFFER_TEXT -zPgroup_01
#ifdef __cplusplus
#error Native cutscene-kanji DATA must have a C compiler producer
#endif

char near CUTSCENE_KANJI[3] = "  ";
typedef char cutscene_kanji_buffer_three[(sizeof(CUTSCENE_KANJI) == 3) ? 1 : -1];
