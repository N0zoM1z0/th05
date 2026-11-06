// Same unchecked DOS transfer as the text masks, into the resident mask bank.
#pragma option -zCBB_CHEETO_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/bb_cheeto.hpp"
#pragma codeseg BB_CHEETO_LOAD_TEXT main_01

extern "C" void pascal near bb_cheeto_load(void)
{
    _AX = 0x3D00;
    reinterpret_cast<char near *>(_DX) = bb_cheeto_fn;
    geninterrupt(0x21);
    _BX = _AX;
    _AH = 0x3F;
    reinterpret_cast<bb_tiles8_t near *>(_DX) = bb_cheeto;
    _CX = BB_SIZE;
    geninterrupt(0x21);
    _AH = 0x3E;
    geninterrupt(0x21);
}
