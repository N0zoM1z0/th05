// Demo (attract mode) replays: loading DEMO?.REC and feeding its inputs to
// the game. Same as the TH05 branch of ReC98's th04/main/demo.cpp.
#pragma option -zCDEMO_TEXT -zPmain_01
#include "src/main/demo/demo.hpp"

// Demos 1-4 hold DEMO_N frames, demo 5 (Extra Stage) DEMO_N_EXTRA.
void near demo_load(void)
{
    size_t size = ((resident->demo_num <= 4)
        ? sizeof(REC<DEMO_N>)
        : sizeof(REC<DEMO_N_EXTRA>)
    );
    DemoBuf = static_cast<uint8_t far *>(hmem_allocbyte(size));
    char far *fn = demo_fn;
    fn[4] = ('0' - 1 + resident->demo_num); // demo_num is 1-based
    file_ropen(fn);
    file_read(DemoBuf, size);
    file_close();
}

// Input hook during demos. Ends the demo and returns to OP once the replay
// runs out or a non-movement key is pressed.
void near DemoPlay(void)
{
    size_t shift_offset = (resident->demo_num <= 4) ? DEMO_N : DEMO_N_EXTRA;
    // Unlike TH04, the movement keys don't end the demo.
    if((key_det & ~INPUT_MOVEMENT) == 0) {
        key_det = DemoBuf[stage_frame];
        shiftkey = DemoBuf[stage_frame + shift_offset];
        // Demos 1-4 end 4 frames before their recording runs out. The
        // Extra Stage demo is not stopped here at all.
        if((resident->demo_num > 4) || (stage_frame < (DEMO_N - 4))) {
            return;
        }
    }
    hmem_free(reinterpret_cast<void __seg *>(DemoBuf));
    palette_black_out(8);
    GameExecl(DEMOPLAY_BINARY_OP);
}
