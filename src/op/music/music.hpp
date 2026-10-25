// Real TH05 Music Room ABI, adapted from ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: planar.h, game/coords.hpp,
// th02/formats/musiccmt.hpp, th03/math/polar.hpp, th05/op/piano.hpp,
// libs/master.lib/master.hpp and pc98_gfx.hpp. No resource contents included.
#ifndef TH05_OP_MUSIC_HPP
#define TH05_OP_MUSIC_HPP

// Capture the complete frontend contribution before the canonical menu header
// repeats this declaration. Every real Music Room body shares this code frame.
#pragma codeseg OP_MUSIC_TEXT op_01
void near musicroom_menu(void);
#include "src/op/main/menu.hpp"
#include "src/shared/geometry.hpp"

#if GAME != 5 || BINARY != 'O'
#error This owner is the TH05 OP Music Room implementation
#endif

typedef int bool16;
typedef int vram_offset_t;
typedef int vram_byte_amount_t;
typedef int shiftjis_ank_amount_t;
typedef uint8_t vc_t;
typedef bool page_t;
typedef uint8_t dots8_t;
typedef uint32_t dots32_t;

struct screen_point_t { screen_x_t x; screen_y_t y; };
union space_changing_pixel_t { Subpixel sp; pixel_t pixel; };
struct polygon_point_t { pixel_t x; Subpixel y; };

template <class T> struct Planar {
    T B, R, G, E;
    T& operator [](int plane) { return (&B)[plane]; }
    const T& operator [](int plane) const { return (&B)[plane]; }
};

static const char SUBPIXEL_BITS = 4;
static const subpixel_t SUBPIXEL_FACTOR = 16;
#define TO_SP(pixel_value) ((pixel_value) << SUBPIXEL_BITS)
inline subpixel_t to_sp(float pixel_value) {
    return static_cast<subpixel_t>(pixel_value * SUBPIXEL_FACTOR);
}

static const shiftjis_ank_amount_t CMT_LINE_LENGTH = 38;
static const shiftjis_ank_amount_t CMT_LINE_SIZE = CMT_LINE_LENGTH + 2;
static const int CMT_COMMENT_LINES = 9;
static const int CMT_LINES = 1 + CMT_COMMENT_LINES;
struct cmt_line_t { shiftjis_t c[CMT_LINE_SIZE]; };
static const unsigned int PIANO_PART_COUNT = 6;
static const screen_y_t PIANO_TOP = 64;
static const pixel_t PIANO_H = 15;
static const pixel_t PIANO_PADDING_BOTTOM = 3;
static const pixel_t PIANO_H_PADDED = PIANO_H + PIANO_PADDING_BOTTOM;
static const screen_y_t PIANO_BOTTOM =
    PIANO_TOP + (PIANO_PART_COUNT * PIANO_H_PADDED);
static const int PLANE_SIZE = 32000;
#define BYTE_DOTS 8
#define GC_B 0x0E
#define SEEK_SET 0

extern dots8_t far *VRAM_PLANE_B;
extern "C" {
    extern const short SinTable8[256], CosTable8[256];
    void __seg* pascal far hmem_allocbyte(unsigned int bytesize);
    void pascal far hmem_free(void __seg* memseg);
    int pascal far irand(void);
    int pascal far file_ropen(const char far *filename);
    int pascal far file_read(void far *buf, unsigned int wsize);
    void pascal far file_seek(long pos, int dir);
    void pascal far file_close(void);
    void pascal far pfstart(const unsigned char far *parfile);
    void pascal far pfend(void);
    void far bgimage_snap(void);
    void far bgimage_free(void);
    void pascal far bgimage_put_rect_16(screen_x_t left, screen_y_t top,
        pixel_t width, pixel_t height);
    void pascal far grcg_polygon_c(const screen_point_t far *pts, int npoint);
    void pascal far grcg_hline(int x1, int x2, int y);
    void pascal far grcg_vline(int x, int y1, int y2);
    void pascal far graph_clear(void);
    void pascal far cdg_free_all(void);
}
void far piano_setup_and_put_initial(void);
void far piano_render(void);
int pascal far polar(int center, int radius, int ratio);
#define polar_x(center_value, radius_value, angle_value) \
    polar(center_value, radius_value, CosTable8[angle_value])
