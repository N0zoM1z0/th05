// Natural TH05 specialization of pinned ReC98 th04/math/vector.cpp.
#pragma option -zCSHARED
#include "src/shared/math/vector.hpp"
int pascal polar(int center, int radius, int ratio)
{
    return (((static_cast<long>(radius) * ratio) >> 8) + center);
}
void pascal vector2_at(SPPoint near &ret, subpixel_t origin_x,
    subpixel_t origin_y, subpixel_t length, int angle)
{
    _BX = angle;
    _BH ^= _BH;
    _BX += _BX;
    ret.x.v = polar_x_fast_unsafe(origin_x, length, _BX);
    ret.y.v = polar_y_fast_unsafe(origin_y, length, _BX);
}
