// TH05 stage5 midboss renderer ABI, ReC98 b6ba5b0a source provenance.
#ifndef TH05_MAIN_MIDBOSS_RENDER5_HPP
#define TH05_MAIN_MIDBOSS_RENDER5_HPP
#include "src/main/stage/setup.hpp"

static const pixel_t MIDBOSS5_W = 64;
static const pixel_t MIDBOSS5_H = 64;
static const unsigned char MIDBOSS5_PHASE_EXPLODE_BIG = 254;
static const int MIDBOSS5_PLAYFIELD_LEFT = 32;
static const int MIDBOSS5_PLAYFIELD_TOP = 16;
static const int MIDBOSS5_PLAYFIELD_ROLL_MARGIN = 32;

extern "C" {
    int pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
    void pascal far super_roll_put(int x, int y, int patnum);
    void pascal far super_roll_put_1plane(int x, int y, int patnum,
        int pattern_plane, unsigned int put_plane);
}
void near midboss_defeat_render(void);
void pascal near midboss5_render(void);

typedef char render5_midboss_is_22[(sizeof(midboss_stuff_t) == 22) ? 1 : -1];
typedef char render5_midboss_phase_at_17[(offsetof(midboss_stuff_t, phase) == 17) ? 1 : -1];
typedef char render5_midboss_damage_at_20[(offsetof(midboss_stuff_t, damage_this_frame) == 20) ? 1 : -1];
#endif
