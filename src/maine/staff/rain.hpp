// The particle rain of the second part of the staff roll.
#ifndef TH05_MAINE_STAFF_RAIN_HPP
#define TH05_MAINE_STAFF_RAIN_HPP

#include "src/maine/staff/lifecycle.hpp"

extern int staff_rain_cursor;
extern int staff_rain_frame;
extern screen_point_t space_window_center;

// master.lib palette types, as in ReC98's pc98.h.
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
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_RAIN_TEXT group_01
#endif
void near staff_rain_spawn(void);
int near staff_rain_update(void);

#endif
