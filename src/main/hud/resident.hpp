// Candidate TH05 resident ABI corroborated by nmlgc/ReC98@b6ba5b0a529edbb3
// th05/resident.hpp, th04/score.h and the matching th05/th05.inc structure.
// This declares all real fields; it does not define/copy the resident payload.
#ifndef TH05_MAIN_HUD_RESIDENT_HPP
#define TH05_MAIN_HUD_RESIDENT_HPP

#include "src/shared/abi.hpp"

typedef unsigned char bool;
#define false 0
#define true 1

#define SCORE_DIGITS 8
#define MAIN_STAGE_COUNT 6

typedef union {
    unsigned char continues_used;
    unsigned char digits[SCORE_DIGITS];
} score_lebcd_t;

struct resident_t {
    char id[10];
    bool zunsoft_shown;
    char unused_1;
    char unknown;
    unsigned char credit_lives;
    unsigned char credit_bombs;
    unsigned char cfg_lives;
    unsigned char cfg_bombs;
    unsigned char rank;
    unsigned char bgm_mode;
    unsigned char stage;
    unsigned char playchar;
    unsigned char se_mode;
    bool turbo_mode;
    bool debug;
    unsigned char debug_stage;
    unsigned char debug_power;
    unsigned char end_sequence;
    unsigned char miss_count;
    unsigned char bombs_used;
    unsigned char demo_stage;
    char unused_2;
    unsigned char demo_num;
    score_lebcd_t score_last;
    long rand;
    unsigned int std_frames;
    unsigned int items_spawned;
    unsigned int items_collected;
    unsigned int point_items_collected;
    unsigned int max_valued_point_items_collected;
    unsigned int enemies_gone;
    unsigned int enemies_killed;
    unsigned int graze;
    unsigned long slow_frames;
    unsigned long frames;
    score_lebcd_t score_highest;
    score_lebcd_t stage_score[MAIN_STAGE_COUNT];
    long unused_3;
};

extern resident_t far *resident;

typedef char th05_resident_is_128[(sizeof(resident_t) == 128) ? 1 : -1];
typedef char th05_resident_demo_at_31[(offsetof(resident_t, demo_num) == 31) ? 1 : -1];
typedef char th05_resident_score_at_32[(offsetof(resident_t, score_last) == 32) ? 1 : -1];
typedef char th05_resident_rng_at_40[(offsetof(resident_t, rand) == 40) ? 1 : -1];
typedef char th05_resident_stats_at_44[(offsetof(resident_t, std_frames) == 44) ? 1 : -1];
typedef char th05_resident_slow_at_60[(offsetof(resident_t, slow_frames) == 60) ? 1 : -1];
typedef char th05_resident_frames_at_64[(offsetof(resident_t, frames) == 64) ? 1 : -1];
typedef char th05_resident_highest_at_68[(offsetof(resident_t, score_highest) == 68) ? 1 : -1];
typedef char th05_resident_stage_scores_at_76[(offsetof(resident_t, stage_score) == 76) ? 1 : -1];
typedef char th05_resident_unused_at_124[(offsetof(resident_t, unused_3) == 124) ? 1 : -1];

#endif
