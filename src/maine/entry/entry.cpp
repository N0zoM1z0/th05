// MAINE.EXE entry point: loads the resident structure through MIKO.CFG, then
// runs the ending, staff roll / all-cast credits, verdict and name
// registration in the order the resident ending type asks for, and finally
// returns to OP.EXE. Adapted from ReC98 th04/end/entry.cpp (GAME == 5).
// The file is UTF-8; the build converts it to Shift-JIS for the
// "怪綺談1.dat" archive name.
#pragma option -zCMAINE_E_TEXT -zPgroup_01
#include <process.h>
#include "src/maine/entry/entry.hpp"

resident_t far *resident;

// Equivalent of ReC98's cfg_load_and_set_resident(). Reads the complete
// MIKO.CFG without any error checking, as in the original.
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
    // In the large model, the variadic NULL terminator must be a four-byte
    // far pointer.
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
    // TH05's cutscene_script_free() is empty, so there is no call here.
}

// Despite its name, this does not delay in TH05: the name comes from TH04,
// where it waits 100 frames before regist_menu(). TH05 waits once at the
// start of main() instead.
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
