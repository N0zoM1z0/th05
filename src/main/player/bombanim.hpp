// Bomb animation state shared by the four characters' bombs (ReC98
// th05/main/player/bombanim.cpp).
#ifndef TH05_MAIN_PLAYER_BOMBANIM_HPP
#define TH05_MAIN_PLAYER_BOMBANIM_HPP
#include "src/main/hud/overlay.hpp"

static const int REIMU_STAR_TRAILS = 6;
static const int REIMU_STAR_NODE_COUNT = 8;
static const int MARISA_LASER_COUNT = 8;
static const int MIMA_CIRCLE_COUNT = 8;
static const pixel_t REIMU_STAR_W = 64;
static const pixel_t REIMU_STAR_H = 64;
static const int BOMB_SCREEN_H = 400;
static const unsigned char BOMB_CIRCLE_FRAMES = 32;
static const int PAT_PLAYCHAR_BOMB_SHAPE = 179;

struct bomb_anim_t {
    point_t pos;
    int val1;
    int val2;
    unsigned char angle;
    signed char padding;
};
struct reimu_star_t {
    struct {
        Subpixel screen_x;
        Subpixel screen_y;
    } topleft;
    SPPoint velocity;
    unsigned char angle;
    signed char padding;
};
struct marisa_laser_t {
    SPPoint center;
    int unused;
    pixel_t radius;
    int padding;
};
// A point in screen pixels. Named apart from screen_point_t, which another
// header defines.
struct BombScreenPoint { int x; int y; };
struct mima_circle_t {
    BombScreenPoint center;
    int unused;
    pixel_t distance;
    unsigned char angle;
    signed char padding;
};
struct yuuka_heart_t {
    BombScreenPoint topleft;
    int unused;
    pixel_t distance;
    unsigned char angle;
    signed char padding;
};
union BombAnimation {
    reimu_star_t reimu[REIMU_STAR_TRAILS][REIMU_STAR_NODE_COUNT];
    marisa_laser_t marisa[MARISA_LASER_COUNT];
    mima_circle_t mima[MIMA_CIRCLE_COUNT];
    yuuka_heart_t yuuka;
};
extern BombAnimation bomb_anim;
extern unsigned char bomb_frame;
extern unsigned char stage_frame_mod8;

uint16_t pascal near randring1_next16_and(uint16_t mask);
uint16_t pascal near randring1_next16_mod(uint16_t divisor);
extern "C" {
    // Far Pascal: two far references for the results, then angle and length.
    void pascal far vector2(int far &x, int far &y,
        unsigned char angle, int length);
    void pascal far super_roll_put_1plane(int x, int y, int patnum,
        int pattern_plane, unsigned int put_plane);
}
void pascal far circles_add_growing(subpixel_t center_x, subpixel_t center_y);
void near reimu_stars_update_and_render(void);

typedef char bomb_generic_is_10[(sizeof(bomb_anim_t) == 10) ? 1 : -1];
typedef char bomb_star_is_10[(sizeof(reimu_star_t) == 10) ? 1 : -1];
typedef char bomb_star_velocity_at_4[(offsetof(reimu_star_t, velocity) == 4) ? 1 : -1];
typedef char bomb_star_angle_at_8[(offsetof(reimu_star_t, angle) == 8) ? 1 : -1];
typedef char bomb_star_padding_at_9[(offsetof(reimu_star_t, padding) == 9) ? 1 : -1];
typedef char bomb_laser_is_10[(sizeof(marisa_laser_t) == 10) ? 1 : -1];
typedef char bomb_laser_radius_at_6[(offsetof(marisa_laser_t, radius) == 6) ? 1 : -1];
typedef char bomb_circle_is_10[(sizeof(mima_circle_t) == 10) ? 1 : -1];
typedef char bomb_circle_distance_at_6[(offsetof(mima_circle_t, distance) == 6) ? 1 : -1];
typedef char bomb_heart_is_10[(sizeof(yuuka_heart_t) == 10) ? 1 : -1];
typedef char bomb_heart_angle_at_8[(offsetof(yuuka_heart_t, angle) == 8) ? 1 : -1];
typedef char bomb_animation_is_480[(sizeof(BombAnimation) == 480) ? 1 : -1];
#endif
