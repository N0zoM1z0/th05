// Natural TH05 behavior from ReC98 th05/demo.cpp -> th04/main/demo.cpp,
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47. No instruction macro is retained.
#pragma option -zCDEMO_TEXT -zPmain_01
#include "src/main/demo/demo.hpp"

void near demo_load(void)
{
    size_t size = ((resident->demo_num <= 4)
        ? sizeof(REC<DEMO_N>)
        : sizeof(REC<DEMO_N_EXTRA>)
    );
    DemoBuf = static_cast<uint8_t far *>(hmem_allocbyte(size));
    char far *fn = demo_fn;
    fn[4] = ('0' - 1 + resident->demo_num);
    file_ropen(fn);
    file_read(DemoBuf, size);
    file_close();
}

void near DemoPlay(void)
{
    size_t shift_offset = (resident->demo_num <= 4) ? DEMO_N : DEMO_N_EXTRA;
    if((key_det & ~INPUT_MOVEMENT) == 0) {
        key_det = DemoBuf[stage_frame];
        shiftkey = DemoBuf[stage_frame + shift_offset];
        if((resident->demo_num > 4) || (stage_frame < (DEMO_N - 4))) {
            return;
        }
    }
    hmem_free(reinterpret_cast<void __seg *>(DemoBuf));
    palette_black_out(8);
    GameExecl(DEMOPLAY_BINARY_OP);
}
