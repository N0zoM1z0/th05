// Declarations used by end/dispatch.cpp.
#ifndef TH05_MAIN_END_DISPATCH_HPP
#define TH05_MAIN_END_DISPATCH_HPP
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This is TH05 MAIN code
#endif

// Values of resident->end_sequence, as also read by MAINE.
typedef enum {
    ES_GOOD = 0xFF,
    ES_BAD = 0xFE,
    ES_EXTRA = 0xFD,
    ES_INGAME = 0x37,
    ES_SCORE = 0,
} end_sequence_t;

extern unsigned char continues_used;
// Both are "maine"; see runtime/end_binary_names.c.
extern const char near ending_binary_main[];
extern const char near ending_binary_extra[];

#pragma codeseg _TEXT
extern "C" void pascal far palette_black_out(unsigned int speed);
#pragma codeseg SHARED
extern "C" int pascal far snd_kaja_interrupt(int ax);
#pragma codeseg END_DISPATCH_TEXT main_01
int pascal far GameExecl(const char far *binary_fn);
// GameExecl() is far, but earlier in the same physical code segment;
// `samecodeseg` lets TLINK shorten the call to NOP / PUSH CS / CALL near.
#pragma samecodeseg GameExecl
void far end_game(void);
void far end_extra(void);
#pragma codeseg

typedef char ending_dispatch_resident_is_128[(sizeof(resident_t) == 128) ? 1 : -1];
typedef char ending_dispatch_sequence_at_26[(offsetof(resident_t, end_sequence) == 26) ? 1 : -1];
#endif
