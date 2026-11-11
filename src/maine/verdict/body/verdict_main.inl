// The original six starting-life settings and three starting-bomb settings
// alter the final score *and* its allowed cap independently. Keep the actual
// saved-game integers as the switch keys, not a new serialized enum field.
enum VerdictStartingLives {
    VERDICT_START_LIVES_ONE = 1,
    VERDICT_START_LIVES_TWO = 2,
    VERDICT_START_LIVES_THREE = 3,
    VERDICT_START_LIVES_FOUR = 4,
    VERDICT_START_LIVES_FIVE = 5,
    VERDICT_START_LIVES_SIX = 6,
};
enum VerdictStartingBombs {
    VERDICT_START_BOMBS_ZERO = 0,
    VERDICT_START_BOMBS_ONE = 1,
    VERDICT_START_BOMBS_TWO = 2,
};
// These are the original capped per-use penalties, not a change in scoring.
static const int VERDICT_MISS_PENALTY_LIMIT = 10;
static const int VERDICT_BOMB_PENALTY_LIMIT = 15;
static const uint32_t VERDICT_MISS_PENALTY_PER_USE = 30000UL;
static const uint32_t VERDICT_BOMB_PENALTY_PER_USE = 15000UL;
static const int VERDICT_COMMENT_RECORD_BYTES = 30;
static const int VERDICT_SECOND_COMMENT_BASE = 780;
static const int VERDICT_COMMENT_DISPLAY_BYTES = 28;
// Original score grading uses separate standard/extra completion clocks.
// End-sequence evaluation deliberately overrides the measured frame count.
static const int VERDICT_STANDARD_COMPLETION_FRAMES = 46000;
static const int VERDICT_EXTRA_COMPLETION_FRAMES = 12800;
// A zero score chooses the very last comment record, then nonzero scores
// climb four fixed score bands before the upper 1.5M boundary.
static const long VERDICT_COMMENT_HIGH_SCORE_SKIP = 1500000L;
static const long VERDICT_COMMENT_LOW_BAND_LIMIT = 1050000L;
static const long VERDICT_COMMENT_MID_BAND_LIMIT = 1200000L;
static const long VERDICT_COMMENT_HIGH_BAND_LIMIT = 1350000L;
static const long VERDICT_COMMENT_EARLY_BAND_POINTS = 50000L;
static const int VERDICT_COMMENT_ZERO_SCORE_ROW = 25;
static const int VERDICT_COMMENT_FIRST_BAND_BASE_ROW = 24;
static const int VERDICT_COMMENT_MID_BAND_ROW = 3;
static const int VERDICT_COMMENT_HIGH_BAND_ROW = 2;
static const int VERDICT_COMMENT_TOP_BAND_ROW = 1;
// Preserve the original integer right shift, strict majority check and
// the *signed* post-rank clamp; no extra score data object is allocated.
static const int VERDICT_SLOW_PLAY_FRACTION_SHIFT = 1;
static const unsigned long VERDICT_TURBO_OFF_SCORE_PENALTY = 200000UL;
static const unsigned long VERDICT_TURBO_OFF_CAP_PENALTY = 100000UL;
static const unsigned long VERDICT_MISS_PENALTY_CAP = 300000UL;
static const unsigned long VERDICT_BOMB_PENALTY_CAP = 225000UL;

