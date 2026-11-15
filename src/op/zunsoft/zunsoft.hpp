// Declarations for the ZUN Soft logo animation.
//
// The #pragma codeseg switches are deliberate: Borland places a function in
// the code segment that is active at its first declaration, so each group of
// prototypes is declared under the segment where the function really lives.
#ifndef TH05_OP_ZUNSOFT_HPP
#define TH05_OP_ZUNSOFT_HPP
#include <dos.h>

// Declared again in menu.hpp, which must not be the first declaration.
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

// master.lib's palette types, spelled exactly as in the other units that
// define them. The logo only fades the first 15 of the 16 colors.
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

// Firework explosion. Only [distance] changes over its lifetime; origin,
// angle and speed stay constant.
struct pyro_t {
    bool alive;
    uint8_t age;
    SPPoint origin;
    Subpixel distance_prev; // ZUN bloat: Never read.
    Subpixel distance;
    Subpixel speed;
    unsigned char angle;
    unsigned char patnum_base; // sprite advances every 4 frames from here
};
static const int SUBPIXEL_FACTOR = 16;
static const int ZUNSOFT_PYRO_COUNT = 256;
static const uint16_t INPUT_NONE = 0;

// Target palette for the non-blocking fade-in.
extern Palette8 zunsoft_palette;
extern pyro_t pyros[ZUNSOFT_PYRO_COUNT];
extern char zun00_pi[9], logo[5];
extern char zun02_bft[10], zun04_bft[10], zun01_bft[10], zun03_bft[10];

#pragma codeseg OP_ZUNSOFT_TEXT op_01
// Spawns [n] new explosions at the given screen position. ReC98 takes a
// screen_point_t here; two separate ints produce the same stack layout.
void pascal near zunsoft_pyro_new(int origin_x, int origin_y, int n, char base);
void pascal near zunsoft_update_and_render(void);
void pascal near zunsoft_palette_update_and_show(int tone);

#define graph_showpage(page_value) outportb(0xA4, page_value)

typedef char zunsoft_pyro_is_14[(sizeof(pyro_t) == 14) ? 1 : -1];
#endif
