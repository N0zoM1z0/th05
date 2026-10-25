// Semantic near-pointer UI bank; all real text providers are maintained separately.
#pragma option -zCBONUS_PTR_TEXT -zPmain_03
#include "src/main/stage/bonus_pointers.hpp"

const char near *const STAGE_CLEAR_BONUS_DESC[11] = {
    bonus_timeout_text,
    bonus_credit_six_text,
    bonus_credit_five_text,
    bonus_credit_four_text,
    bonus_continue_one_text,
    bonus_continue_two_text,
    bonus_continue_three_text,
    bonus_easy_text,
    bonus_normal_text,
    bonus_hard_text,
    bonus_lunatic_text
};

const char near *BONUS_STAGE = bonus_stage_text;
const char near *BONUS_DREAM = bonus_dream_text;
const char near *GRAZEX50 = bonus_graze_text;
const char near *POINT_ITEMS = bonus_point_items_text;
const char near *BONUS_NOMISS = bonus_no_miss_text;
const char near *BONUS_NOBOMB = bonus_no_bomb_text;
const char near *BONUS_TOTAL = bonus_total_text;
const char near *ALL_CLEAR = bonus_all_clear_text;
const char near *PLAYER_REM = bonus_lives_text;
const char near *POINT_TOTAL = bonus_point_total_text;
