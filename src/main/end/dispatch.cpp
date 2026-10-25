// Natural TH04 ending-dispatch donor with original TH05 sequence selection.
#pragma option -zCEND_DISPATCH_TEXT -zPmain_01
#include "src/main/end/dispatch.hpp"
#pragma codeseg END_DISPATCH_TEXT main_01

void far end_game(void)
{
    if(continues_used != 0) {
        resident->end_sequence = ES_BAD;
    } else {
        resident->end_sequence = ES_GOOD;
    }
    snd_kaja_interrupt((2 << 8) | 4); // KAJA_SONG_FADE, speed4.
    palette_black_out(16);
    GameExecl(ending_binary_main);
}

void far end_extra(void)
{
    resident->end_sequence = ES_EXTRA;
    snd_kaja_interrupt((2 << 8) | 4); // KAJA_SONG_FADE, speed4.
    palette_black_out(16);
    GameExecl(ending_binary_extra);
}
