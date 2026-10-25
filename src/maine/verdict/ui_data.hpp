// Exact existing verdict UI object interfaces; no graphic or font payload.
#ifndef TH05_VERDICT_UI_DATA_HPP
#define TH05_VERDICT_UI_DATA_HPP
#include "src/shared/abi.hpp"
#if GAME != 5 || BINARY != 'E'
#error This verdict text owner belongs to TH05 MAINE
#endif

// Identical to the accepted verdict formatter's complete byte character type.
typedef uint8_t shiftjis_t;
extern const shiftjis_t near verdict_score_unit[];
extern const shiftjis_t near verdict_decimal_point[];
extern const shiftjis_t near verdict_percent_sign[];
extern const shiftjis_t near verdict_fraction_point[];
extern const shiftjis_t near verdict_bonus_percent_sign[];
extern const shiftjis_t near verdict_heading[];
extern const shiftjis_t near verdict_rank_label[];
extern const shiftjis_t near verdict_score_label[];
extern const shiftjis_t near verdict_misses_label[];
extern const shiftjis_t near verdict_bombs_label[];
extern const shiftjis_t near verdict_completion_label[];
extern const shiftjis_t near verdict_kills_label[];
extern const shiftjis_t near verdict_items_label[];
extern const shiftjis_t near verdict_point_items_label[];
extern const shiftjis_t near verdict_bonus_label[];
extern const shiftjis_t near verdict_slowdown_label[];
extern const shiftjis_t near verdict_skill_label[];
extern const shiftjis_t near verdict_miss_times[];
extern const shiftjis_t near verdict_bomb_times[];
extern const shiftjis_t near verdict_points_unit[];
extern const char near verdict_comment_filename[];
extern const shiftjis_t near verdict_unrated[];
extern const shiftjis_t near verdict_slowdown_warning[];
extern const char near verdict_picture_filename[];
extern const shiftjis_t near verdict_stage_1_title[];
extern const shiftjis_t near verdict_stage_2_title[];
extern const shiftjis_t near verdict_stage_3_title[];
extern const shiftjis_t near verdict_stage_4_title[];
extern const shiftjis_t near verdict_stage_5_title[];
extern const shiftjis_t near verdict_stage_6_title[];
extern const shiftjis_t near verdict_final_score_title[];
#endif