void near verdict_main(void)
{
    uint32_t max_skill;
    register int line; // Preserved from the independently pinned TH04 donor.

    skill = 0;
    graph_putsa_fx_func = FX_WEIGHT_BOLD;
    graph_putsa_fx(verdict_text_left, verdict_text_top,
        verdict_text_color, verdict_heading);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 24,
        verdict_text_color, verdict_rank_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 48,
        verdict_text_color, verdict_score_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 72,
        verdict_text_color, verdict_misses_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 96,
        verdict_text_color, verdict_bombs_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 120,
        verdict_text_color, verdict_completion_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 144,
        verdict_text_color, verdict_kills_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 168,
        verdict_text_color, verdict_items_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 192,
        verdict_text_color, verdict_point_items_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 216,
        verdict_text_color, verdict_bonus_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 240,
        verdict_text_color, verdict_slowdown_label);
    graph_putsa_fx(verdict_text_left, verdict_text_top + 272,
        verdict_text_color, verdict_skill_label);

    verdict_rank = ((resident->stage == VERDICT_STAGE_EXTRA) ?
        VERDICT_RANK_EXTRA : resident->rank);
    graph_gaiji_puts(verdict_text_left + 160, verdict_text_top + 24,
        VERDICT_GLYPH_WIDTH, &verdict_rank_glyphs[verdict_rank][0], verdict_text_color);
    verdict_score_put(verdict_text_left + 128, verdict_text_top + 48,
        resident->score_last);
    graph_3_digit_put(verdict_text_left + 224, verdict_text_top + 72,
        resident->miss_count);
    graph_3_digit_put(verdict_text_left + 224, verdict_text_top + 96,
        resident->bombs_used);
    graph_putsa_fx(verdict_text_left + 272, verdict_text_top + 72,
        verdict_text_color, verdict_miss_times);
    graph_putsa_fx(verdict_text_left + 272, verdict_text_top + 96,
        verdict_text_color, verdict_bomb_times);

    verdict_capture_quarter = true;
    if(resident->stage != VERDICT_STAGE_EXTRA) {
        if(resident->end_sequence >= VERDICT_ES_BAD) {
            resident->std_frames = VERDICT_STANDARD_COMPLETION_FRAMES;
        }
        skill_apply_and_graph_percentage_put(verdict_text_left + 176,
            verdict_text_top + 120, VERDICT_STANDARD_COMPLETION_FRAMES, resident->std_frames);
    } else {
        if(resident->end_sequence == VERDICT_ES_EXTRA) {
            resident->std_frames = VERDICT_EXTRA_COMPLETION_FRAMES;
        }
        skill_apply_and_graph_percentage_put(verdict_text_left + 176,
            verdict_text_top + 120, VERDICT_EXTRA_COMPLETION_FRAMES, resident->std_frames);
    }
    verdict_capture_quarter = false;
    skill_apply_and_graph_percentage_put(verdict_text_left + 176,
        verdict_text_top + 144, resident->enemies_gone, resident->enemies_killed);
    skill_apply_and_graph_percentage_put(verdict_text_left + 176,
        verdict_text_top + 168, resident->items_spawned, resident->items_collected);
    skill_apply_and_graph_percentage_put(verdict_text_left + 176,
        verdict_text_top + 192, resident->point_items_collected,
        resident->max_valued_point_items_collected);
    verdict_apply_bonus();
    skill_subtract = true;
    skill_apply_and_graph_percentage_put(verdict_text_left + 176,
        verdict_text_top + 240, resident->frames / 10, resident->slow_frames / 10);
    skill_subtract = false;
    reinterpret_cast<long &>(skill) /= 12;
    skill += verdict_skill_quarter;
    if(resident->score_highest.digits[SCORE_DIGITS - 1] >= 10) {
        skill += 500000UL;
    } else {
        skill += (static_cast<uint32_t>(resident->score_highest.digits[6]) * 5000UL);
        skill += (static_cast<uint32_t>(resident->score_highest.digits[7]) * 50000UL);
    }
    switch(verdict_rank) {
    case VERDICT_RANK_EASY:
        skill -= 50000UL;
        max_skill = 800000UL;
        break;
    case VERDICT_RANK_NORMAL:
        max_skill = 1000000UL;
        break;
    case VERDICT_RANK_HARD:
        skill *= 5;
        reinterpret_cast<long &>(skill) /= 4;
        skill += 150000UL;
        max_skill = 1200000UL;
        break;
    case VERDICT_RANK_LUNATIC:
        skill *= 3;
        reinterpret_cast<long &>(skill) /= 2;
        skill += 300000UL;
        max_skill = 1400000UL;
        break;
    case VERDICT_RANK_EXTRA:
        skill *= 3;
        reinterpret_cast<long &>(skill) /= 2;
        skill += 250000UL;
        max_skill = 2000000UL;
        break;
    }
    switch(resident->credit_lives) {
    case VERDICT_START_LIVES_ONE: skill += 50000UL; max_skill += 100000UL; break;
    case VERDICT_START_LIVES_TWO: skill += 25000UL; max_skill += 50000UL; break;
    case VERDICT_START_LIVES_THREE: break;
    case VERDICT_START_LIVES_FOUR: max_skill -= 25000UL; break;
    case VERDICT_START_LIVES_FIVE: max_skill -= 50000UL; break;
    case VERDICT_START_LIVES_SIX: max_skill -= 75000UL; break;
    }
    switch(resident->credit_bombs) {
    case VERDICT_START_BOMBS_ZERO: skill += 50000UL; max_skill += 100000UL; break;
    case VERDICT_START_BOMBS_ONE: skill += 30000UL; max_skill += 50000UL; break;
    case VERDICT_START_BOMBS_TWO: skill += 20000UL; max_skill += 25000UL; break;
    }
    if(!resident->turbo_mode) {
        skill -= VERDICT_TURBO_OFF_SCORE_PENALTY;
        max_skill -= VERDICT_TURBO_OFF_CAP_PENALTY;
    }
    if(resident->miss_count >= VERDICT_MISS_PENALTY_LIMIT) {
        skill -= VERDICT_MISS_PENALTY_CAP;
    } else {
        skill -= (static_cast<uint32_t>(resident->miss_count) * VERDICT_MISS_PENALTY_PER_USE);
    }
    if(resident->bombs_used >= VERDICT_BOMB_PENALTY_LIMIT) {
        skill -= VERDICT_BOMB_PENALTY_CAP;
    } else {
        skill -= (static_cast<uint32_t>(resident->bombs_used) * VERDICT_BOMB_PENALTY_PER_USE);
    }
    if(resident->end_sequence < VERDICT_ES_EXTRA) {
        skill *= 7;
        reinterpret_cast<long &>(skill) /= 8;
    }
    if(static_cast<long>(skill) < 0) {
        skill = 0;
    } else if(skill > max_skill) {
        skill = max_skill;
    }

    verdict_comments[0][0] = 0;
    verdict_comments[1][0] = 0;
    if((resident->frames >> VERDICT_SLOW_PLAY_FRACTION_SHIFT) > resident->slow_frames) {
        graph_fraction_of_million_put(verdict_text_left + 176,
            verdict_text_top + 272, skill);
        graph_putsa_fx(verdict_text_left + 272, verdict_text_top + 272,
            verdict_text_color, verdict_points_unit);
        file_ropen(verdict_comment_filename);
        if(static_cast<long>(skill) < VERDICT_COMMENT_HIGH_SCORE_SKIP) {
            if(skill == 0) {
                line = VERDICT_COMMENT_ZERO_SCORE_ROW;
            } else if(static_cast<long>(skill) < VERDICT_COMMENT_LOW_BAND_LIMIT) {
                line = (VERDICT_COMMENT_FIRST_BAND_BASE_ROW - (static_cast<long>(skill) / VERDICT_COMMENT_EARLY_BAND_POINTS));
            } else if(static_cast<long>(skill) < VERDICT_COMMENT_MID_BAND_LIMIT) {
                line = VERDICT_COMMENT_MID_BAND_ROW;
            } else if(static_cast<long>(skill) < VERDICT_COMMENT_HIGH_BAND_LIMIT) {
                line = VERDICT_COMMENT_HIGH_BAND_ROW;
            } else {
                line = VERDICT_COMMENT_TOP_BAND_ROW;
            }
            file_seek((line * VERDICT_COMMENT_RECORD_BYTES), 0);
        }
        file_read(verdict_comments[0], VERDICT_COMMENT_RECORD_BYTES);
        line = verdict_comment_id();
        file_seek((line * VERDICT_COMMENT_RECORD_BYTES) + VERDICT_SECOND_COMMENT_BASE, 0);
        file_read(verdict_comments[1], VERDICT_COMMENT_RECORD_BYTES);
        file_close();
        verdict_comments[0][VERDICT_COMMENT_DISPLAY_BYTES] = 0;
        verdict_comments[1][VERDICT_COMMENT_DISPLAY_BYTES] = 0;
    } else {
        graph_putsa_fx(verdict_text_left + 176, verdict_text_top + 272,
            verdict_text_color, verdict_unrated);
        graph_putsa_fx(verdict_text_left + 48, verdict_text_top + 296,
            verdict_comment_color, verdict_slowdown_warning);
    }
}
