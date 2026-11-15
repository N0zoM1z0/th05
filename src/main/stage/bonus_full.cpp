// Stage Clear and All Clear bonus tallies, rendered to text RAM.
//
// As in TH04, scores are counted in units of 10 points. The multiplier helpers
// from bonus_helpers.cpp are compiled into this translation unit first, since
// they precede these functions in the original code segment: Borland writes
// relocations in 1 KiB chunks of code, and stage_allclear_bonus() only gets
// the original relocation order at its original offset in the object file.
#pragma option -zCBONUS_HELP_TEXT -zPmain_03
#include "src/main/stage/bonus_full.hpp"
#pragma codeseg BONUS_HELP_TEXT main_03
#define TH05_BONUS_HELPERS_COMBINED
#include "src/main/stage/bonus_helpers.cpp"
#undef TH05_BONUS_HELPERS_COMBINED

void near stage_clear_bonus(void)
{
    unsigned long points;
    bool no_miss;
    bool no_bomb;
    unsigned int value;

    // ZUN quirk: No Bomb also requires No Miss.
    no_miss = (resident->miss_count == bonus_previous_miss_count);
    bonus_previous_miss_count = resident->miss_count;
    no_bomb = (resident->bombs_used == bonus_previous_bomb_count) && no_miss;
    bonus_previous_bomb_count = resident->bombs_used;

    // Darken the playfield behind the tally.
    PaletteTone = 60;
    palette_show();
    gaiji_putsa(20, 4, gpCLEAR_BONUS, BONUS_TX_WHITE);
    text_putsa(6, 8, BONUS_STAGE, BONUS_TX_WHITE);
    text_putsa(6, 10, BONUS_DREAM, BONUS_TX_WHITE);
    text_putsa(6, 12, GRAZEX50, BONUS_TX_WHITE);
    text_putsa(6, 14, POINT_ITEMS, BONUS_TX_WHITE);
    if(no_miss) { text_putsa(6, 16, BONUS_NOMISS, BONUS_TX_CYAN); }
    if(no_bomb) { text_putsa(6, 17, BONUS_NOBOMB, BONUS_TX_CYAN); }
    text_putsa(6, 21, BONUS_TOTAL, BONUS_TX_WHITE);

    value = (stage_id * 100) + 100;
    points = value;
    hud_points_put(34, 8, value);
    value = dream * 10;
    points += value;
    hud_points_put(34, 10, value);
    value = stage_graze * 5;
    points += value;
    hud_points_put(34, 12, value);
    // The sum so far is multiplied by the number of point items.
    value = stage_point_items_collected;
    points *= value;
    hud_5_digit_put(40, 14, value, BONUS_TX_WHITE);
    value = (stage_id * 5000) + 10000;
    if(no_miss) {
        points += value;
        hud_points_put(34, 16, value);
    }
    if(no_bomb) {
        points += value;
        hud_points_put(34, 17, value);
    }
    // Large bonuses raise the play performance (and thus the rank), small
    // ones lower it.
    if(points >= 1200000UL) {
        playperf_raise(4);
    } else if(points >= 800000UL) {
        playperf_raise(2);
    } else if(points >= 500000UL) {
        playperf_raise(1);
    } else if(points <= 100000UL) {
        playperf_lower(2);
    } else if(points <= 200000UL) {
        playperf_lower(1);
    }
    stage_bonus_apply_modifiers(&points);
    hud_points_put(34, 21, points);
    score_delta += points;
}

void near stage_allclear_bonus(void)
{
    unsigned long points;
    unsigned long extra;
    bool no_miss;
    bool no_bomb;
    unsigned int value;
    no_miss = (resident->miss_count == bonus_previous_miss_count);
    bonus_previous_miss_count = resident->miss_count;
    no_bomb = (resident->bombs_used == bonus_previous_bomb_count) && no_miss;
    bonus_previous_bomb_count = resident->bombs_used;

    PaletteTone = 60;
    palette_show();
    extends_gained = 10;
    gaiji_putsa(19, 4, gpCONGRATULATION, BONUS_TX_WHITE);
    text_putsa(6, 6, ALL_CLEAR, BONUS_TX_WHITE);
    text_putsa(6, 8, BONUS_DREAM, BONUS_TX_WHITE);
    text_putsa(6, 10, GRAZEX50, BONUS_TX_WHITE);
    text_putsa(6, 12, PLAYER_REM, BONUS_TX_WHITE);
    text_putsa(6, 14, POINT_ITEMS, BONUS_TX_WHITE);
    if(no_miss) { text_putsa(6, 16, BONUS_NOMISS, BONUS_TX_CYAN); }
    if(no_bomb) { text_putsa(6, 17, BONUS_NOBOMB, BONUS_TX_CYAN); }
    text_putsa(6, 18, POINT_TOTAL, BONUS_TX_CYAN);
    text_putsa(6, 21, BONUS_TOTAL, BONUS_TX_WHITE);

    value = 1000;
    points = value;
    hud_points_put(34, 6, value);
    value = dream * 10;
    points += value;
    hud_points_put(34, 8, value);
    value = stage_graze * 5;
    points += value;
    hud_points_put(34, 10, value);
    // (lives - 1) * 10,000 points
    value = (lives * 1000) - 1000;
    points += value;
    hud_points_put(34, 12, value);
    value = stage_point_items_collected;
    points *= value;
    hud_5_digit_put(40, 14, value, BONUS_TX_WHITE);
    extra = 50000UL;
    if(no_miss) {
        points += extra;
        hud_points_put(34, 16, extra);
    }
    if(no_bomb) {
        points += extra;
        hud_points_put(34, 17, extra);
    }
    // 2,500 points for every point item collected during the whole game
    extra = (unsigned long)extend_point_items_collected * 250UL;
    points += extra;
    hud_points_put(34, 18, extra);
    stage_bonus_apply_modifiers(&points);
    hud_points_put(34, 21, points);
    score_delta += points;
}
