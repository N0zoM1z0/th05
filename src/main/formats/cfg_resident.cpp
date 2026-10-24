// Candidate adapted from nmlgc/ReC98@b6ba5b0a; not accepted before cold replay.
#pragma option -zCCFG_LRES_TEXT -k-

#include <dos.h>
#include "src/main/formats/cfg_resident.hpp"

static inline resident_t __seg *cfg_load_and_set_resident_dos(
    cfg_t near &cfg, const char near *fn
) {
    // Preserve the original raw DOS error behavior: open/read failures are
    // not checked before consuming the resident segment in the CFG buffer.
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

// Observed trailing alignment byte; check it, but exclude instruction credit.
#pragma codestring "\x90"
