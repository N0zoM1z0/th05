// Natural vector semantics from ReC98 b6ba5b0a th04/math/vector.hpp/vector2n.asm;
// the candidate's physical-register instructions and emitted bytes are omitted.
#pragma option -zCVECTOR2_NEAR_TEXT -zPmain_03
#include "src/shared/math/vector2_near.hpp"
#pragma codeseg VECTOR2_NEAR_TEXT main_03

extern "C" void pascal near vector2_near(
    SPPoint near &ret, unsigned char angle, subpixel_t length)
{
    // Both samples are read before either output store, as in the native body.
    const unsigned int table_offset = static_cast<unsigned int>(angle) * sizeof(short);
    const short cosine = *reinterpret_cast<const short *>(
        reinterpret_cast<const char *>(CosTable8) + table_offset);
    const short sine = *reinterpret_cast<const short *>(
        reinterpret_cast<const char *>(SinTable8) + table_offset);
    const subpixel_t x = static_cast<subpixel_t>(
        (static_cast<long>(length) * cosine) >> VECTOR2_TRIG_FRAC_BITS);
    const subpixel_t y = static_cast<subpixel_t>(
        (static_cast<long>(length) * sine) >> VECTOR2_TRIG_FRAC_BITS);
    ret.x.v = x;
    ret.y.v = y;
}
