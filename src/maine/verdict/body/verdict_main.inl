// _ude.txt holds 30-byte comment records. Records 0-25 comment on the skill
// value; the block starting at record 26 (byte 780) holds the second lines
// selected by verdict_comment_id().
static const int VERDICT_COMMENT_RECORD_BYTES = 30;
static const int VERDICT_SECOND_COMMENT_BASE = 780;

// "ゲーム達成率" compares the frames spent outside of boss fights with these
// totals. Reaching any ending always counts as 100%.
// (46000 does not fit into a 16-bit int, but is only ever stored in or passed
// as an unsigned 16-bit value.)
static const int VERDICT_STANDARD_COMPLETION_FRAMES = 46000;
static const int VERDICT_EXTRA_COMPLETION_FRAMES = 12800;

void near verdict_main(void)
{
    uint32_t max_skill;
    register int line; // `register`, as in TH04

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

    // Stage completion counts four times as much as each other percentage:
    // see the [verdict_skill_quarter] addition below.
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
    // ZUN quirk: [skill] is unsigned, but all divisions are signed.
    reinterpret_cast<long &>(skill) /= 12;
    skill += verdict_skill_quarter;
    // Up to 500,000 points for the high score, at 5,000 per 1,000,000 and
    // 50,000 per 10,000,000 points.
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
    // Starting lives and bombs settings adjust both the value and its cap.
    switch(resident->credit_lives) {
    case 1: skill += 50000UL; max_skill += 100000UL; break;
    case 2: skill += 25000UL; max_skill += 50000UL; break;
    case 3: break;
    case 4: max_skill -= 25000UL; break;
    case 5: max_skill -= 50000UL; break;
    case 6: max_skill -= 75000UL; break;
    }
    switch(resident->credit_bombs) {
    case 0: skill += 50000UL; max_skill += 100000UL; break;
    case 1: skill += 30000UL; max_skill += 50000UL; break;
    case 2: skill += 20000UL; max_skill += 25000UL; break;
    }
    if(!resident->turbo_mode) {
        skill -= 200000UL;
        max_skill -= 100000UL;
    }
    // 30,000 per miss and 15,000 per bomb, up to 10 misses and 15 bombs.
    if(resident->miss_count >= 10) {
        skill -= 300000UL;
    } else {
        skill -= (static_cast<uint32_t>(resident->miss_count) * 30000UL);
    }
    if(resident->bombs_used >= 15) {
        skill -= 225000UL;
    } else {
        skill -= (static_cast<uint32_t>(resident->bombs_used) * 15000UL);
    }
    // Game over before reaching any ending
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
    // Only rated if less than half of all frames were slowed down.
    if((resident->frames >> 1) > resident->slow_frames) {
        graph_fraction_of_million_put(verdict_text_left + 176,
            verdict_text_top + 272, skill);
        graph_putsa_fx(verdict_text_left + 272, verdict_text_top + 272,
            verdict_text_color, verdict_points_unit);
        file_ropen(verdict_comment_filename);
        // Values of 1,500,000 and above skip the seek and read record 0 at
        // the start of the freshly opened file.
        if(static_cast<long>(skill) < 1500000L) {
            if(skill == 0) {
                line = 25;
            } else if(static_cast<long>(skill) < 1050000L) {
                line = (24 - (static_cast<long>(skill) / 50000L));
            } else if(static_cast<long>(skill) < 1200000L) {
                line = 3;
            } else if(static_cast<long>(skill) < 1350000L) {
                line = 2;
            } else {
                line = 1;
            }
            file_seek((line * VERDICT_COMMENT_RECORD_BYTES), 0);
        }
        file_read(verdict_comments[0], VERDICT_COMMENT_RECORD_BYTES);
        line = verdict_comment_id();
        file_seek((line * VERDICT_COMMENT_RECORD_BYTES) + VERDICT_SECOND_COMMENT_BASE, 0);
        file_read(verdict_comments[1], VERDICT_COMMENT_RECORD_BYTES);
        file_close();
        // Cut off the line break at the end of each record.
        verdict_comments[0][28] = 0;
        verdict_comments[1][28] = 0;
    } else {
        graph_putsa_fx(verdict_text_left + 176, verdict_text_top + 272,
            verdict_text_color, verdict_unrated);
        graph_putsa_fx(verdict_text_left + 48, verdict_text_top + 296,
            verdict_comment_color, verdict_slowdown_warning);
    }
}
