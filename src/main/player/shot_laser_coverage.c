/* Five 8-pixel horizontal occupancy rows used by the active shot laser. */
#pragma option -zCSHOT_LASER_COVERAGE_TEXT -zPmain_01
#ifdef __cplusplus
#error Native raster-coverage DATA must be compiled as C
#endif

/* Centered beam grows through two, four and six occupied pixels before
 * the two disconnected edge positions of its fourth animation cel. */
#define LASER_ROW_FULL 0xffU
#define LASER_CENTER_WIDTH(n) (((1U << (n)) - 1U) << ((8U - (n)) / 2U))
#define LASER_FOURTH_CEL_GAPS ((1U << 6) | (1U << 1))

enum ShotLaserCoverageCel {
    SHOT_LASER_CEL_COUNT = 5,
    SHOT_LASER_NARROW_WIDTH = 2,
    SHOT_LASER_MEDIUM_WIDTH = 4,
    SHOT_LASER_WIDE_WIDTH = 6
};

unsigned char near SHOT_LASER_DOTS[SHOT_LASER_CEL_COUNT] = {
    LASER_CENTER_WIDTH(SHOT_LASER_NARROW_WIDTH),
    LASER_CENTER_WIDTH(SHOT_LASER_MEDIUM_WIDTH),
    LASER_CENTER_WIDTH(SHOT_LASER_WIDE_WIDTH),
    LASER_ROW_FULL ^ LASER_FOURTH_CEL_GAPS,
    LASER_ROW_FULL
};

typedef char shot_laser_five_coverages[(sizeof(SHOT_LASER_DOTS) == 5) ? 1 : -1];
#undef LASER_ROW_FULL
#undef LASER_CENTER_WIDTH
#undef LASER_FOURTH_CEL_GAPS
