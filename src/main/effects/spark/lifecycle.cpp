// Semantic donor: maintained TH04 spark/init.cpp and spark/invalidate.cpp.
// TH05 keeps the original 96-entry traversal despite its 64-entry active pool.
#pragma option -zCSPARK_LIFE_TEXT -zPmain_01 -k-
#include "src/main/effects/spark/lifecycle.hpp"

// The existing canonical tile entry consumes four actual point bytes and
// RET4. Reuse the reviewed legacy Borland by-value view, as in enemy invalidation.
typedef void (near pascal *near SparkPointInvalidation)(const SPPoint center);
typedef char spark_point_call_is_near[(sizeof(SparkPointInvalidation) == 2) ? 1 : -1];

void near sparks_invalidate(void)
{
    register spark_t near *spark;
    register int sparks_left;
    *reinterpret_cast<uint32_t near *>(&tile_invalidate_box) =
        (static_cast<uint32_t>(SPARK_H) << 16) | SPARK_W;
    sparks_left = SPARK_COUNT_BUG;
    spark = sparks;
    do {
        if(spark->flag != F_FREE) {
            reinterpret_cast<SparkPointInvalidation>(
                &tiles_invalidate_around)(spark->center.prev);
        }
        spark++;
    } while(--sparks_left > 0);
}

extern "C" void near sparks_init(void)
{
    register spark_t near *spark;
    register int sparks_left;
    spark = sparks;
    sparks_left = SPARK_COUNT_BUG;
    do {
        *reinterpret_cast<unsigned char near *>(&spark->angle) =
            static_cast<unsigned char>(irand());
        spark++;
    } while(--sparks_left != 0);
    // The original writes only the low byte of this genuine word object.
    *reinterpret_cast<unsigned char near *>(&spark_ring_offset) = 0;
}
