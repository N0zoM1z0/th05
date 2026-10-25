// Natural TH05 verdict logic and actual foreign interfaces.
#ifndef TH05_VERDICT_MAIN_DRAFT_HPP
#define TH05_VERDICT_MAIN_DRAFT_HPP
#include "src/maine/verdict/format.hpp"
#include "src/maine/verdict/bonus.hpp"
#include "src/maine/verdict/display.hpp"
enum verdict_rank_t {
    VERDICT_RANK_EASY = 0, VERDICT_RANK_NORMAL = 1,
    VERDICT_RANK_HARD = 2, VERDICT_RANK_LUNATIC = 3,
    VERDICT_RANK_EXTRA = 4
};
static const int VERDICT_STAGE_EXTRA = 6;
enum graph_putsa_fx_func_t {
    FX_WEIGHT_NORMAL = 0, FX_WEIGHT_HEAVY = 1,
    FX_WEIGHT_BOLD = 2, FX_WEIGHT_BLACK = 3,
    FX_MASK, FX_MASK_1 = FX_MASK, FX_MASK_2, FX_MASK_3, FX_MASK_4, FX_MASK_END,
    _graph_putsa_fx_func_FORCE_INT16 = 0x7FFF
};
extern graph_putsa_fx_func_t graph_putsa_fx_func;
extern uint8_t verdict_rank;
extern char verdict_rank_glyphs[5][8];
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
#pragma codeseg _TEXT
extern "C" {
    int pascal far file_ropen(const char far *filename);
    void pascal far file_seek(long offset, int origin);
    int pascal far file_read(void far *buffer, unsigned count);
    void pascal far file_close(void);
}
#ifdef TH05_VERDICT_FULL_FAMILY
#pragma codeseg VERDICT_FULL_TEXT group_01
#else
#pragma codeseg VERDICT_MAIN_TEXT group_01
#endif
void near verdict_main(void);
#endif
