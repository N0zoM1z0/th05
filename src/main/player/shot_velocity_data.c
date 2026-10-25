/* Fixed-speed game motion lookup generated from mathematical Q8 directions. */
#pragma option -zCSHOT_VEL_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error This initialized semantic DATA producer requires C mode
#endif
#include "src/main/player/shot_velocity_data.h"

/* Twelve pixels per frame, in the game's sixteen-subpixels-per-pixel units. */
#define SHOT_SPEED_SUBPIXELS 192L
/* Explicit floor division preserves negative fixed-point quantization. */
#define VELOCITY_COMPONENT(q8) \
    ((int)(((q8) >= 0) ? (((q8) * SHOT_SPEED_SUBPIXELS) / 256L) : \
        -((-(q8) * SHOT_SPEED_SUBPIXELS + 255L) / 256L)))
#define VELOCITY_FROM_Q8(cosine, sine) \
    { VELOCITY_COMPONENT(cosine), VELOCITY_COMPONENT(sine) }

const ShotVelocityPoint near VELOCITY_192_AT_ANGLE[256] = {
#include "src/main/player/shot_velocity_q8.inc"
};

#undef VELOCITY_FROM_Q8
#undef VELOCITY_COMPONENT
#undef SHOT_SPEED_SUBPIXELS
