// Natural maintained TH04 cleanup donor, complete real shared far callback.
#pragma option -zCEXIT_CORE_TEXT -zPshared_exit
#include "src/shared/core/game_exit.hpp"
#pragma codeseg EXIT_CORE_TEXT shared_exit

void far game_exit(void)
{
    pfend();
    exit_graph_accesspage(1);
    graph_clear();
    exit_graph_accesspage(0);
    graph_clear();
    exit_graph_accesspage(0);
    exit_graph_showpage(0);
    mem_unassign();
    vsync_end();
    text_clear();
    js_end();
    egc_start();
    bgm_finish();
}
