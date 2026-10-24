// Candidate declarations adapted from nmlgc/ReC98@b6ba5b0a529edbb3:
// th01/math/subpixel.hpp, th04/math/motion.hpp, th04/main/playfld.hpp.
// Retain the class identities because they enter Borland's C++ symbol names.
#ifndef TH05_SHARED_GEOMETRY_HPP
#define TH05_SHARED_GEOMETRY_HPP

#include "src/shared/abi.hpp"

typedef int subpixel_t;
typedef uint8_t subpixel_length_8_t;

template <class SubpixelType, class PixelType> class SubpixelBase {
public:
    typedef SubpixelBase<SubpixelType, PixelType> SelfType;
    SubpixelType v;

    SubpixelType operator -(const SelfType &other) const {
        return (this->v - other.v);
    }

    operator SubpixelType() const {
        return v;
    }
};

typedef SubpixelBase<subpixel_t, pixel_t> Subpixel;
typedef SubpixelBase<subpixel_length_8_t, pixel_length_8_t> SubpixelLength8;

template <class T> struct SPPointBase {
    T x;
    T y;
};

struct SPPoint : public SPPointBase<Subpixel> {
};

struct PlayfieldPoint : public SPPoint {
};

// Real motion state, rather than a shortened view of the current coordinates.
// The near qualification belongs to the original template type.
template <class PointType> struct near MotionBase {
    PointType cur;
    PointType prev;
    PointType velocity;
};

struct PlayfieldMotion : public MotionBase<PlayfieldPoint> {
    PlayfieldPoint pascal near update_seg1();
    PlayfieldPoint pascal near update_seg3();
};

typedef char th05_subpixel_is_2[(sizeof(Subpixel) == 2) ? 1 : -1];
typedef char th05_subpixel_byte_is_1[(sizeof(SubpixelLength8) == 1) ? 1 : -1];
typedef char th05_point_is_4[(sizeof(PlayfieldPoint) == 4) ? 1 : -1];
typedef char th05_point_x_at_0[(offsetof(PlayfieldPoint, x) == 0) ? 1 : -1];
typedef char th05_point_y_at_2[(offsetof(PlayfieldPoint, y) == 2) ? 1 : -1];
typedef char th05_motion_is_12[(sizeof(PlayfieldMotion) == 12) ? 1 : -1];
typedef char th05_motion_cur_at_0[(offsetof(PlayfieldMotion, cur) == 0) ? 1 : -1];
typedef char th05_motion_prev_at_4[(offsetof(PlayfieldMotion, prev) == 4) ? 1 : -1];
typedef char th05_motion_velocity_at_8[(offsetof(PlayfieldMotion, velocity) == 8) ? 1 : -1];

#endif
