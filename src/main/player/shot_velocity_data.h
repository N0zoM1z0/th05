/* Complete mathematical velocity records consumed as signed Q12.4 words. */
#ifndef TH05_SHOT_VELOCITY_DATA_H
#define TH05_SHOT_VELOCITY_DATA_H
#include <stddef.h>
typedef struct ShotVelocityPoint {
    int x;
    int y;
} ShotVelocityPoint;
extern const ShotVelocityPoint near VELOCITY_192_AT_ANGLE[256];
typedef char shot_velocity_word2[(sizeof(int) == 2) ? 1 : -1];
typedef char shot_velocity_point4[(sizeof(ShotVelocityPoint) == 4) ? 1 : -1];
typedef char shot_velocity_x0[(offsetof(ShotVelocityPoint, x) == 0) ? 1 : -1];
typedef char shot_velocity_y2[(offsetof(ShotVelocityPoint, y) == 2) ? 1 : -1];
typedef char shot_velocity_table1024[(sizeof(VELOCITY_192_AT_ANGLE) == 1024) ? 1 : -1];
#endif
