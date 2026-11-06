// Full active-spark motion, clipping, gravity and age update.
#pragma option -zCSPARK_UPDATE_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/effects/spark/lifecycle.hpp"
#pragma codeseg SPARK_UPDATE_TEXT main_01

extern "C" void near sparks_update(void)
{
    register spark_t near *spark;
    register int sparks_left;
    sparks_left = SPARK_COUNT;
    spark = sparks;
    do {
        if(spark->flag != F_FREE) {
            if(spark->flag != F_ALIVE) {
                spark->flag = F_FREE;
            } else {
                spark->center.update_seg1();
                // Consume both actual DX:AX Point-return words before a call.
                if(static_cast<uint16_t>(static_cast<subpixel_t>(_AX) +
                       ((SPARK_W / 2) * 16)) >= ((PLAYFIELD_W + SPARK_W) * 16) ||
                   static_cast<uint16_t>(static_cast<subpixel_t>(_DX) +
                       ((SPARK_H / 2) * 16)) >= ((PLAYFIELD_H + SPARK_H) * 16)) {
                    spark->flag = F_REMOVE;
                } else {
                    spark->center.velocity.y.v++;
                    spark->age++;
                    if(spark->age > 40) {
                        spark->flag = F_REMOVE;
                    }
                }
            }
        }
        spark++;
    } while(--sparks_left > 0);
}
