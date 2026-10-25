// Complete natural MAIN entry; actual same-CS process-handoff contract.
#ifndef TH05_RUNTIME_COMBINED
#pragma option -zCDEMO_TEXT -zPmain_01
#endif
#include "src/main/runtime/main.hpp"
#pragma codeseg DEMO_TEXT main_01
#pragma samecodeseg GameExecl

void main(void)
{
    if(!cfg_load_resident_ptr()) {
        return;
    }
    mem_assign_paras = (291200 >> 4);
    game_init_main(main_pf_fn);
    random_seed = resident->rand;
    ems_allocate_and_preload_eyecatch();
    text_clear();
    snd_determine_modes(resident->bgm_mode, resident->se_mode);
    snd_load(se_fn, SND_LOAD_SE);

    for(;;) {
        stage_session_init();
        gameplay_loop();
        if(quit != Q_NEXT_STAGE) {
            break;
        }
        stage_session_free();
    }
    GameExecl(op_fn);
}
