// One real semantic bank; const filenames and mutable title byte arrays remain distinct.
#pragma option -zCMY_TITLE_BANK_TEXT -zPmain_03
#ifdef __cplusplus
#error This initialized semantic DATA producer requires C mode
#endif
#include "src/main/boss/mai_yuki/title_bank_c.h"

MaiYukiTitleBank near mai_yuki_title_bank = {
    "_DM09.TX2",
    "真紅の少女　～ Crimson Dead!!",
    "_DM08.TX2",
    "裏切りの少女　～ Judas Kiss"
};
