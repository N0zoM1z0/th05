// EGC copy of a 16-dot-aligned rectangle from VRAM page 1 to page 0,
// after ReC98 th04/hardware/egcrect.cpp (TH05 variant).
#pragma option -zCSHARED
#include <dos.h>
#pragma codeseg SHARED

extern "C" void pascal far egc_off(void);
void near egc_rect_setup(void);
extern unsigned int egcrect_w;

static const unsigned int SEG_PLANE_B = 0xA800;
static const unsigned int PLANE_SIZE = (80 * 400);
static const int ROW_WORDS = (80 / 2);

void pascal far egc_copy_rect_1_to_0_16(int left, int top, int w, int h)
{
    #define vo_tmp         _BX
    #define first_bit      _CX
    #define stride         static_cast<int>(_BP)
    #define w_tmp          _AX
    #define rows_remaining static_cast<int>(_BX)
    #define dots           _DX

    egc_rect_setup();

    // EGC_COMPAREREAD | EGC_WS_ROP | EGC_RL_MEMREAD | 0xF0
    _DX = 0x04A4;
    _AX = 0x29F0;
    asm { out dx, ax }

    // Inline assembly keeps the parameters out of SI.
    asm { mov ax, left; }
    asm { mov dx, top; }

    vo_tmp = _AX;
    static_cast<int>(vo_tmp) >>= 4;
    asm { shl bx, 1; }
    _DX <<= 6;
    vo_tmp += _DX;
    _DX >>= 2;
    vo_tmp += _DX;

    _DI = vo_tmp;
    _AX &= 0x0F;
    first_bit = _AX;

    w_tmp = ((_AX + w) >> 4);
    if(first_bit) {
        w_tmp++;
    }
    egcrect_w = w_tmp;

    _CX = ROW_WORDS;
    _CX -= w_tmp;
    asm { shl cx, 1; }
    rows_remaining = h;
    stride = _CX;
    _ES = SEG_PLANE_B;

    do {
        _CX = egcrect_w;
        put_loop: {
            _DI |= _DI;
            if(!(_FLAGS & 0x80) && (_DI < PLANE_SIZE)) {
                _AL = 1;
                asm { out 0A6h, al }
                dots = peek(_ES, _DI);
                _AX ^= _AX;
                asm { out 0A6h, al }
                *reinterpret_cast<int far *>(MK_FP(_ES, _DI)) = dots;
            }
            _DI += 2;
            asm { loop put_loop; }
        }
        _DI += stride;
        rows_remaining--;
    } while(!(_FLAGS & 0x80));
    egc_off();

    #undef dots
    #undef rows_remaining
    #undef w_tmp
    #undef stride
    #undef first_bit
    #undef vo_tmp
}
#pragma codestring "\x90"
