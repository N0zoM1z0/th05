// Loads the text-dissolve masks into one 3 KiB segment: TXT1.BB (2 KiB) at
// offset 0, then TXT2.BB (1 KiB) right after it. Same flow as TH04, but with
// direct DOS calls. ZUN landmine: none of the DOS results are checked.
#pragma option -zCBB_TEXT_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/bb_text.hpp"
#pragma codeseg BB_TEXT_LOAD_TEXT main_01

extern "C" void pascal near bb_txt_load(void)
{
    bb_txt_seg = reinterpret_cast<bb_tiles8_t __seg *>(
        hmem_allocbyte(BB_SIZE + (BB_SIZE / 2)));

    _AX = 0x3D00;
    reinterpret_cast<char near *>(_DX) = bb_txt_fn;
    geninterrupt(0x21);
    _BX = _AX;
    // DOS reads into DS:DX, so point DS at the new segment for the read.
    asm { push ds; }
    _DS = reinterpret_cast<unsigned int>(bb_txt_seg);
    _CX = BB_SIZE;
    _DX = 0;
    _AH = 0x3F;
    geninterrupt(0x21);
    asm { pop ds; }
    _AH = 0x3E;
    geninterrupt(0x21);

    // Same filename buffer, now "txt2.bb".
    bb_txt_fn[3] = '2';
    _AX = 0x3D00;
    reinterpret_cast<char near *>(_DX) = bb_txt_fn;
    geninterrupt(0x21);
    _BX = _AX;
    asm { push ds; }
    _DS = reinterpret_cast<unsigned int>(bb_txt_seg);
    _CX = BB_SIZE / 2;
    _DX = BB_SIZE;
    _AH = 0x3F;
    geninterrupt(0x21);
    asm { pop ds; }
    _AH = 0x3E;
    geninterrupt(0x21);
}

extern "C" void pascal near bb_txt_free(void)
{
    if(bb_txt_seg) {
        hmem_free(bb_txt_seg);
        bb_txt_seg = 0;
    }
}
