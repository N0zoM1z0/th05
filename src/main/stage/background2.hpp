// Stage-two particles and palette/tile transition, using full canonical storage.
#ifndef TH05_STAGE2_HPP
#define TH05_STAGE2_HPP
#include <dos.h>
#include "src/main/boss/background.hpp"
#include "src/main/bullet/cheeto.hpp"

#define S2PARTICLE_COUNT 64
// Complete ReC98 th05/main/stage/s2part.hpp type, distinct from boss_particle_t.
struct s2particle_t {
    unsigned char flag;
    unsigned char angle;
    PlayfieldMotion pos;
    unsigned int zoom;
    int unused[5];
};
#define s2particles (reinterpret_cast<s2particle_t near *>(custom_entities))

// Complete canonical RGB/Palette ODR definitions from the frozen Shinki owner.
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

extern unsigned int stage_frame;
extern bool scroll_active;
extern vram_y_t scroll_line;
extern uint16_t tile_ring[25][32];
extern unsigned int PaletteTone;
extern bool palette_changed;
extern int stage2_particles_spawned;
extern unsigned char stage2_palette_level;
extern unsigned char stage2_tone_offset;
extern unsigned char stage2_palette_falling;

// Real tile source-area coordinates: 640 pixels / 8 bits per VRAM byte,
// with the final four 16-pixel tile columns reserved for the source images.
static const int STAGE2_ROW_SIZE = 640 / 8;
static const int STAGE2_TILE_AREA_VRAM_LEFT = (640 - (4 * 16)) / 8;

#pragma codeseg _TEXT
extern "C" int pascal far IRand(void);
extern "C" void pascal far graph_scrollup(vram_y_t line);
#pragma codeseg SHARED
// Real far reference arguments and a byte angle; Pascal stack extent is12 bytes.
extern "C" void pascal far vector2(subpixel_t far &x, subpixel_t far &y,
    unsigned char angle, subpixel_t length);
#pragma codeseg STAGE2_TEXT main_01
void near tiles_invalidate_all(void);
vram_y_t pascal near scroll_subpixel_y_to_vram_seg1(subpixel_t y);
void pascal near stage2_particle_init(s2particle_t near &particle);
void pascal near stage2_update(void);

typedef char stage2_particle_full_26[(sizeof(s2particle_t) == 26) ? 1 : -1];
typedef char stage2_particle_fits_custom[(sizeof(s2particle_t) == sizeof(custom_t)) ? 1 : -1];
typedef char stage2_motion_at_2[(offsetof(s2particle_t, pos) == 2) ? 1 : -1];
typedef char stage2_zoom_at_14[(offsetof(s2particle_t, zoom) == 14) ? 1 : -1];
typedef char stage2_unused_at_16[(offsetof(s2particle_t, unused) == 16) ? 1 : -1];
typedef char stage2_palette_full_48[(sizeof(Palette8) == 48) ? 1 : -1];
typedef char stage2_tile_ring_full_1600[(sizeof(tile_ring) == 1600) ? 1 : -1];
#endif
