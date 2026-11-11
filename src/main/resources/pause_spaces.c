// Three distinct real 5-byte on-screen pause clearing resources.
#pragma option -zCPAUSE_TEXT -zPmain_01
#ifdef __cplusplus
#error Original pause-screen initializer is produced by C
#endif
#include <stddef.h>
typedef struct MainPauseClearText {
    const char first[5];
    const char second[5];
    const char third[5];
} MainPauseClearText;
typedef char pause15[(sizeof(MainPauseClearText)==15)?1:-1];
typedef char pause_second5[(offsetof(MainPauseClearText,second)==5)?1:-1];
typedef char pause_third10[(offsetof(MainPauseClearText,third)==10)?1:-1];
#define PAUSE_BLANK "    "
MainPauseClearText near main_pause_clear_text = {
    PAUSE_BLANK,
    PAUSE_BLANK,
    PAUSE_BLANK
};
