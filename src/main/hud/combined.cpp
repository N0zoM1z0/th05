// Genuine contiguous HUD family, not a synthetic prefix. The eight preceding
// functions are copied verbatim from frozen accepted natural owners; see the
// private source-equivalence proof. They retain zero additional credit here.
#pragma option -G -zCHUD_COMBINED_TEXT -zPmain_01
#include "src/main/hud/combined.hpp"
// Same maintained TH04 HUD context: define byte aggregates before -a2.
#pragma option -a2

// BEGIN FROZEN BODY src/main/hud/score_reset.cpp
void near score_reset(void)
{
    int record = 1;
    register int i;
    for(i = SCORE_DIGITS - 1; i > 0; i--) {
        if(record == 1) {
            if(resident->score_highest.digits[i] < score.digits[i]) {
                record = 2;
            } else if(resident->score_highest.digits[i] > score.digits[i]) {
                record = 0;
            }
        }
        if(record == 2) {
            resident->score_highest.digits[i] = score.digits[i];
        }
        // Digit0 retains the continuation-count/least-significant slot.
        score.digits[i] = 0;
    }
    score_delta = 0;
    score_delta_frame = 0;
    hiscore_popup_shown = 0;
}
// END FROZEN BODY src/main/hud/score_reset.cpp

// BEGIN FROZEN BODY src/main/hud/lives_bombs.cpp
void far hud_lives_put(void)
{
    signed char value;
    signed char i;
    register int x;
    value = (lives - 1);
    if(value < 6) {
        i = 0;
        x = 62;
        while(i < value) {
            gaiji_putca(x, 13, HUD_RESOURCE_YINYANG, HUD_RESOURCE_WHITE);
            x += 2;
            i++;
        }
        while(i < 5) {
            gaiji_putca(x, 13, HUD_RESOURCE_EMPTY, HUD_RESOURCE_WHITE);
            x += 2;
            i++;
        }
    } else {
        text_putsa(62, 13, hud_lives_extra, HUD_RESOURCE_WHITE);
        if(value >= 10) {
            gaiji_putca(68, 13, (HUD_RESOURCE_DIGIT_ZERO + (value / 10)),
                HUD_RESOURCE_WHITE);
            value %= 10;
        }
        gaiji_putca(70, 13, (HUD_RESOURCE_DIGIT_ZERO + value),
            HUD_RESOURCE_WHITE);
    }
}

void far hud_bombs_put(void)
{
    signed char value;
    signed char i = 0;
    register int x;
    // The stored count is compared in its unsigned byte domain before being
    // assigned to the original signed display local. Keep the canonical
    // signed storage declaration used by the gameplay owners unchanged.
    if(static_cast<unsigned char>(bombs) <= 5) {
        x = 62;
        value = bombs;
        while(i < value) {
            gaiji_putca(x, 11, HUD_RESOURCE_BOMB, HUD_RESOURCE_WHITE);
            x += 2;
            i++;
        }
        while(i < 5) {
            gaiji_putca(x, 11, HUD_RESOURCE_EMPTY, HUD_RESOURCE_WHITE);
            x += 2;
            i++;
        }
    } else {
        value = bombs;
        text_putsa(62, 11, hud_bombs_extra, HUD_RESOURCE_WHITE);
        if(value >= 10) {
            gaiji_putca(68, 11, (HUD_RESOURCE_DIGIT_ZERO + (value / 10)),
                HUD_RESOURCE_WHITE);
            value %= 10;
        }
        gaiji_putca(70, 11, (HUD_RESOURCE_DIGIT_ZERO + value),
            HUD_RESOURCE_WHITE);
    }
}
// END FROZEN BODY src/main/hud/lives_bombs.cpp

// BEGIN FROZEN BODY src/main/hud/indicators.cpp
extern "C" void pascal far hud_point_items_put(void)
{
    hud_5_digit_put(62, 16, stage_point_items_collected, HUD_INDICATOR_WHITE);
    hud_5_digit_put(62, 15, extend_point_items_collected, HUD_INDICATOR_CYAN);
}

