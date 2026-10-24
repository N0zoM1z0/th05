// Physical TH05 MAINE interfaces. No helper bodies or substitute game state.
#ifndef TH05_MAINE_ALLCAST_HPP
#define TH05_MAINE_ALLCAST_HPP

#include <dos.h>
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'E'
#error This owner is the TH05 MAINE all-cast animation
#endif

typedef int screen_x_t;
typedef int screen_y_t;
typedef int vram_y_t;
typedef int int16_t;
typedef unsigned char page_t;
typedef unsigned char playchar_t;
typedef unsigned char vc_t;
typedef unsigned int vc2;

#define RES_X 640
#define RES_Y 400
#define BYTE_DOTS 8
#define PLAYCHAR_COUNT 4
#define PAGE_COUNT 2
#define PI_MASK_COUNT 4
#define GC_RMW 0xC0
static const int CUTSCENE_PIC_H = RES_Y / 2;
static const int CUTSCENE_PIC_LEFT = RES_X / 4;
static const int KAJA_SONG_PLAY = 0;

extern unsigned int PaletteTone;
void pascal far frame_delay(int frames);
int pascal far pi_load(int slot, const char far *filename);
void pascal far pi_palette_apply(int slot);
void pascal far pi_put_quarter_8(screen_x_t left, vram_y_t top, int slot, int quarter);
void pascal far pi_put_quarter_masked_8(screen_x_t left, vram_y_t top, int slot, int quarter, int mask_id);
void pascal far pi_free(int slot);
enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
extern "C" {
    void pascal far grcg_setcolor(int mode, vc2 color);
    void pascal far grcg_byteboxfill_x(int left, int top, int right, int bottom);
    void pascal far palette_show(void);
    void pascal far palette_black_out(unsigned speed);
    void pascal far snd_load(const char far *filename, snd_load_func_t operation);
    int pascal far snd_kaja_interrupt(int ax);
    int16_t far snd_bgm_measure(void);
}

#define graph_accesspage(page) outportb(0xA6, page)
#define graph_showpage(page) outportb(0xA4, page)
#define grcg_off() outportb(0x7C, 0)
#define grcg_boxfill_8(left, top, right, bottom) \
    grcg_byteboxfill_x(((left) / BYTE_DOTS), top, ((right) / BYTE_DOTS), bottom)
#define palette_settone(tone) (PaletteTone = (tone), palette_show())
#define palette_100() palette_settone(100)
#define snd_kaja_func(operation, parameter) \
    snd_kaja_interrupt(((operation) << 8) | static_cast<uint8_t>(parameter))

void near allcast_animate(void);
typedef char th05_allcast_page_is_byte[(sizeof(page_t) == 1) ? 1 : -1];
typedef char th05_allcast_playchar_is_byte[(sizeof(playchar_t) == 1) ? 1 : -1];
typedef char th05_allcast_filename_pointer_is_far[(sizeof(const char *) == 4) ? 1 : -1];

#endif
