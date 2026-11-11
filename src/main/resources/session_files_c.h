// Eight real original MAIN resource filenames, without a pointer table.
#ifndef TH05_MAIN_RESOURCES_SESSION_FILES_C_H
#define TH05_MAIN_RESOURCES_SESSION_FILES_C_H
#include <stddef.h>
typedef struct MainSessionFiles {
    const char demo_record[10];
    const char launcher_name[3];
    const char ems_resident_name[9];
    const char bomb_background[8];
    const char reimu_face[9];
    const char marisa_face[9];
    const char mima_face[9];
    const char yuuka_face[9];
} MainSessionFiles;
extern MainSessionFiles near main_session_files;
typedef char msf_size66[(sizeof(MainSessionFiles)==66)?1:-1];
typedef char msf_demo_at_0[(offsetof(MainSessionFiles,demo_record)==0)?1:-1];
typedef char msf_launcher_at_10[(offsetof(MainSessionFiles,launcher_name)==10)?1:-1];
typedef char msf_ems_at_13[(offsetof(MainSessionFiles,ems_resident_name)==13)?1:-1];
typedef char msf_bg_at_22[(offsetof(MainSessionFiles,bomb_background)==22)?1:-1];
typedef char msf_reimu_at_30[(offsetof(MainSessionFiles,reimu_face)==30)?1:-1];
typedef char msf_marisa_at_39[(offsetof(MainSessionFiles,marisa_face)==39)?1:-1];
typedef char msf_mima_at_48[(offsetof(MainSessionFiles,mima_face)==48)?1:-1];
typedef char msf_yuuka_at_57[(offsetof(MainSessionFiles,yuuka_face)==57)?1:-1];
#endif