extern "C" void pascal far hud_dream_put(void)
{
    const hud_dream_colors_t colors = HUD_DREAM_COLORS;
    if((dream_prev <= (HUD_INDICATOR_BAR_MAX - 1)) &&
       (dream >= HUD_INDICATOR_BAR_MAX)) {
        overlay_popup_id_new = HUD_INDICATOR_DREAM_MAX_POPUP;
        overlay2 = overlay_popup_update_and_render;
        if(bullet_clear_time < 20) {
            bullet_clear_time = 20;
        }
    }
    dream_prev = dream;
    hud_bar_put(20, dream, colors.v[dream / (HUD_INDICATOR_BAR_MAX / 8)]);
}

void far hud_graze_put(void)
{
    hud_5_digit_put(62, 18, stage_graze, HUD_INDICATOR_WHITE);
}

extern "C" void pascal far hud_power_put(void)
{
    const hud_power_colors_t colors = HUD_POWER_COLORS;
    hud_bar_put(22, power, colors.v[shot_level]);
}
// END FROZEN BODY src/main/hud/indicators.cpp

// BEGIN FROZEN BODY src/main/hud/hp_draw.cpp
void pascal far hud_hp_put(int bar_value)
{
    const hud_bar9_t blank = gHUD_HP_BLANK;
    const hud_colors5_t colors = HUD_HP_COLORS;
    if(bar_value != 0) {
        gaiji_putsa(61, 8, reinterpret_cast<const char far *>(gsENEMY),
            HUD_HP_DRAW_YELLOW);
        hud_bar_put(9, bar_value, colors.v[bar_value / 32]);
    } else {
        gaiji_putsa(61, 8, reinterpret_cast<const char far *>(&blank.v[5]),
            HUD_HP_DRAW_WHITE);
        gaiji_putsa(56, 9, reinterpret_cast<const char far *>(blank.v),
            HUD_HP_DRAW_WHITE);
    }
}
// END FROZEN BODY src/main/hud/hp_draw.cpp

// New complete initializer; original ordinary switch generates its own table.
void far hud_put(void)
{
    gaiji_putsa(60, 3, reinterpret_cast<const char far *>(gsHISCORE),
        HUD_FULL_YELLOW);
    gaiji_putsa(61, 5, reinterpret_cast<const char far *>(gsSCORE),
        HUD_FULL_YELLOW);
    hud_score_put();

    switch(playchar) {
    case HUD_FULL_REIMU:
        gaiji_putsa(57, 11, reinterpret_cast<const char far *>(gsREIGEKI),
            HUD_FULL_YELLOW);
        gaiji_putsa(57, 13, reinterpret_cast<const char far *>(gsREIMU),
            HUD_FULL_YELLOW);
        gaiji_putsa(62, 21, reinterpret_cast<const char far *>(gsREIRYOKU),
            HUD_FULL_YELLOW);
        break;
    case HUD_FULL_MARISA:
    case HUD_FULL_MIMA:
    case HUD_FULL_YUUKA:
        gaiji_putsa(57, 11, reinterpret_cast<const char far *>(gsBOMB),
            HUD_FULL_YELLOW);
        gaiji_putsa(57, 13, reinterpret_cast<const char far *>(gsPLAYER),
            HUD_FULL_YELLOW);
        gaiji_putsa(62, 21, reinterpret_cast<const char far *>(gsPOWER),
            HUD_FULL_YELLOW);
        break;
    }

    hud_bombs_put();
    hud_lives_put();
    gaiji_putca(58, 16, HUD_FULL_POINT_GLYPH, HUD_FULL_YELLOW);
    gaiji_putsa(57, 15, reinterpret_cast<const char far *>(gsRUIKEI),
        HUD_FULL_CYAN);
    hud_point_items_put();
    gaiji_putca(63, 19, HUD_FULL_DREAM_GLYPH, HUD_FULL_YELLOW);
    hud_dream_put();
    gaiji_putca(58, 18, HUD_FULL_GRAZE_GLYPH, HUD_FULL_YELLOW);
    hud_graze_put();
    hud_power_put();
    gaiji_putsa(57, 23, (const char near *)&glEASY[rank * 8],
        ((rank == 0) ? HUD_FULL_GREEN :
         (rank == 1) ? HUD_FULL_CYAN :
         (rank == 2) ? HUD_FULL_MAGENTA : HUD_FULL_RED));
    hud_hp_put(0);
}
