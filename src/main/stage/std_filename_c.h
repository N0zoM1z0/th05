// The original stand-alone TH05 standard-stage filename string.
#ifndef TH05_MAIN_STAGE_STD_FILENAME_C_H
#define TH05_MAIN_STAGE_STD_FILENAME_C_H
#include <stddef.h>
typedef struct MainStdFilename {
    const char filename[9];
} MainStdFilename;
extern MainStdFilename near main_std_filename;
typedef char std_fname_size9[(sizeof(MainStdFilename)==9)?1:-1];
typedef char std_fname_begin0[(offsetof(MainStdFilename,filename)==0)?1:-1];
#endif
