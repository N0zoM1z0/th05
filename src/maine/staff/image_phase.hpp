// Full canonical CDG16 record and genuine staff image-phase APIs.
#ifndef TH05_STAFF_IMAGE_PHASE_HPP
#define TH05_STAFF_IMAGE_PHASE_HPP
#include "src/shared/abi.hpp"
#if GAME != 5 || BINARY != 'E'
#error This owner is the TH05 MAINE staff image phase
#endif

typedef uint16_t seg_t;
typedef uint8_t dots8_t;
enum cdg_plane_layout_t {
    CDG_COLORS = 0, CDG_COLORS_AND_ALPHA = 1, CDG_ALPHA = 2
};
// Identical full class definition to the accepted MAIN EMS consumer. Source
// provenance is ReC98 th03/formats/cdg.h; this owner defines no pool storage.
struct CDG {
    uint16_t bitplane_size;
    int pixel_w;
    int pixel_h;
    int offset_at_bottom_left;
    uint16_t vram_dword_w;
    uint8_t image_count;
    signed char plane_layout;
    dots8_t __seg *seg[2];
    dots8_t __seg *&seg_alpha() { return seg[0]; }
    dots8_t __seg *&seg_colors() { return seg[1]; }
};
static const int CDG_SLOT_COUNT = 64;
extern CDG cdg_slots[CDG_SLOT_COUNT];

extern unsigned char staff_text_clear_requested;
extern int staff_bgm_measure;
extern int staff_image_phase_a;
extern int staff_image_wipe_extent_a;
extern int staff_image_wipe_frame_a;
extern char staff_image_cover_a[3];
static const unsigned int STAFF_TEXT_BLACK = 0x01;
static const unsigned int STAFF_TEXT_REVERSE = 0x04;
static const int STAFF_IMAGE_HOLD_MEASURE = 3996;

#pragma codeseg _TEXT
extern "C" void pascal far text_putsa(unsigned int x, unsigned int y,
    const char far *text, unsigned int attribute);
#pragma codeseg SHARED
extern "C" void pascal far cdg_put_noalpha_8(int left, int top, int slot);
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_WIPE_TEXT group_01
#endif
// Six true word slots and RET12; actual callers consume AL status0/1/2.
unsigned char pascal near staff_text_wipe(int left, int top, int width,
    int height, int extent, int direction);
#ifdef TH05_STAFF_FULL_FAMILY
#pragma codeseg STAFF_FULL_TEXT group_01
#else
#pragma codeseg STAFF_IMAGE_A_TEXT group_01
#endif
int pascal near staff_image_update_a(int center_x, int center_y,
    int slot, int measure);
#pragma codeseg

typedef char staff_image_cdg_is_16[(sizeof(CDG) == 16) ? 1 : -1];
typedef char staff_image_cdg_w_at_2[(offsetof(CDG, pixel_w) == 2) ? 1 : -1];
typedef char staff_image_cdg_h_at_4[(offsetof(CDG, pixel_h) == 4) ? 1 : -1];
typedef char staff_image_cdg_planes_at_12[(offsetof(CDG, seg) == 12) ? 1 : -1];
typedef char staff_image_cdg_planes_are_4[(sizeof(((CDG *)0)->seg) == 4) ? 1 : -1];
typedef char staff_image_cdg_pool_is_1024[(sizeof(cdg_slots) == 1024) ? 1 : -1];
typedef char staff_image_phase_is_2[(sizeof(staff_image_phase_a) == 2) ? 1 : -1];
typedef char staff_image_clear_is_1[(sizeof(staff_text_clear_requested) == 1) ? 1 : -1];
#endif
