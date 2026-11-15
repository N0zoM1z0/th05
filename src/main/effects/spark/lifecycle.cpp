// Spark initialization and tile invalidation (ReC98 th04/main/sparks.asm).
//
// ZUN bug: both functions walk 96 sparks although the pool only has 64, so
// they also touch the 512 bytes that follow `sparks` in memory.
#pragma option -zCSPARK_LIFE_TEXT -zPmain_01 -k-
#include "src/main/effects/spark/lifecycle.hpp"

// tiles_invalidate_around() takes its 4-byte point by value on the stack and
// pops it with RET 4. Calling it through this pointer type passes the point
// the same way the original does (enemy invalidation uses the same trick).
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
        // Only the low byte of the 16-bit angle is randomized.
        *reinterpret_cast<unsigned char near *>(&spark->angle) =
            static_cast<unsigned char>(irand());
        spark++;
    } while(--sparks_left != 0);
    // ZUN quirk: like the angles above, only the low byte of this 16-bit
    // variable is cleared.
    *reinterpret_cast<unsigned char near *>(&spark_ring_offset) = 0;
}
