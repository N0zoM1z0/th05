// Natural types and interfaces from pinned ReC98 th04/math/vector.hpp.
#ifndef TH05_SHARED_MATH_VECTOR_HPP
#define TH05_SHARED_MATH_VECTOR_HPP
#include <dos.h>
#include "src/shared/geometry.hpp"
extern "C" {
extern const short SinTable8[256];
extern const short CosTable8[256];
void pascal vector2_at(SPPoint near &ret, subpixel_t origin_x,
    subpixel_t origin_y, subpixel_t length, int angle);
}
int pascal polar(int center, int radius, int ratio);
#define polar_by_offset(center, radius, table, offset) ( \
    (static_cast<long>(radius) * *reinterpret_cast<const short *>( \
        reinterpret_cast<const signed char*>(table) + offset \
    ) >> 8) + center \
)
static inline pixel_t polar_x_fast_unsafe(
    pixel_t center, pixel_t &radius, uint16_t table_offset)
{
    return polar_by_offset(center, radius, CosTable8, table_offset);
}
static inline pixel_t polar_y_fast_unsafe(
    pixel_t center, pixel_t &radius, uint16_t table_offset)
{
    return polar_by_offset(center, radius, SinTable8, table_offset);
}
#endif
