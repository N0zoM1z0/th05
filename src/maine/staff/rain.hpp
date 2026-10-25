// Complete state and palette interfaces for the staff rain transition.
#ifndef TH05_MAINE_STAFF_RAIN_HPP
#define TH05_MAINE_STAFF_RAIN_HPP

#include "src/maine/staff/lifecycle.hpp"

extern int staff_rain_cursor;
extern int staff_rain_frame;
extern screen_point_t space_window_center;

// Same complete canonical RGB/Palette definitions as the frozen Boss owners.
typedef unsigned int vc2;
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

#pragma codeseg _TEXT
extern "C" void pascal far palette_show(void);
#pragma codeseg STAFF_RAIN_TEXT group_01
void near staff_rain_spawn(void);
int near staff_rain_update(void);

typedef char staff_rain_rgb_is_3[(sizeof(RGB8) == 3) ? 1 : -1];
typedef char staff_rain_palette_is_48[(sizeof(Palette8) == 48) ? 1 : -1];
typedef char staff_rain_blue_is_at_2[(offsetof(RGB8, c.b) == 2) ? 1 : -1];

#endif
