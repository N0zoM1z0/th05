// TH03/TH05 vector pair, native far Pascal ABI and 32-bit signed products.
#pragma option -zCSHARED
#include <dos.h>
extern "C" {
    extern const short SinTable8[256];
    extern const short CosTable8[256];
    int pascal far iatan2(int y, int x);
    void pascal far vector2(int &ret_x, int &ret_y, unsigned char angle, int length);
    void pascal far vector2_between_plus(int x1, int y1, int x2, int y2,
        unsigned char plus_angle, int &ret_x, int &ret_y, int length);
}
void pascal far vector2_between_plus(int x1, int y1, int x2, int y2,
    unsigned char plus_angle, int &ret_x, int &ret_y, int length)
{
    _SI = length;
    _DL = static_cast<unsigned char>(iatan2(y2 - y1, x2 - x1) + plus_angle);
    _EAX = static_cast<signed int>(_SI);
    _DH = 0;
    _DX += _DX;
    _BX = _DX;
    asm {
        movsx edx, word ptr [bx + CosTable8]
        movsx ecx, word ptr [bx + SinTable8]
    }
    ret_x = static_cast<int>(static_cast<signed long>(_EAX * _EDX) >> 8);
    ret_y = static_cast<int>((static_cast<signed long>(static_cast<signed int>(_SI)) * static_cast<signed long>(_ECX)) >> 8);
}
