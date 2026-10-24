// Full spark storage and real interfaces, corroborated by pinned ReC98
// th04/main/spark.hpp and the maintained TH04 reconstruction's natural C++.
#ifndef TH05_SPARK_LIFECYCLE_HPP
#define TH05_SPARK_LIFECYCLE_HPP
#include "src/main/player/reimu.hpp"
#include "src/main/hud/overlay.hpp"

struct spark_t {
    entity_flag_t flag;
    unsigned char age;
    PlayfieldMotion center;
    unsigned int angle;
};
static const int SPARK_COUNT = 64;
static const int SPARK_COUNT_BUG = 96;
static const pixel_t SPARK_W = 8;
static const pixel_t SPARK_H = 8;
extern spark_t sparks[SPARK_COUNT];
extern uint16_t spark_ring_offset;

#pragma codeseg _TEXT
extern "C" int pascal far irand(void);
#pragma codeseg SPARK_LIFE_TEXT main_01
extern "C" void near sparks_init(void);
void near sparks_invalidate(void);

typedef char spark_record_is_16[(sizeof(spark_t) == 16) ? 1 : -1];
typedef char spark_motion_at_2[(offsetof(spark_t, center) == 2) ? 1 : -1];
typedef char spark_angle_at_14[(offsetof(spark_t, angle) == 14) ? 1 : -1];
typedef char spark_pool_is_1024[(sizeof(sparks) == 1024) ? 1 : -1];
typedef char spark_box_is_4[(sizeof(point_t) == 4) ? 1 : -1];
#endif
