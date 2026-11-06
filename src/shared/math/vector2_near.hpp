// Canonical TH04/TH05 near vector interface; no table or result storage owned.
#ifndef TH05_SHARED_VECTOR2_NEAR_HPP
#define TH05_SHARED_VECTOR2_NEAR_HPP
#include "src/shared/math/vector.hpp"

static const int VECTOR2_TRIG_FRAC_BITS = 8;
#pragma codeseg VECTOR2_NEAR_TEXT main_03
extern "C" void pascal near vector2_near(
    SPPoint near &ret, unsigned char angle, subpixel_t length);
#pragma codeseg

typedef char vector2_near_point_is_4[(sizeof(SPPoint) == 4) ? 1 : -1];
typedef char vector2_near_length_is_2[(sizeof(subpixel_t) == 2) ? 1 : -1];
#endif
