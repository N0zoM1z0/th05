// Natural maintained TH04 HUD donor, with actual TH05 indicator behavior.
// The donor's documented -G context agrees with the original HUD prologues.
#pragma option -G
#pragma option -zCHUD_INDICATORS_TEXT -zPmain_01
#include "src/main/hud/indicators.hpp"
#pragma codeseg HUD_INDICATORS_TEXT main_01

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
