// Declarations for game_exit() and game_exit_to_dos().
#ifndef TH05_GAME_EXIT_HPP
#define TH05_GAME_EXIT_HPP
#include <dos.h>
#include "src/shared/abi.hpp"

#if GAME != 5
#error These callbacks recover the TH05 shared shutdown protocol
#endif

#pragma codeseg _TEXT
extern "C" {
    void pascal far pfend(void);
    void pascal far graph_clear(void);
    int pascal far mem_unassign(void);
    void pascal far vsync_end(void);
    void pascal far text_clear(void);
    void pascal far js_end(void);
    void pascal far egc_start(void);
    void pascal far bgm_finish(void);
    void pascal far key_beep_on(void);
    void pascal far text_systemline_show(void);
    void pascal far text_cursor_show(void);
}
#pragma codeseg
// Both functions are far; only the DOS wrapper tells the compiler that
// game_exit() shares its code segment.
void far game_exit(void);
void far game_exit_to_dos(void);

#define exit_graph_accesspage(page) outportb(0xA6, page)
#define exit_graph_showpage(page) outportb(0xA4, page)
#endif