#define polar_y(center_value, radius_value, angle_value) \
    polar(center_value, radius_value, SinTable8[angle_value])
#define VRAM_CHUNK(plane_value, offset_value, bit_count) \
    *(dots##bit_count##_t far *)(VRAM_PLANE_##plane_value + offset_value)
#define graph_showpage(page_value) outportb(0xA4, page_value)
#define palette_settone(tone_value) (PaletteTone = tone_value, palette_show())

// Segment handles really occupy two bytes; the saved plane is not a far
// pointer object. These are the original master.lib typed allocation helpers.
template<class T> struct HMem {
    static T __seg* alloc(unsigned int size_in_elements) {
        return reinterpret_cast<T __seg *>(hmem_allocbyte(
            size_in_elements * sizeof(T)));
    }
    static void free(T far *&block) {
        hmem_free(reinterpret_cast<void __seg *>(block));
    }
    static void free(T __seg *&block) {
        hmem_free(reinterpret_cast<void __seg *>(block));
    }
};

static inline char ring_min() { return 0; }
#define ring_dec(value, ring_end) \
    (value)--; \
    if(value < ring_min()) { (value) = ring_end; }
#define ring_inc_ge(value, ring_end) \
    (value)++; \
    if((value) >= (ring_end)) { (value) = 0; }

// Complete frontend first declarations share one real near-code frame. The
// DS-copy helper has a genuine hardware/intrinsic body but receives no credit.
#pragma codeseg OP_MUSIC_TEXT op_01
void pascal near track_unput_or_put(uint8_t track_sel, bool16 put);
void pascal near tracklist_put(uint8_t sel);
void near nopoly_B_snap(void);
void near nopoly_B_free(void);
#pragma codeseg OP_MUSIC_TEXT op_01
void near nopoly_B_put(void);
#pragma codeseg OP_MUSIC_TEXT op_01
void pascal near polygon_build(screen_point_t near *points,
    screen_x_t center_x, space_changing_pixel_t center_y, pixel_t radius,
    int point_count, unsigned char plus_angle);
void near polygons_update_and_render(void);
void near music_update_render_and_flip(void);
void pascal near cmt_load(int track);
void near cmt_put(void);
void near cmt_fadein_both_animate(void);
void near cmt_unput_both_animate(void);
void pascal near cmt_load_unput_and_put_both_animate(int track);
void pascal near tracklist_unput_and_put_both_animate(int sel);

typedef char th05_music_point_is_4[(sizeof(screen_point_t) == 4) ? 1 : -1];
typedef char th05_music_space_changing_is_2[
    (sizeof(space_changing_pixel_t) == 2) ? 1 : -1];
typedef char th05_music_polygon_point_is_4[
    (sizeof(polygon_point_t) == 4) ? 1 : -1];
typedef char th05_music_polygon_y_at_2[
    (offsetof(polygon_point_t, y) == 2) ? 1 : -1];
typedef char th05_music_comment_line_is_40[(sizeof(cmt_line_t) == 40) ? 1 : -1];
typedef char th05_music_saved_plane_handle_is_2[
    (sizeof(dots8_t __seg*) == 2) ? 1 : -1];
typedef char th05_music_vram_pointer_is_4[
    (sizeof(VRAM_PLANE_B) == 4) ? 1 : -1];
typedef char th05_music_saved_planes_is_16[
    (sizeof(Planar<dots8_t far*>) == 16) ? 1 : -1];
typedef char th05_music_saved_planes_R_at_4[
    (offsetof(Planar<dots8_t far*>, R) == 4) ? 1 : -1];
typedef char th05_music_color_is_1[(sizeof(vc_t) == 1) ? 1 : -1];
typedef char th05_music_page_is_1[(sizeof(page_t) == 1) ? 1 : -1];

// Restore the includer's default code segment; the owner explicitly selects
// the complete frontend contribution before including the canonical body.
#pragma codeseg

#endif
