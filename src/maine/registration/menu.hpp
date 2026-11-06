// True foreign frames precede the shared score/menu declarations.
#ifndef TH05_MREG_MENU_HPP
#define TH05_MREG_MENU_HPP
#include <dos.h>
#include "src/main/hud/resident.hpp"

#pragma codeseg _TEXT
extern "C" {
    void pascal far palette_show(void);
    void pascal far palette_black_in(unsigned int speed);
    void pascal far palette_black_out(unsigned int speed);
    int pascal far graph_copy_page(int to_page);
    int pascal far super_entry_bfnt(const char far *filename);
    void far super_free(void);
    void pascal far text_clear(void);
    void pascal far gaiji_putca(int x, int y, int glyph, int attr);
}
#pragma codeseg SHARED
int far input_reset_sense_held(void);
int pascal far input_wait_for_change(int frames);
int pascal far pi_load(int slot, const char far *filename);
void pascal far pi_palette_apply(int slot);
void pascal far pi_put_8(int left, int top, int slot);
void pascal far pi_free(int slot);
extern "C" {
    void far bgimage_snap(void);
    void far bgimage_free(void);
    void pascal far graph_putsa_fx(int left, int top,
        unsigned int color, const uint8_t far *text);
    int pascal far snd_kaja_interrupt(int ax);
    void pascal far snd_se_play(int sound);
}
#pragma codeseg REG_SCORE_TEXT GROUP_01
bool pascal near hiscore_scoredat_load_for(int pc);
void near hiscore_scoredat_save(void);
void near score_insert(void);
void pascal near places_put(int pc);
#pragma codeseg SHARED
#include "src/op/hiscore/view.hpp"
#include "src/maine/registration/alphabet_data.hpp"

extern uint8_t entered_place;
extern playchar_t playchar;
extern int entered_name_cursor;
extern char registration_bg_fn[8];
extern char registration_score_font[10];
extern char registration_cloud_font[10];
extern char registration_ball_font[10];
extern uint8_t registration_turbo_warning_shadow[51];
extern uint8_t registration_turbo_warning[51];
extern char registration_bgm_fn[5];

#pragma codeseg REG_HELPERS_TEXT GROUP_01
void pascal near reg_name_put(int place, playchar_t pc, uint8_t cursor);
void pascal near alphabet_cursor_put(int col, int row, int attr);
void pascal near glyphball_spawn(int x, int y, int place, playchar_t pc, uint8_t cursor);
void near glyphballs_commit_and_wait(void);
void near registration_frame(void);
#pragma codeseg REG_MENU_TEXT GROUP_01
void near regist_menu(void);

static const uint8_t REG_NO_ENTRY = 0xFF;
static const uint8_t REG_EMPTY_GLYPH = 0x02;
static const uint16_t REG_INPUT_BOMB = 0x10;
static const uint8_t REG_END_EXTRA = 0xFD;
static const int REG_ATTR_WHITE = 0xE1;
static const int REG_ATTR_HIGHLIGHT = 0x85;
static const int REG_REPEAT_DELAY = 30;
#endif
