// MAP format/flow: maintained TH04 src/main/formats/map.cpp and ReC98
// b6ba5b0a th04/formats/map.hpp. TH05 uses unchecked direct DOS transfers.
#pragma option -zCMAP_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/map_load.hpp"
#pragma codeseg MAP_LOAD_TEXT main_01

void near map_load(void)
{
    register int handle;

    map_free();
    map_fn[3] = ('0' + stage_id);

    _AX = 0x3D00;
    reinterpret_cast<char near *>(_DX) = map_fn;
    geninterrupt(0x21);
    _BX = _AX;
    handle = _AX;

    _AH = 0x3F;
    reinterpret_cast<map_header_t near *>(_DX) = &map_header;
    _CX = sizeof(map_header);
    geninterrupt(0x21);

    map_seg = reinterpret_cast<map_section_tiles_t __seg *>(
        hmem_allocbyte(map_header.size)
    );
    // DOS reads into DS:DX. Preserve the game's DS around the segment switch.
    asm { push ds; }
    _BX = handle;
    _CX = map_header.size;
    // The allocator's actual segment result is still in AX. BX/CX transport
    // above does not overwrite it; avoid rereading the stored segment handle.
    _DS = _AX;
    _DX = 0;
    _AH = 0x3F;
    geninterrupt(0x21);
    asm { pop ds; }

    _AH = 0x3E;
    geninterrupt(0x21);
}
