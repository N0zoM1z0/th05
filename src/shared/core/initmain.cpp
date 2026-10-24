// Natural ReC98 b6ba5b0a th03/core/initmain.cpp, GAME=5 behavior.
#pragma option -zCSHARED -3
#include "src/shared/abi.hpp"
extern size_t mem_assign_paras;
extern "C" {
    extern unsigned int __cdecl bbufsiz;
    int pascal far mem_assign_dos(unsigned int paragraphs);
    void pascal far vsync_start(void);
    void pascal far egc_start(void);
    void pascal far graph_400line(void);
    int pascal far js_start(void);
    void pascal far pfstart(const unsigned char far *filename);
    int pascal far bgm_init(int buffer_size);
}
#define pfsetbufsiz(size) bbufsiz = size

int pascal far game_init_main(const unsigned char far *pf_fn)
{
    if(mem_assign_dos(mem_assign_paras)) {
        return 1;
    }
    pfsetbufsiz(4096);
    vsync_start();
    egc_start();
    graph_400line();
    js_start();
    pfstart(pf_fn);
    bgm_init(2048);
    return 0;
}
