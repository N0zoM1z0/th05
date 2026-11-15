/* Writable filenames for the text masks, the stage map and the config file.
 * bb_txt_load() and map_load() change one digit of their names in place. */
#pragma option -zCMAIN_FORMAT_NAMES_TEXT -zPmain_01
#ifdef __cplusplus
#error Resource filename DATA is compiled in C mode
#endif
#include "src/shared/abi.hpp"

typedef struct MainFormatFilenames {
    char bb_text[8];
    char stage_map[9];
    unsigned char next_word_alignment; /* zero padding to an even address */
    char cfg_filename[9];
} MainFormatFilenames;

MainFormatFilenames near main_format_filenames = {
    "txt1.bb",
    "st00.map",
    0,
    "MIKO.CFG"
};

typedef char format_names_size[(sizeof(MainFormatFilenames) == 27) ? 1 : -1];
typedef char format_bb_offset[(offsetof(MainFormatFilenames, bb_text) == 0) ? 1 : -1];
typedef char format_map_offset[(offsetof(MainFormatFilenames, stage_map) == 8) ? 1 : -1];
typedef char format_align_offset[(offsetof(MainFormatFilenames, next_word_alignment) == 17) ? 1 : -1];
typedef char format_cfg_offset[(offsetof(MainFormatFilenames, cfg_filename) == 18) ? 1 : -1];
