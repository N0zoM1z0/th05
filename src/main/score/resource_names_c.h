// The original consecutive score file and continue glyph resources.
#ifndef TH05_MAIN_SCORE_RESOURCE_NAMES_C_H
#define TH05_MAIN_SCORE_RESOURCE_NAMES_C_H
#include <stddef.h>
typedef struct MainScoreResourceNames {
    const char score_file[11];
    const unsigned char continue_glyphs[9];
} MainScoreResourceNames;
extern MainScoreResourceNames near main_score_resource_names;
typedef char score_resource_size20[(sizeof(MainScoreResourceNames)==20)?1:-1];
typedef char score_resource_name_at0[(offsetof(MainScoreResourceNames,score_file)==0)?1:-1];
typedef char score_resource_glyphs_at11[(offsetof(MainScoreResourceNames,continue_glyphs)==11)?1:-1];
#endif
