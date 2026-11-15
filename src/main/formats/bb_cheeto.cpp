// Loads the Extra-stage curved-bullet ("cheeto") masks from LS00.BB into the
// static bb_cheeto[] buffer.
#pragma option -zCBB_CHEETO_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/bb_cheeto.hpp"
#pragma codeseg BB_CHEETO_LOAD_TEXT main_01

extern "C" void pascal near bb_cheeto_load(void)
{
    // DOS file open (read-only). ZUN landmine: no error handling.
    _AX = 0x3D00;
    reinterpret_cast<char near *>(_DX) = bb_cheeto_fn;
    geninterrupt(0x21);
    _BX = _AX;
    // DOS file read of the whole 2 KiB payload, then close.
    _AH = 0x3F;
    reinterpret_cast<bb_tiles8_t near *>(_DX) = bb_cheeto;
    _CX = BB_SIZE;
    geninterrupt(0x21);
    _AH = 0x3E;
    geninterrupt(0x21);
}
