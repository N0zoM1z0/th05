// TH05 logo scene, complete canonical geometry and native graphics/driver frames.
#ifndef TH05_OP_ZUNSOFT_HPP
#define TH05_OP_ZUNSOFT_HPP
#include <dos.h>

// The canonical menu header repeats this real near entry.
#pragma codeseg OP_ZUNSOFT_TEXT op_01
void near zunsoft_animate(void);

#pragma codeseg _TEXT
extern "C" {
    int pascal far irand(void);
    void pascal far palette_show(void);
    void pascal far palette_black_out(unsigned int speed);
    void pascal far graph_clear(void);
    int pascal far graph_copy_page(int page);
    int pascal far super_entry_bfnt(const char far *filename);
    void pascal far super_put_rect(int left, int top, int pattern);
    void pascal far super_free(void);
}

#pragma codeseg SHARED
#include "src/op/main/menu.hpp"
#include "src/shared/geometry.hpp"
int pascal far polar(int center, int radius, int ratio);
extern "C" {
    extern const short SinTable8[256], CosTable8[256];
    extern unsigned int vsync_Count1;
    void far bgimage_snap(void);
    void far bgimage_put(void);
    void far bgimage_free(void);
    void pascal far snd_delay_until_measure(int measure, unsigned int frames);
}

// Token-identical complete RGB/Palette definitions used by the accepted staff
// and Boss owners. All sixteen colors remain present; this scene fades fifteen.
#define COLOR_COUNT 16
#define COMPONENT_COUNT 3
template <class ComponentType, int Range> union RGB {
    struct { ComponentType r, g, b; } c;
    ComponentType v[COMPONENT_COUNT];
    static ComponentType min() { return 0; }
    static ComponentType max() { return Range - 1; }
    void set(ComponentType r, ComponentType g, ComponentType b) {
        this->c.r = r; this->c.g = g; this->c.b = b;
    }
};
template <class RGBType> struct Palette {
    RGBType colors[COLOR_COUNT];
    static int range() { return RGBType::Range; }
    RGBType& operator [](vc2 col) { return colors[col]; }
    const RGBType& operator [](vc2 col) const { return colors[col]; }
};
typedef RGB<uint8_t, 256> RGB8;
typedef Palette<RGB8> Palette8;
extern "C" { extern Palette8 __cdecl Palettes; }

struct pyro_t {
    bool alive;
    uint8_t age;
    SPPoint origin;
    Subpixel distance_prev;
    Subpixel distance;
    Subpixel speed;
    unsigned char angle;
    unsigned char patnum_base;
};
static const int SUBPIXEL_FACTOR = 16;
static const int ZUNSOFT_PYRO_COUNT = 256;
static const uint16_t INPUT_NONE = 0;

extern Palette8 zunsoft_palette;
extern pyro_t pyros[ZUNSOFT_PYRO_COUNT];
extern char zun00_pi[9], logo[5];
extern char zun02_bft[10], zun04_bft[10], zun01_bft[10], zun03_bft[10];

#pragma codeseg OP_ZUNSOFT_TEXT op_01
// Four actual Pascal words, coordinate x/y, count and a byte sprite in a word.
void pascal near zunsoft_pyro_new(int origin_x, int origin_y, int n, char base);
void pascal near zunsoft_update_and_render(void);
void pascal near zunsoft_palette_update_and_show(int tone);

#define graph_showpage(page_value) outportb(0xA4, page_value)

typedef char zunsoft_rgb_is_3[(sizeof(RGB8) == 3) ? 1 : -1];
typedef char zunsoft_palette_is_48[(sizeof(Palette8) == 48) ? 1 : -1];
typedef char zunsoft_pyro_is_14[(sizeof(pyro_t) == 14) ? 1 : -1];
typedef char zunsoft_origin_at_2[(offsetof(pyro_t, origin) == 2) ? 1 : -1];
typedef char zunsoft_previous_at_6[(offsetof(pyro_t, distance_prev) == 6) ? 1 : -1];
typedef char zunsoft_distance_at_8[(offsetof(pyro_t, distance) == 8) ? 1 : -1];
typedef char zunsoft_speed_at_10[(offsetof(pyro_t, speed) == 10) ? 1 : -1];
typedef char zunsoft_angle_at_12[(offsetof(pyro_t, angle) == 12) ? 1 : -1];
typedef char zunsoft_pattern_at_13[(offsetof(pyro_t, patnum_base) == 13) ? 1 : -1];
typedef char zunsoft_pool_is_3584[(sizeof(pyros) == 3584) ? 1 : -1];
#endif
