// Complete original 56-byte EGC hardware copy of the 384x368 playfield.
// ReC98 preserves the page-select, register and 16-bit row-loop semantics.
#pragma option -zCDIALOG_RUN_TEXT -zPmain_01
#include <dos.h>
#include "src/main/dialog/runtime.hpp"
#pragma codeseg DIALOG_RUN_TEXT main_01
void near egc_start_copy_noframe(void);
extern "C" void pascal far egc_off(void);
extern unsigned char page_front;
void near playfield_copy_front_to_back(void)
{
    egc_start_copy_noframe();
    _ES = 0xa850;
    _DI = 0x72b4;
    _DX = 0xa6;
    _AL = page_front;
    box_copy_next_row:
        _CX = 24;
    box_copy_next_word:
        outportb(_DX, _AL);
        _AL ^= 1;
        _BX = *reinterpret_cast<unsigned short __es *>(_DI);
        outportb(_DX, _AL);
        _AL ^= 1;
        *reinterpret_cast<unsigned short __es *>(_DI) = _BX;
        _DI += 2;
        asm { loop box_copy_next_word; }
        asm {
            sub di, 0x80
            jge box_copy_next_row
        }
    outportb(_DX, _AL);
    egc_off();
}
