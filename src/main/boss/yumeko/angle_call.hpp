// Word-value view of the existing near Pascal aim-angle entry.
#ifndef TH05_YUMEKO_ANGLE_CALL_HPP
#define TH05_YUMEKO_ANGLE_CALL_HPP
// Native171CC reads X/Y at BP+8/+6, the angle byte at BP+4, and returns RET6.
// Each canonical Subpixel argument is one signed word, with no hidden pointer.
typedef unsigned char (pascal near *near YumekoAimWords)(
    subpixel_t x, subpixel_t y, unsigned char plus_angle);
typedef char yumeko_aim_pointer_is_near[(sizeof(YumekoAimWords) == 2) ? 1 : -1];
typedef char yumeko_aim_subpixel_is_word[(sizeof(Subpixel) == 2) ? 1 : -1];
#define yumeko_angle_from_xy(x_value, y_value, plus_value) \
    (reinterpret_cast<YumekoAimWords>(&player_angle_from)(x_value, y_value, plus_value))
#endif
