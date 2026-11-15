/* Filename of the eyecatch images shown while a stage loads. */
#pragma option -zCEYECATCH_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Compile this file as C
#endif

char EYECATCH_FN[] = "eye.cdg";
typedef char eyecatch_filename_length[(sizeof(EYECATCH_FN) == 8) ? 1 : -1];
