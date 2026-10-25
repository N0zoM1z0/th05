// Complete TH05 game-over/continue interfaces; all text and state are foreign.
#ifndef TH05_GAMEOVER_HPP
#define TH05_GAMEOVER_HPP
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner implements TH05 MAIN game-over and continue
#endif

typedef void (near pascal *near GameoverOverlay)(void);
extern GameoverOverlay overlay1;
extern unsigned char gameover_fade_frame;
extern unsigned char continues_used;
extern unsigned char stage_id;
extern unsigned char power;
extern unsigned char dream;
extern unsigned char bombs;
extern unsigned char lives;
extern unsigned int key_det;
extern unsigned int PaletteTone;
extern const char near gGAMEOVER[];
extern const char near gCONTINUE_QUESTION[];
extern const char near gYES[];
extern const char near gNO[];
extern const char near gCREDIT[];
extern char near gameover_erase_in[];
extern char near gameover_erase_out[];
extern const char near maine_binary[];

static const unsigned int GAMEOVER_TX_BLACK = 0x01;
static const unsigned int GAMEOVER_TX_WHITE = 0xE1;
static const unsigned int GAMEOVER_TX_GREEN = 0x81;
static const unsigned int GAMEOVER_TX_REVERSE = 0x04;
static const unsigned int GAMEOVER_INPUT_UP = 0x0001;
static const unsigned int GAMEOVER_INPUT_DOWN = 0x0002;
static const unsigned int GAMEOVER_INPUT_SHOT = 0x0020;
static const unsigned int GAMEOVER_INPUT_CANCEL = 0x1000;
static const unsigned int GAMEOVER_INPUT_OK = 0x2000;
static const unsigned char GAMEOVER_KEEP_RUNNING = 0;
static const unsigned char GAMEOVER_END_SCORE = 0;

#pragma codeseg _TEXT
extern "C" {
    void pascal far gaiji_putca(int x, int y, unsigned int glyph, unsigned int attr);
    void pascal far gaiji_putsa(int x, int y, const char far *text, unsigned int attr);
    void pascal far text_putsa(int x, int y, const char far *text, unsigned int attr);
    void pascal far palette_show(void);
    void pascal far palette_black_out(unsigned int speed);
}
#pragma codeseg SHARED
int far input_reset_sense_held(void);
int pascal far input_wait_for_change(int frames);
void pascal far frame_delay(int frames);
extern "C" int pascal far snd_kaja_interrupt(int ax);

#pragma codeseg GAMEOVER_AFTER_TEXT main_01
void near overlay_wipe(void);
void near overlay_black(void);
extern "C" void pascal far shot_level_update(void);
#pragma samecodeseg shot_level_update
#pragma codeseg GAMEOVER_TEXT main_01
extern "C" void pascal near nullfunc_near(void);
void near hiscore_continue_enter(void);
void near score_reset(void);
extern "C" void pascal near hud_score_put(void);
void far hud_lives_put(void);
void far hud_bombs_put(void);
int pascal far GameExecl(const char far *binary_fn);
#pragma samecodeseg hud_lives_put
#pragma samecodeseg hud_bombs_put
#pragma samecodeseg GameExecl

unsigned char near gameover_fade_in(void);
unsigned char near gameover_fade_out(void);
unsigned char near gameover_run(void);
unsigned char near gameover_continue_menu(void);
#pragma codeseg

typedef char gameover_callback_is_near[(sizeof(GameoverOverlay) == 2) ? 1 : -1];
typedef char gameover_resident_is_complete[(sizeof(resident_t) == 128) ? 1 : -1];
#endif
