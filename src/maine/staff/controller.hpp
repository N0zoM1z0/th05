// staffroll_animate(): the whole staff roll, ending with the two verdict screens.
#ifndef TH05_STAFF_CONTROLLER_HPP
#define TH05_STAFF_CONTROLLER_HPP
#include <dos.h>
#include "src/maine/staff/rain.hpp"
#include "src/maine/staff/orb_opening.hpp"
#include "src/maine/staff/frame.hpp"
#include "src/maine/staff/reveal_b.hpp"

// The verdict functions are declared under the VERDICT_FULL_TEXT segment they
// were compiled in.
#ifndef TH05_VERDICT_FULL_FAMILY
#define TH05_VERDICT_FULL_FAMILY
#define TH05_STAFF_RESTORE_VERDICT
#endif
#include "src/maine/verdict/full.hpp"
#ifdef TH05_STAFF_RESTORE_VERDICT
#undef TH05_STAFF_RESTORE_VERDICT
#undef TH05_VERDICT_FULL_FAMILY
#endif

enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
static const int STAFF_KAJA_SONG_PLAY = 0;
static const int STAFF_KAJA_SONG_FADE = 2;
static const int STAFF_GRCG_RMW = 0xC0;
static const size_t STAFF_VERDICT_SCREEN_SIZE = 352 * (320 / 8);
static const size_t STAFF_VERDICT_SCROLL_STEP = 8 * (320 / 8);
static const uint16_t STAFF_INPUT_UP = 0x0001;
static const uint16_t STAFF_INPUT_DOWN = 0x0002;
static const uint16_t STAFF_INPUT_BOMB = 0x0010;
static const uint16_t STAFF_INPUT_SHOT = 0x0020;
static const uint16_t STAFF_INPUT_CANCEL = 0x1000;
static const uint16_t STAFF_INPUT_OK = 0x2000;
extern uint16_t key_det;

// Defined in filenames.cpp.
extern char staff_bgm_filename[6];
extern char staff_cdg_00_filename[10];
extern char staff_cdg_01_filename[10];
extern char staff_cdg_02_filename[10];
extern char staff_cdg_03_filename[10];
extern char staff_cdg_04_filename[10];
extern char staff_cdg_05_filename[10];
extern char staff_cdg_06_filename[10];
extern char staff_cdg_07_filename[10];
extern char staff_cdg_08_filename[10];
extern char staff_cdg_09_filename[10];
extern char staff_cdg_10_filename[10];
extern char staff_bfnt_01_filename[10];
extern char staff_bfnt_00_filename[10];

#pragma codeseg _TEXT
extern "C" {
    void pascal far grcg_setcolor(int mode, vc2 color);
    void pascal far grcg_byteboxfill_x(int left, int top, int right, int bottom);
    int pascal far super_entry_bfnt(const char far *filename);
    int pascal far super_convert_tiny(int slot);
    void pascal far super_free(void);
}
#pragma codeseg SHARED
extern "C" {
    void pascal far snd_load(const char far *filename, snd_load_func_t operation);
    int pascal far snd_kaja_interrupt(int ax);
    void pascal far cdg_load_all_noalpha(int slot, const char far *filename);
    void pascal far cdg_free_all(void);
}
int far input_reset_sense_held(void);
#pragma codeseg STAFF_BITMAP_TEXT group_01
void pascal near verdict_bitmap_snap(size_t bitmap_offset);
void pascal near verdict_bitmap_put(size_t bitmap_offset);
#pragma codeseg STAFF_CONTROL_TEXT group_01
void near staffroll_animate(void);
#pragma codeseg
#endif
