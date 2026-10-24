// Complete EX-Alice state machine and real foreign code/data interfaces.
#ifndef TH05_MAIN_BOSS_EXALICE_UPDATE_HPP
#define TH05_MAIN_BOSS_EXALICE_UPDATE_HPP

// Preserve actual first-declaration contexts before the common setup surface.
#pragma codeseg BOSS_BG_TEXT main_01
void pascal near exalice_bg_render(void);
extern "C" void pascal near exalice_custombullets_render(void);
#pragma codeseg EXALICE_UPD_TEXT main_03
void pascal far exalice_update(void);
// The original far hit wrapper shares this callback's CS. Capture that
// context before the independent phase owner's repeated declaration.
int far exalice_hittest_shots(void);
#include "src/main/boss/exalice/phase.hpp"
#include "src/main/boss/exalice/patterns.hpp"
#include "src/main/boss/exalice/later.hpp"
#include "src/main/boss/exalice/laser_patterns.hpp"
#include "src/main/boss/exalice/final_patterns.hpp"

// Complete canonical ODR types from the frozen Shinki owner. Its broader
// boss-specific interface is not imported into this independent owner.
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
extern "C" int pascal far super_convert_tiny(int patnum);
#pragma codeseg BOSS_TEXT main_03
void near boss_hittest_shots_invincible(void);
void pascal near boss_defeat_update(unsigned int units);
void pascal near hud_hp_update_and_render(int hp, int total);
#pragma codeseg EXALICE_PAT_TEXT main_03
void near firewaves_update(void);

#pragma codeseg EXALICE_UPD_TEXT main_03
extern int exalice_backdrop_patnum;
// Real16-byte near-callback table; no pointer values are defined here.
extern exalice_pattern_t exalice_patterns_by_phase[4][2];
typedef char exalice_palette_is_full_48[(sizeof(Palette8) == 48) ? 1 : -1];
typedef char exalice_pattern_pairs_are_16[(sizeof(exalice_patterns_by_phase) == 16) ? 1 : -1];
#endif
