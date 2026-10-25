// Natural TH04 HUD algorithm adapted to the actual TH05 standalone counts.
// -G is the maintained donor's initial producer option, not a size probe.
#pragma option -G -zCHUD_RESOURCES_TEXT -zPmain_01
#include "src/main/hud/lives_bombs.hpp"

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
