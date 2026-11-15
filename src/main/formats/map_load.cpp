// Loads the current stage's .MAP file (tile sections) into its own segment.
// Same flow as TH04's map_load() (ReC98 th04/formats/map.hpp), but TH05 uses
// direct DOS calls. ZUN landmine: none of the DOS results are checked.
#pragma option -zCMAP_LOAD_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/main/formats/map_load.hpp"
#pragma codeseg MAP_LOAD_TEXT main_01

void near map_load(void)
{
    register int handle;

    map_free();
    map_fn[3] = ('0' + stage_id);

    // DOS file open (read-only)
    _AX = 0x3D00;
    reinterpret_cast<char near *>(_DX) = map_fn;
    geninterrupt(0x21);
    _BX = _AX;
    handle = _AX;

    // DOS file read: the header, which holds the size of the section data.
    _AH = 0x3F;
    reinterpret_cast<map_header_t near *>(_DX) = &map_header;
    _CX = sizeof(map_header);
    geninterrupt(0x21);

    map_seg = reinterpret_cast<map_section_tiles_t __seg *>(
        hmem_allocbyte(map_header.size)
    );
    // DOS file read of the sections into the new segment. DOS reads into
    // DS:DX, so DS is switched to that segment for the read.
    asm { push ds; }
    _BX = handle;
    _CX = map_header.size;
    // AX still holds hmem_allocbyte()'s result. Assigning DS from map_seg
    // instead would reload it from memory and add two bytes.
    _DS = _AX;
    _DX = 0;
    _AH = 0x3F;
    geninterrupt(0x21);
    asm { pop ds; }

    _AH = 0x3E;
    geninterrupt(0x21);
}
