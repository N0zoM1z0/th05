// Candidate ABI and shot iteration adapted from nmlgc/ReC98@b6ba5b0a529edbb3:
// th04/main/player/shot.hpp, th05/main/player/shot.hpp, th03/math/randring.hpp
// and th02/main/entity.hpp. All Shot fields retain their original types/layout.
#ifndef TH05_MAIN_PLAYER_REIMU_HPP
#define TH05_MAIN_PLAYER_REIMU_HPP

#include "src/shared/geometry.hpp"

enum entity_flag_t {
    F_FREE = 0,
    F_ALIVE = 1,
    F_REMOVE = 2,
    _entity_flag_t_FORCE_UINT8 = 0xff
};

#define ST_NORMAL 0
#define ST_HOMING 1
#define ST_MISSILE_LEFT 2
#define ST_MISSILE_RIGHT 3
#define ST_MISSILE_STRAIGHT 4
#define SC_1X 0x8
#define SC_2X 0x2
#define SC_3X 0x1
#define SC_6X 0x4

static const pixel_t PLAYER_OPTION_DISTANCE = ((32 / 2) + (16 / 2));
static const char PAT_SHOT_SUB = 22;

uint16_t pascal near randring1_next16_and(uint16_t mask);

inline uint8_t randring1_next8_ge_lt(uint8_t min, uint8_t max) {
    return (min + randring1_next16_and((max - min) - 1));
}

SPPoint pascal near shot_velocity_set(SPPoint near *velocity, unsigned char angle);

struct Shot {
    entity_flag_t flag;
    char age;
    PlayfieldMotion pos;
    char patnum_base;
    char type;
    char damage;
    char angle;

    void from_option_l(float offset = 0.0f) {
        // Same Q12.4 subtraction as the original Subpixel operator-=, without
        // expanding an already accepted shared class definition.
        this->pos.cur.x.v -= static_cast<subpixel_t>((PLAYER_OPTION_DISTANCE + offset) * 16);
    }

    void from_option_r(float offset = 0.0f) {
        this->pos.cur.x.v += static_cast<subpixel_t>((PLAYER_OPTION_DISTANCE + offset) * 16);
    }

    void set_option_sprite() {
        this->patnum_base = PAT_SHOT_SUB;
    }

    void set_option_sprite_and_damage(char damage) {
        set_option_sprite();
        this->damage = damage;
    }

    void set_random_angle_forwards(unsigned char min = -0x48, unsigned char max = -0x38) {
        shot_velocity_set((SPPoint near *)&this->pos.velocity, randring1_next8_ge_lt(min, max));
    }
};

Shot near *near shots_add(void);
char near shot_cycle_init(void);

struct ShotAddIterator {
    unsigned char angle;
    unsigned char i;

    ShotAddIterator(unsigned char count) : i(count) {
    }

    void add_secondary(unsigned char n) {
        i += n;
    }

    void set_random_angle(unsigned char min = -0x48, unsigned char max = -0x38) {
        angle = randring1_next8_ge_lt(min, max);
    }

    unsigned char next(void) {
        return i -= 1;
    }
};

#define shot_func_init(shot, sai, cycle, count, primary_cycle, secondary_cycle, secondary_offset_expr) \
    Shot near *shot; \
    ShotAddIterator sai(count); \
    cycle = shot_cycle_init(); \
    if((cycle & (primary_cycle | secondary_cycle)) == 0) { \
        return; \
    } \
    if(cycle & secondary_cycle) { \
        sai.secondary_offset_expr; \
    }

extern "C" {
    void pascal near shot_reimu_l2(void);
    void pascal near shot_reimu_l3(void);
    void pascal near shot_reimu_l4(void);
    void pascal near shot_reimu_l5(void);
    void pascal near shot_reimu_l6(void);
    void pascal near shot_reimu_l7(void);
    void pascal near shot_reimu_l8(void);
    void pascal near shot_reimu_l9(void);
}

typedef char th05_reimu_entity_flag_is_1[(sizeof(entity_flag_t) == 1) ? 1 : -1];
typedef char th05_reimu_shot_is_18[(sizeof(Shot) == 18) ? 1 : -1];
typedef char th05_reimu_shot_flag_at_0[(offsetof(Shot, flag) == 0) ? 1 : -1];
typedef char th05_reimu_shot_age_at_1[(offsetof(Shot, age) == 1) ? 1 : -1];
typedef char th05_reimu_shot_pos_at_2[(offsetof(Shot, pos) == 2) ? 1 : -1];
typedef char th05_reimu_shot_sprite_at_14[(offsetof(Shot, patnum_base) == 14) ? 1 : -1];
typedef char th05_reimu_shot_type_at_15[(offsetof(Shot, type) == 15) ? 1 : -1];
typedef char th05_reimu_shot_damage_at_16[(offsetof(Shot, damage) == 16) ? 1 : -1];
typedef char th05_reimu_shot_angle_at_17[(offsetof(Shot, angle) == 17) ? 1 : -1];
typedef char th05_reimu_iterator_is_2[(sizeof(ShotAddIterator) == 2) ? 1 : -1];
typedef char th05_reimu_iterator_angle_at_0[(offsetof(ShotAddIterator, angle) == 0) ? 1 : -1];
typedef char th05_reimu_iterator_index_at_1[(offsetof(ShotAddIterator, i) == 1) ? 1 : -1];
typedef char th05_reimu_shot_pointer_is_2[(sizeof(Shot near *) == 2) ? 1 : -1];

#endif
