// Demo replay buffer layout and the functions used by demo.cpp. Names
// follow ReC98's th04/main/demo.hpp.
#ifndef TH05_MAIN_DEMO_HPP
#define TH05_MAIN_DEMO_HPP
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This is TH05 MAIN code
#endif

typedef uint16_t input_t;
typedef uint8_t input_replay_t;
static const input_t INPUT_MOVEMENT = 0x0F0F;
static const unsigned int DEMO_N = 5000;
static const unsigned int DEMO_N_EXTRA = (DEMO_N * 4);
// A DEMO?.REC file: the low byte of key_det for every frame, then the
// shift key state for every frame.
template <unsigned int Frames> struct REC {
    input_replay_t input[Frames];
    bool shift[Frames];
};
extern input_t key_det;
extern bool shiftkey;
extern unsigned int stage_frame;
extern uint8_t far *DemoBuf;
extern char near demo_fn[];
extern const char near DEMOPLAY_BINARY_OP[];

extern "C" {
    void __seg *pascal far hmem_allocbyte(unsigned bytesize);
    void pascal far hmem_free(void __seg *block);
    int pascal far file_ropen(const char far *filename);
    int pascal far file_read(void far *buffer, unsigned size);
    void pascal far file_close(void);
    void pascal far palette_black_out(unsigned speed);
}
// GameExecl() is far Pascal. TLINK shortens the call from DemoPlay() to
// NOP / PUSH CS / CALL near only if both end up in the same segment
// (DEMO_TEXT, as in the original); being in the same group is not enough.
#pragma codeseg DEMO_GAMEEXECL_CONTEXT main_01
int pascal far GameExecl(const char far *binary_fn);
#pragma codeseg DEMO_TEXT main_01
void near demo_load(void);
void near DemoPlay(void);

typedef char th05_demo_input_is_1[(sizeof(input_replay_t) == 1) ? 1 : -1];
typedef char th05_demo_shift_is_1[(sizeof(bool) == 1) ? 1 : -1];
typedef char th05_demo_regular_record_is_10000[(sizeof(REC<DEMO_N>) == 10000) ? 1 : -1];
typedef char th05_demo_extra_record_is_40000[(sizeof(REC<DEMO_N_EXTRA>) == 40000U) ? 1 : -1];
#endif
