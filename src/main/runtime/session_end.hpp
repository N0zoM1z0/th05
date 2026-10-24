// Actual TH05 stage release and pause-menu interfaces. No resource payload.
#ifndef TH05_SESSION_END_HPP
#define TH05_SESSION_END_HPP
#include "src/shared/abi.hpp"

#if GAME != 5 || BINARY != 'M'
#error This source implements TH05 MAIN stage release and pause
#endif

extern unsigned int key_det;
extern const char near gsCHUUDAN[];
extern const char near gsSAIKAI[];
extern const char near gsSHUURYOU[];
extern const char near aGAME_PAUSE_SPACES_1[];
extern const char near aGAME_PAUSE_SPACES_2[];
extern const char near aGAME_PAUSE_SPACES_3[];

static const int STAGE_PATTERN_FIRST = 180;
static const int STAGE_PATTERN_END = 256;
// Actual CDG_PER_STAGE..CDG_PER_STAGE_last, inclusive, from frozen ems.hpp.
static const int STAGE_CDG_FIRST = 1;
static const int STAGE_CDG_END = 31;
static const unsigned int PAUSE_INPUT_UP = 0x0001;
static const unsigned int PAUSE_INPUT_DOWN = 0x0002;
static const unsigned int PAUSE_INPUT_SHOT = 0x0020;
static const unsigned int PAUSE_INPUT_CANCEL = 0x1000;
static const unsigned int PAUSE_INPUT_OK = 0x2000;
static const unsigned int PAUSE_INPUT_Q = 0x4000;
static const unsigned int PAUSE_TX_YELLOW = 0xC1;
static const unsigned int PAUSE_TX_WHITE = 0xE1;
static const unsigned int PAUSE_TX_UNDERLINE = 0x08;

#pragma codeseg SESSION_END_MAIN01_TEXT main_01
void near bb_boss_free(void);
void near dialog_free(void);
void near std_free(void);
void near map_free(void);
#pragma codeseg SHARED
int far input_reset_sense_held(void);
int pascal far input_wait_for_change(int frames);
extern "C" void pascal far cdg_free(int slot);
#pragma codeseg _TEXT
extern "C" {
    void pascal far super_clean(int first, int end);
    void pascal far gaiji_putsa(int x, int y, const char far *text, unsigned int attr);
    void pascal far text_putsa(int x, int y, const char far *text, unsigned int attr);
}
#pragma codeseg SESSION_END_TEXT main_01
extern "C" {
    void near stage_session_free(void);
    int near pause(void);
}
#pragma codeseg

typedef char session_end_input_is_2[(sizeof(key_det) == 2) ? 1 : -1];
#endif
