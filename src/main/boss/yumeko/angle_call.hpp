// Calls player_angle_from() with X and Y as plain subpixel words.
#ifndef TH05_YUMEKO_ANGLE_CALL_HPP
#define TH05_YUMEKO_ANGLE_CALL_HPP
// player_angle_from() takes two Subpixel values, which are single words on the
// stack. Passing an `x.v + to_sp(64)` expression through the Subpixel signature
// would first store it in a Subpixel temporary, an instruction that ZUN's code
// doesn't have.
typedef unsigned char (pascal near *near YumekoAimWords)(
    subpixel_t x, subpixel_t y, unsigned char plus_angle);
typedef char yumeko_aim_pointer_is_near[(sizeof(YumekoAimWords) == 2) ? 1 : -1];
typedef char yumeko_aim_subpixel_is_word[(sizeof(Subpixel) == 2) ? 1 : -1];
#define yumeko_angle_from_xy(x_value, y_value, plus_value) \
    (reinterpret_cast<YumekoAimWords>(&player_angle_from)(x_value, y_value, plus_value))
#endif
