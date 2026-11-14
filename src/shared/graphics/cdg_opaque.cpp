// Opaque CDG blit of all four planes, after ReC98 th04/formats/cdg_p_na.cpp
// (linked into TH05 OP, MAIN and MAINE).
#pragma option -zCSHARED
#include <dos.h>
#include "src/shared/abi.hpp"
#pragma codeseg SHARED

struct CDG {
    uint16_t bitplane_size;
    int pixel_w;
    int pixel_h;
    int offset_at_bottom_left;
    uint16_t vram_dword_w;
    uint8_t image_count;
    signed char plane_layout;
    unsigned int seg_alpha;
    unsigned int seg_colors;
};
extern CDG cdg_slots[64];

static const unsigned int SEG_PLANE_B = 0xA800;
static const unsigned int SEG_PLANE_E = 0xE000;
static const unsigned int SEG_PLANE_DIST_E = 0x2800;
static const unsigned int SEG_PLANE_DIST_BRG = 0x0800;
static const int ROW_SIZE = 80;
static const int PLANE_COUNT = 4;

void pascal far cdg_put_noalpha_8(int left, int top, int slot)
{
    #define cdg         reinterpret_cast<CDG near *>(_SI)
    #define tmp         static_cast<unsigned int>(_AX)
    #define cdg_dword_w static_cast<int>(_BP)
    #define dst_offset  static_cast<int>(_BX)
    #define planes_left static_cast<char>(_AL)
    register int stride;

    asm { push ds; }

    // ES = SEG_PLANE_B + (top * (ROW_SIZE / 16)), then stack E, G and R.
    _AX = top;
    _BX = _AX;
    _AX = (((_AX * 4) + _BX) + SEG_PLANE_B);
    _ES = _AX;
    _AX += (SEG_PLANE_E - SEG_PLANE_B);
    asm { push ax; }
    _AX -= SEG_PLANE_DIST_E;
    asm { push ax; }
    _AX -= SEG_PLANE_DIST_BRG;
    asm { push ax; }

    _SI = slot;
    _SI <<= 4;
    _SI += FP_OFF(cdg_slots);
    dst_offset = left;
    dst_offset >>= 3;
    dst_offset += cdg->offset_at_bottom_left;

    tmp = cdg->vram_dword_w;
    cdg_dword_w = tmp;
    // One more full line: each row moves from the end of one CDG line to
    // the start of the previous one.
    stride = ((tmp * 4) + ROW_SIZE);

    tmp = cdg->seg_colors;
    _DS = tmp;
    _SI = 0;
    planes_left = PLANE_COUNT;
    asm { cld; }
    asm { nop; }
    do {
        _DI = dst_offset;
        do {
            _CX = cdg_dword_w;
            asm { rep movsd; }
            _DI -= stride;
        } while(!(_FLAGS & 0x80));
        // SI is now at the start of the next plane.
        --planes_left;
        if(_FLAGS & 0x40) {
            break;
        }
        asm { pop es; }
    } while(1);

    asm { pop ds; }

    #undef planes_left
    #undef dst_offset
    #undef cdg_dword_w
    #undef tmp
    #undef cdg
}
#pragma codestring "\x90"
