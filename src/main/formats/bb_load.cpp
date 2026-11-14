// TH04 .BB allocation/loading flow, with TH05's unchecked direct DOS transfers.
#pragma option -zCBB_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/bb_load.hpp"

// TCC's __emit__ intrinsic keeps SI out of its automatic callee-save lowering.
// That lets the original near-Pascal epilogue restore SI before materializing
// the AX segment return value. The DOS transfers and pointer arithmetic remain
// ordinary C++/DOS intrinsics; only the four SI register operations are emitted.
void __emit__(uint8_t __byte, ...);

typedef char bb_filename_argument_is_4[(sizeof(const char far *) == 4) ? 1 : -1];
typedef char bb_payload_size_is_2048[(BB_SIZE == 2048) ? 1 : -1];

#pragma codeseg BB_LOAD_TEXT main_01

bb_tiles8_t __seg *pascal near bb_load(const char far *filename)
{
    // Save the caller's SI before allocation; the original DS is kept in SI.
    __emit__(0x56); // PUSH SI
    bb_load_seg = reinterpret_cast<bb_tiles8_t __seg *>(hmem_allocbyte(BB_SIZE));
    _BX = _SP;
    __emit__(0x8C, 0xDE); // MOV SI, DS
    _AX = 0x3D00;
    asm { lds dx, dword ptr ss:[bx+4]; }
    geninterrupt(0x21);
    _BX = _AX;
    __emit__(0x8E, 0xDE); // MOV DS, SI
    _DS = reinterpret_cast<unsigned int>(bb_load_seg);
    _CX = BB_SIZE;
    _DX = 0;
    _AH = 0x3F;
    geninterrupt(0x21);
    _AH = 0x3E;
    geninterrupt(0x21);
    __emit__(0x8E, 0xDE); // MOV DS, SI
    __emit__(0x5E); // POP SI, before the AX return load
    return bb_load_seg;
}
