// Complete point-popup update with scalar field types and rise assignment.
#pragma option -zCPOINTNUM_LIFE_TEXT -zPmain_01 -k-
#include "src/main/pointnum/lifecycle.hpp"
#pragma codeseg POINTNUM_LIFE_TEXT main_01

extern "C" void pascal near pointnums_update(void)
{
    register pointnum_t near *pointnum;
    register int remaining;
    pointnum_t near * near *alive;
    unsigned char age;

    pointnum_first_yellow_alive = 0;
    alive = pointnums_alive;
    pointnum = pointnums;
    remaining = POINTNUM_COUNT;
    do {
        if(pointnum->flag != F_FREE) {
            if(static_cast<unsigned char>(pointnum->flag) == F_REMOVE) {
                pointnum->flag = F_FREE;
            } else {
                age = pointnum->age;
                pointnum->center_prev_y.v = pointnum->center_cur.y.v;
                if((pointnum->center_cur.y.v =
                       ((age >= POINTNUM_RISE_AGE)
                           ? (pointnum->center_cur.y.v - to_sp(0.5f))
                           : pointnum->center_cur.y.v)) <= TO_SP(-(POINTNUM_H / 2))) {
                    pointnum->flag = F_REMOVE;
                } else {
                    age++;
                    pointnum->age = age;
                    if(age > POINTNUM_LAST_AGE) {
                        pointnum->flag = F_REMOVE;
                    } else {
                        *alive = pointnum;
                        if(static_cast<unsigned int>(remaining) <= POINTNUM_YELLOW_COUNT && !pointnum_first_yellow_alive) {
                            pointnum_first_yellow_alive = pointnum;
                        }
                        alive++;
                    }
                }
            }
        }
        pointnum++;
    } while(--remaining != 0);
    *alive = 0;
}
