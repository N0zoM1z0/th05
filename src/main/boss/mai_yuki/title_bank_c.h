// C-compatible semantic model; not a claim about historical source grouping.
// Semantic object bank preserving original text types and alternating layout.
#ifndef TH05_MAI_YUKI_TITLE_BANK_C_H
#define TH05_MAI_YUKI_TITLE_BANK_C_H
#include <stddef.h>
typedef unsigned char shiftjis_t;

typedef struct MaiYukiTitleBank {
    const char yuki_dialog[10];
    shiftjis_t yuki_bgm_title[30];
    const char mai_dialog[10];
    shiftjis_t mai_bgm_title[28];
} MaiYukiTitleBank;
extern MaiYukiTitleBank near mai_yuki_title_bank;
typedef char my_title_bank_size78[(sizeof(MaiYukiTitleBank) == 78) ? 1 : -1];
typedef char my_title_bank_yuki_fn0[(offsetof(MaiYukiTitleBank, yuki_dialog) == 0) ? 1 : -1];
typedef char my_title_bank_yuki_bgm10[(offsetof(MaiYukiTitleBank, yuki_bgm_title) == 10) ? 1 : -1];
typedef char my_title_bank_mai_fn40[(offsetof(MaiYukiTitleBank, mai_dialog) == 40) ? 1 : -1];
typedef char my_title_bank_mai_bgm50[(offsetof(MaiYukiTitleBank, mai_bgm_title) == 50) ? 1 : -1];
#endif
