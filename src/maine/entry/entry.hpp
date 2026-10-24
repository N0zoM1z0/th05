// MAINE entry ABI adapted from ReC98 th04/end/entry.cpp with GAME=5.
#ifndef TH05_MAINE_ENTRY_HPP
#define TH05_MAINE_ENTRY_HPP

#include "src/main/hud/resident.hpp"
#include "src/main/formats/cfg_resident.hpp"

typedef enum {
    ES_GOOD = 0xFF,
    ES_BAD = 0xFE,
    ES_EXTRA = 0xFD,
    ES_INGAME = 0x37,
    ES_SCORE = 0,
} end_sequence_t;

enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
static const int KAJA_SONG_FADE = 2;

extern unsigned int mem_assign_paras;
extern long random_seed;

void far game_exit(void);
int pascal far game_init_main(const unsigned char far *pf_fn);
void pascal far frame_delay(int frames);
int pascal near cutscene_script_load(const char far *filename);
void near cutscene_animate(void);
void near staffroll_animate(void);
void near allcast_animate(void);
void near verdict_animate(void);
void near regist_menu(void);

extern "C" {
    int pascal far file_ropen(const char far *filename);
    int pascal far file_read(void far *buffer, unsigned int count);
    void pascal far file_close(void);
    void pascal far cdg_free_all(void);
    void pascal far graph_hide(void);
    void pascal far graph_show(void);
    void pascal far text_clear(void);
    int pascal far snd_determine_modes(int bgm, int se);
    void pascal far snd_load(const char far *filename, snd_load_func_t function);
    int pascal far snd_kaja_interrupt(int ax);
}

void pascal near game_exit_and_exec(char far *filename);
void near end_animate(void);

#endif
