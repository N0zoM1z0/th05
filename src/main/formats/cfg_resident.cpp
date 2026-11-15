// Reads MIKO.CFG and returns the resident-structure segment stored in it.
// Adapted from ReC98 (th04/formats/cfg.hpp and th02/formats/cfg.hpp).
#pragma option -zCCFG_LRES_TEXT -k-

#include <dos.h>
#include "src/main/formats/cfg_resident.hpp"

static inline resident_t __seg *cfg_load_and_set_resident_dos(
    cfg_t near &cfg, const char near *fn
) {
    // DOS file open, read and close. ZUN landmine: no error handling; on a
    // failed read, the resident segment is whatever the buffer held before.
    _AX = 0x3d00;
    reinterpret_cast<const char near *>(_DX) = fn;
    geninterrupt(0x21);
    _BX = _AX;

    _AH = 0x3f;
    reinterpret_cast<cfg_t near *>(_DX) = &cfg;
    _CX = sizeof(cfg);
    geninterrupt(0x21);

    _AH = 0x3e;
    geninterrupt(0x21);

    resident = cfg.resident;
    return cfg.resident;
}

resident_t __seg *near cfg_load_resident_ptr(void)
{
    return cfg_load_and_set_resident_dos(cfg, CFG_FN);
}

// The original has a NOP padding byte after this function.
#pragma codestring "\x90"
