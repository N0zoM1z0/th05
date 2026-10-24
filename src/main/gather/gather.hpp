// Natural TH05 gather-circle ABI, corroborated by pinned ReC98 gather.hpp
// and the original operands. All fields are retained, with no offset padding.
#ifndef TH05_MAIN_GATHER_HPP
#define TH05_MAIN_GATHER_HPP

#include <dos.h>
#include "src/main/bullet/template.hpp"
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner is the TH05 MAIN gather implementation
#endif

typedef unsigned char vc_t;
typedef unsigned int vc2;
typedef int screen_x_t;
typedef int vram_y_t;
enum entity_flag_t {
    F_FREE = 0, F_ALIVE = 1, F_REMOVE = 2,
    _entity_flag_t_FORCE_UINT8 = 0xFF
};

struct gather_t {
    entity_flag_t flag;
    vc_t col;
    PlayfieldMotion center;
    Subpixel radius_cur;
    int ring_points;
    unsigned char angle_cur;
    unsigned char angle_delta;
    Subpixel radius_prev;
    Subpixel radius_delta;
    BulletTemplate bullet_template;
};
struct gather_template_t {
    PlayfieldPoint center;
    PlayfieldPoint velocity;
    Subpixel radius;
    int ring_points;
    vc_t col;
    unsigned char angle_delta;
};

#define GATHER_POINT_W 8
#define GATHER_POINT_H 8
#define GATHER_FRAMES 32
#define GATHER_COUNT 16
#define BST_NORMAL 0
#define BST_GATHER_NORMAL_SPECIAL_MOVE 0xFE
#define BST_GATHER_ONLY 0xFF
#define SEG_PLANE_B 0xA800
static const int GATHER_CAP = 8;

extern gather_t gather_circles[GATHER_COUNT];
extern gather_template_t gather_template;
extern BulletTemplate bullet_template;
extern PlayfieldPoint drawpoint;

// Real external assembly helpers. They remain unimplemented and uncredited.
void pascal near set_gather_template_to_bullet_template(gather_t near &gather);
void pascal near set_bullet_template_to_gather_template(gather_t near &gather);
void near grcg_setcolor_direct_seg3_raw(void); // Consumes the actual GRCG color in AH.
void __fastcall near gather_point_render(screen_x_t left, vram_y_t top);
extern "C" {
    void near bullets_add_regular(void);
    void near bullets_add_special(void);
    void pascal far vector2_at(SPPoint near &ret, subpixel_t origin_x,
        subpixel_t origin_y, subpixel_t length, int angle);
    vram_y_t pascal near scroll_subpixel_y_to_vram_seg3(subpixel_t y);
}

inline subpixel_t gather_to_sp(float pixel_value) {
    return static_cast<subpixel_t>(pixel_value * 16);
}
#define GATHER_RADIUS_END gather_to_sp(2.0f)
#define playfield_encloses_point(point, w, h) ( \
    (static_cast<subpixel_t>((point).x) > gather_to_sp(0 - ((w) / 2))) && \
    (static_cast<subpixel_t>((point).x) < gather_to_sp(384 + ((w) / 2))) && \
    (static_cast<subpixel_t>((point).y) > gather_to_sp(0 - ((h) / 2))) && \
    (static_cast<subpixel_t>((point).y) < gather_to_sp(368 + ((h) / 2))) \
)

// The reference point methods' genuine coordinate transforms, expressed as
// macros so the already accepted physical class declaration is unchanged.
#define gather_vram_top_scrolled(point, h) \
    scroll_subpixel_y_to_vram_seg3( \
        static_cast<subpixel_t>((point).y) + gather_to_sp(16 - ((h) / 2)) \
    )
#define gather_screen_left(point, w) \
    (32 + (static_cast<subpixel_t>((point).x) >> 4) - ((w) / 2))

typedef char th05_gather_flag_is_1[(sizeof(entity_flag_t) == 1) ? 1 : -1];
typedef char th05_gather_is_38[(sizeof(gather_t) == 38) ? 1 : -1];
typedef char th05_gather_center_at_2[(offsetof(gather_t, center) == 2) ? 1 : -1];
typedef char th05_gather_radius_at_14[(offsetof(gather_t, radius_cur) == 14) ? 1 : -1];
typedef char th05_gather_points_at_16[(offsetof(gather_t, ring_points) == 16) ? 1 : -1];
typedef char th05_gather_angle_at_18[(offsetof(gather_t, angle_cur) == 18) ? 1 : -1];
typedef char th05_gather_previous_at_20[(offsetof(gather_t, radius_prev) == 20) ? 1 : -1];
typedef char th05_gather_delta_at_22[(offsetof(gather_t, radius_delta) == 22) ? 1 : -1];
typedef char th05_gather_bullet_at_24[(offsetof(gather_t, bullet_template) == 24) ? 1 : -1];
typedef char th05_gather_template_is_14[(sizeof(gather_template_t) == 14) ? 1 : -1];

#endif
