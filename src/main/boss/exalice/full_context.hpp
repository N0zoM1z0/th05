// Coherent real shot gate, phase helper and full EX-Alice callback context.
#ifndef TH05_MAIN_BOSS_EXALICE_FULL_CONTEXT_HPP
#define TH05_MAIN_BOSS_EXALICE_FULL_CONTEXT_HPP

// Preserve actual first-declaration contexts before the common setup surface.
#pragma codeseg BOSS_BG_TEXT main_01
void pascal near exalice_bg_render(void);
extern "C" void pascal near exalice_custombullets_render(void);
extern "C" void pascal near nullfunc_near(void);
#pragma codeseg EXALICE_FULL_TEXT main_03
// Full canonical enum before any phase-helper declaration. All three real
// local functions capture the same actual CODE segment before shared headers.
enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7FFF
};
int far exalice_hittest_shots(void);
void pascal near exalice_phase_next(explosion_type_t type, int next_end_hp);
void pascal far exalice_update(void);
#include "src/main/boss/exalice/patterns.hpp"
#include "src/main/boss/exalice/later.hpp"
#include "src/main/boss/exalice/laser_patterns.hpp"
#include "src/main/boss/exalice/final_patterns.hpp"

// Complete canonical one-byte zap union and real shared state. The accepted
// phase/generic headers remain unchanged; their broad declarations are not
// imported before the real local-definition context above.
union BulletZapState { bool active; uint8_t frame; };
extern BulletZapState bullet_zap;
extern bool bombing;
extern unsigned char exalice_bomb_invincibility;
extern bool boss_phase_timed_out;
extern bool bullet_zap_drop_point_items;
extern bool palette_changed;
extern SPPoint homing_target;
extern nearfunc_t_near bg_render_bombing_func;
static const unsigned char PHASE_BOSS_EXPLODE_SMALL = 253;

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
bool near boss_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void near boss_items_drop(void);
void pascal near boss_explode_small(explosion_type_t type);
void pascal near boss_score_bonus(unsigned int units);
void pascal near boss_defeat_update(unsigned int units);
void pascal near hud_hp_update_and_render(int hp, int total);
#pragma codeseg EXALICE_PAT_TEXT main_03
void near firewaves_update(void);

#pragma codeseg EXALICE_FULL_TEXT main_03
extern int exalice_backdrop_patnum;
// Real16-byte near-callback table; no pointer values are defined here.
extern exalice_pattern_t exalice_patterns_by_phase[4][2];
typedef char full_exalice_zap_is_1[(sizeof(BulletZapState) == 1) ? 1 : -1];
typedef char full_exalice_explosion_is_2[(sizeof(explosion_type_t) == 2) ? 1 : -1];
typedef char exalice_palette_is_full_48[(sizeof(Palette8) == 48) ? 1 : -1];
typedef char exalice_pattern_pairs_are_16[(sizeof(exalice_patterns_by_phase) == 16) ? 1 : -1];
#endif
