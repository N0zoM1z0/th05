// C-compatible semantic model; not a claim about historical source grouping.
// Semantic resource objects grouped without losing types, identity or mutability.
#ifndef TH05_MAIN_RESOURCE_FILENAME_BANK_C_H
#define TH05_MAIN_RESOURCE_FILENAME_BANK_C_H
#include <stddef.h>

typedef struct MainResourceFiles {
    const unsigned char main_pf_fn[12];
    const char se_fn[5];
    const char op_fn[3];
    char stage_bgm_base[5];
    const char SESSION_EYE_RGB[8];
    const char SESSION_REIMU_BFT[10];
    const char SESSION_MARI_BFT[9];
    const char SESSION_MIMA_BFT[9];
    const char SESSION_YUKA_BFT[9];
    const char SESSION_MIKOD_BFT[10];
    const char SESSION_MIKO32_BFT[11];
    const char SESSION_REIMU16_BFT[12];
    const char SESSION_MARI16_BFT[11];
    const char SESSION_MIMA16_BFT[11];
    const char SESSION_YUKA16_BFT[11];
    const char SESSION_MIKO16_BFT[11];
    const char SESSION_BOMB_YUUKA_BFT[10];
    const char SESSION_BOMB_BFT[10];
    const char SESSION_BSS0_CD2[9];
    const char SESSION_ST00_BFT[9];
    const char SESSION_ST00_MPN[9];
    const char SESSION_BSS1_CD2[9];
    const char SESSION_ST01_BFT[9];
    const char SESSION_ST01_MPN[9];
    const char SESSION_BSS2_CD2[9];
    const char SESSION_ST02_BFT[9];
    const char SESSION_ST02_MPN[9];
    const char SESSION_BSS3_CD2[9];
    const char SESSION_ST03_BFT[9];
    const char SESSION_ST03_MPN[9];
    const char SESSION_BSS4_CD2[9];
    const char SESSION_ST04_BFT[9];
    const char SESSION_ST04_MPN[9];
    const char SESSION_BSS4_CD2_REPEAT[9];
    const char SESSION_ST04_BFT_REPEAT[9];
    const char SESSION_BSS6_CD2[9];
    const char SESSION_ST06_BFT[9];
    const char SESSION_ST06_MPN[9];
} MainResourceFiles;
extern MainResourceFiles near main_resource_files;
typedef char mrf_size347[(sizeof(MainResourceFiles) == 347) ? 1 : -1];
typedef char mrf_offset_00[(offsetof(MainResourceFiles, main_pf_fn) == 0) ? 1 : -1];
typedef char mrf_offset_01[(offsetof(MainResourceFiles, se_fn) == 12) ? 1 : -1];
typedef char mrf_offset_02[(offsetof(MainResourceFiles, op_fn) == 17) ? 1 : -1];
typedef char mrf_offset_03[(offsetof(MainResourceFiles, stage_bgm_base) == 20) ? 1 : -1];
typedef char mrf_offset_04[(offsetof(MainResourceFiles, SESSION_EYE_RGB) == 25) ? 1 : -1];
typedef char mrf_offset_05[(offsetof(MainResourceFiles, SESSION_REIMU_BFT) == 33) ? 1 : -1];
typedef char mrf_offset_06[(offsetof(MainResourceFiles, SESSION_MARI_BFT) == 43) ? 1 : -1];
typedef char mrf_offset_07[(offsetof(MainResourceFiles, SESSION_MIMA_BFT) == 52) ? 1 : -1];
typedef char mrf_offset_08[(offsetof(MainResourceFiles, SESSION_YUKA_BFT) == 61) ? 1 : -1];
typedef char mrf_offset_09[(offsetof(MainResourceFiles, SESSION_MIKOD_BFT) == 70) ? 1 : -1];
typedef char mrf_offset_10[(offsetof(MainResourceFiles, SESSION_MIKO32_BFT) == 80) ? 1 : -1];
typedef char mrf_offset_11[(offsetof(MainResourceFiles, SESSION_REIMU16_BFT) == 91) ? 1 : -1];
typedef char mrf_offset_12[(offsetof(MainResourceFiles, SESSION_MARI16_BFT) == 103) ? 1 : -1];
typedef char mrf_offset_13[(offsetof(MainResourceFiles, SESSION_MIMA16_BFT) == 114) ? 1 : -1];
typedef char mrf_offset_14[(offsetof(MainResourceFiles, SESSION_YUKA16_BFT) == 125) ? 1 : -1];
typedef char mrf_offset_15[(offsetof(MainResourceFiles, SESSION_MIKO16_BFT) == 136) ? 1 : -1];
typedef char mrf_offset_16[(offsetof(MainResourceFiles, SESSION_BOMB_YUUKA_BFT) == 147) ? 1 : -1];
typedef char mrf_offset_17[(offsetof(MainResourceFiles, SESSION_BOMB_BFT) == 157) ? 1 : -1];
typedef char mrf_offset_18[(offsetof(MainResourceFiles, SESSION_BSS0_CD2) == 167) ? 1 : -1];
typedef char mrf_offset_19[(offsetof(MainResourceFiles, SESSION_ST00_BFT) == 176) ? 1 : -1];
typedef char mrf_offset_20[(offsetof(MainResourceFiles, SESSION_ST00_MPN) == 185) ? 1 : -1];
typedef char mrf_offset_21[(offsetof(MainResourceFiles, SESSION_BSS1_CD2) == 194) ? 1 : -1];
typedef char mrf_offset_22[(offsetof(MainResourceFiles, SESSION_ST01_BFT) == 203) ? 1 : -1];
typedef char mrf_offset_23[(offsetof(MainResourceFiles, SESSION_ST01_MPN) == 212) ? 1 : -1];
typedef char mrf_offset_24[(offsetof(MainResourceFiles, SESSION_BSS2_CD2) == 221) ? 1 : -1];
typedef char mrf_offset_25[(offsetof(MainResourceFiles, SESSION_ST02_BFT) == 230) ? 1 : -1];
typedef char mrf_offset_26[(offsetof(MainResourceFiles, SESSION_ST02_MPN) == 239) ? 1 : -1];
typedef char mrf_offset_27[(offsetof(MainResourceFiles, SESSION_BSS3_CD2) == 248) ? 1 : -1];
typedef char mrf_offset_28[(offsetof(MainResourceFiles, SESSION_ST03_BFT) == 257) ? 1 : -1];
typedef char mrf_offset_29[(offsetof(MainResourceFiles, SESSION_ST03_MPN) == 266) ? 1 : -1];
typedef char mrf_offset_30[(offsetof(MainResourceFiles, SESSION_BSS4_CD2) == 275) ? 1 : -1];
typedef char mrf_offset_31[(offsetof(MainResourceFiles, SESSION_ST04_BFT) == 284) ? 1 : -1];
typedef char mrf_offset_32[(offsetof(MainResourceFiles, SESSION_ST04_MPN) == 293) ? 1 : -1];
typedef char mrf_offset_33[(offsetof(MainResourceFiles, SESSION_BSS4_CD2_REPEAT) == 302) ? 1 : -1];
typedef char mrf_offset_34[(offsetof(MainResourceFiles, SESSION_ST04_BFT_REPEAT) == 311) ? 1 : -1];
typedef char mrf_offset_35[(offsetof(MainResourceFiles, SESSION_BSS6_CD2) == 320) ? 1 : -1];
typedef char mrf_offset_36[(offsetof(MainResourceFiles, SESSION_ST06_BFT) == 329) ? 1 : -1];
typedef char mrf_offset_37[(offsetof(MainResourceFiles, SESSION_ST06_MPN) == 338) ? 1 : -1];

#endif
