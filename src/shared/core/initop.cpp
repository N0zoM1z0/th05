// Natural ReC98 b6ba5b0a th03/core/initop.cpp, actual GAME5 branch.
#pragma option -zCSHARED -3
#include <dos.h>
#include "src/shared/abi.hpp"
extern size_t mem_assign_paras;
extern "C" {
    extern unsigned int __cdecl bbufsiz;
    int pascal far mem_assign_dos(unsigned int paragraphs);
    void pascal far graph_start(void);
    void pascal far graph_clear(void);
    void pascal far vsync_start(void);
    void pascal far key_beep_off(void);
    void pascal far text_systemline_hide(void);
    void pascal far text_cursor_hide(void);
    void pascal far egc_start(void);
    int pascal far js_start(void);
    void pascal far pfstart(const unsigned char far *filename);
    int pascal far bgm_init(int buffer_size);
}
#define graph_accesspage(page) outportb(0xA6, page)
#define graph_showpage(page) outportb(0xA4, page)
#define pfsetbufsiz(size) bbufsiz = size

int far game_init_op(const unsigned char far *pf_fn)
{
    if(mem_assign_dos(mem_assign_paras)) {
        return 1;
    }
    graph_start();
    graph_accesspage(1);
    graph_clear();
    graph_accesspage(0);
    graph_clear();
    graph_accesspage(0);
    graph_showpage(0);
    pfsetbufsiz(8192);
    vsync_start();
    key_beep_off();
    text_systemline_hide();
    text_cursor_hide();
    egc_start();
    js_start();
    if(pf_fn[0]) {
        pfstart(pf_fn);
    }
    bgm_init(1024);
    return 0;
}
