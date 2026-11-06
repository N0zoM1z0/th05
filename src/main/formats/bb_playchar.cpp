// Load and release the selected player's bomb-background tile bitmap.
#pragma option -zCBB_PLAYCHAR_TEXT -zPmain_01 -k-
#include "src/shared/abi.hpp"

#pragma codeseg _TEXT
extern "C" void pascal far hmem_free(void __seg *block);
#pragma codeseg BB_PLAYCHAR_TEXT main_01
#include "src/main/stage/setup.hpp"

char bb_playchar_fn[7] = "BB0.BB";
extern bb_tiles8_t __seg *bb_playchar_seg;
extern unsigned char playchar;

extern "C" void pascal near bb_playchar_load(void)
{
    // This is the original additive filename update, including repeated calls.
    bb_playchar_fn[2] += static_cast<char>(playchar);
    bb_playchar_seg = bb_load(bb_playchar_fn);
}

extern "C" void pascal near bb_playchar_free(void)
{
    if(bb_playchar_seg) {
        hmem_free(bb_playchar_seg);
        bb_playchar_seg = 0;
    }
}
