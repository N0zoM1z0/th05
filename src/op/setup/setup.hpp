// Declarations for the first-launch sound setup menu and its MSWIN.BFT
// window. Based on ReC98 th04/op/m_setup.cpp.
#ifndef TH05_OP_SETUP_SETUP_HPP
#define TH05_OP_SETUP_SETUP_HPP

#include "src/op/main/menu.hpp"

static const pixel_t MSWIN_W = 16;
static const pixel_t MSWIN_H = 16;
typedef int mswin_tile_amount_t;

// master.lib's Palette8 layout, for the unused palette in setup.cpp.
union SetupRGB8 {
    struct { uint8_t r; uint8_t g; uint8_t b; } c;
    uint8_t v[3];
};
struct SetupPalette8 {
    SetupRGB8 colors[16];
};
// Size of the currently animated window, in 16x16 tiles.
struct SetupWindow {
    mswin_tile_amount_t w;
    mswin_tile_amount_t h;
    pixel_t pixel_w(void) const { return w * MSWIN_W; }
    pixel_t pixel_h(void) const { return h * MSWIN_H; }
};
extern SetupWindow window;

extern "C" {
    void pascal far super_put(int left, int top, int patnum);
    int pascal far super_entry_bfnt(const char far *filename);
    void pascal far super_free(void);
    void pascal far palette_black_in(unsigned int speed);
}
int pascal far input_wait_for_change(int frames);
#define palette_settone(tone_value) (PaletteTone = tone_value, palette_show())
#define shiftjis_w(literal_value) ((sizeof(literal_value) - 1) * GLYPH_HALF_W)
#define SETUP_STATIC_ASSERT(condition_value) ((void)sizeof(char[1 - 2*!(condition_value)]))

void pascal near window_dropdown_put(screen_x_t left, screen_y_t bottom_tile_top);
void pascal near window_rollup_put(screen_x_t left, screen_y_t bottom_tile_top);
void pascal near dropdown(screen_x_t left, screen_y_t top);
void pascal near singleline(screen_x_t left, screen_y_t top);
void pascal near rollup(screen_x_t left, screen_y_t top);
void pascal near bgm_choice_put(int mode, vc2 color);
void pascal near se_choice_put(int mode, vc2 color);
void near bgm_help_put(void);
void near se_help_put(void);
void near setup_bgm_menu(void);
void near setup_se_menu(void);

#endif
