// Natural MAINE entry adapted from nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th04/end/entry.cpp, GAME=5.
// Canonical UTF-8; the real archive filename requires explicit CP932 staging.
#pragma option -zCMAINE_E_TEXT -zPgroup_01
#include <process.h>
#include "src/maine/entry/entry.hpp"

resident_t far *resident;

static inline resident_t __seg *entry_cfg_load_and_set_resident(
    cfg_t &configuration, const char far *filename
) {
    file_ropen(filename);
    file_read(&configuration, sizeof(configuration));
    file_close();
    resident_t __seg *resident_segment = configuration.resident;
    resident = resident_segment;
    return resident_segment;
}

resident_t __seg *near cfg_load_resident_ptr(void)
{
    cfg_t configuration;
    return entry_cfg_load_and_set_resident(configuration, "MIKO.CFG");
}

void pascal near game_exit_and_exec(char far *filename)
{
    cdg_free_all();
    graph_hide();
    text_clear();
    game_exit();
    // execl's large-model variadic terminator is a complete four-byte pointer.
    execl(filename, filename, 0UL);
}

void near end_animate(void)
{
    static char far *SCRIPT_FN = "_ED00.TXT";
    if(resident->end_sequence == ES_BAD) {
        SCRIPT_FN[3] = '0';
    } else if(resident->end_sequence == ES_EXTRA) {
        SCRIPT_FN[3] = '2';
    } else {
        SCRIPT_FN[3] = '1';
    }
    SCRIPT_FN[4] = ('0' + resident->playchar);
    cutscene_script_load(SCRIPT_FN);
    cutscene_animate();
    // TH05's cutscene_script_free() is intentionally empty.
}

inline void delay_then_regist_menu(void)
{
    regist_menu();
}

void main(void)
{
    if(!cfg_load_resident_ptr()) {
        return;
    }
    mem_assign_paras = (336000 >> 4);
    game_init_main(reinterpret_cast<const unsigned char far *>("怪綺談1.dat"));
    snd_determine_modes(resident->bgm_mode, resident->se_mode);
    snd_load("miko", SND_LOAD_SE);
    graph_show();
    random_seed = resident->rand;
    frame_delay(100);

    if(resident->end_sequence >= ES_BAD) {
        end_animate();
        staffroll_animate();
        delay_then_regist_menu();
    } else if(resident->end_sequence == ES_EXTRA) {
        end_animate();
        allcast_animate();
        verdict_animate();
        delay_then_regist_menu();
    } else {
        delay_then_regist_menu();
        verdict_animate();
    }
    snd_kaja_interrupt((KAJA_SONG_FADE << 8) | 4);
    game_exit_and_exec("op");
}
