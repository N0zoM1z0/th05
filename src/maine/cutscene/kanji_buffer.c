/* The cutscene interpreter copies each two-byte Shift-JIS character from the
 * script into this buffer before rendering it. */
#pragma option -zCCUTSCENE_KANJI_BUFFER_TEXT -zPgroup_01
#ifdef __cplusplus
#error This file is compiled as C
#endif

char near CUTSCENE_KANJI[3] = "  ";
