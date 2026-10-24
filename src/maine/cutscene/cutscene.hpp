// Natural cutscene interfaces adapted from pinned nmlgc/ReC98, TH05/TH03.
// Complete physical types and real hardware/library ABIs; no emitted code.
#ifndef TH05_MAINE_CUTSCENE_HPP
#define TH05_MAINE_CUTSCENE_HPP

#include <dos.h>
#include <ctype.h>
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'E'
#error This owner is the TH05 MAINE cutscene implementation
#endif

typedef char int8_t;
typedef int int16_t;
typedef int bool16;
typedef int screen_x_t;
typedef int screen_y_t;
typedef int vram_y_t;
typedef int vram_offset_t;
typedef int vram_byte_amount_t;
typedef int shiftjis_ank_amount_t;
typedef int shiftjis_kanji_amount_t;
typedef unsigned char vc_t;
typedef unsigned int vc2;
typedef uint8_t shiftjis_t;
typedef uint16_t shiftjis_kanji_t;
typedef uint8_t dots8_t;
typedef uint16_t dots16_t;
typedef dots16_t egc_temp_t;

struct screen_point_t { screen_x_t x; screen_y_t y; };
template<class T> struct Planar { T B, R, G, E; };
union ShiftJISKanji { shiftjis_kanji_t t; int8_t byte[2]; };
template<class RowDots, pixel_t H> struct DotRect {
    RowDots row[H];
    RowDots& operator [](pixel_t y) { return row[y]; }
    const RowDots& operator [](pixel_t y) const { return row[y]; }
};
#define dot_rect_t(w, h) DotRect<dots##w##_t, h>

#define RES_X 640
#define RES_Y 400
#define BYTE_DOTS 8
#define GLYPH_H 16
#define GLYPH_FULL_W 16
#define GLYPH_HALF_W 8
#define PF_FN_LEN 13
#define GC_RMW 0xC0
#define V_WHITE 15
#define WEIGHT_BOLD 2
#define PI_MASK_COUNT 4u
#define RETURN_KEY_CELS 4u
#define ga_RETURN_KEY 0x1C
#define gs_NOTES 3
#define gs_HEART_2 6
#define gs_EXCLAMATION 7
#define gs_QUESTION 8
#define gs_SWEAT 9
#define gs_DOUBLE_EXCLAMATION 10
#define gs_EXCLAMATION_QUESTION 11
static const int CUTSCENE_PIC_W = RES_X / 2;
static const int CUTSCENE_PIC_H = RES_Y / 2;
static const int CUTSCENE_PIC_LEFT = (RES_X / 2) - (CUTSCENE_PIC_W / 2);
static const int CUTSCENE_PIC_VRAM_W = CUTSCENE_PIC_W / BYTE_DOTS;
static const int PI_QUARTER_COUNT = 4;
static const int PI_QUARTER_W = RES_X / 2;
static const int PI_QUARTER_H = RES_Y / 2;
static const int EGC_REGISTER_DOTS = 16;
static const int EGC_REGISTER_SIZE = 2;

enum graph_putsa_fx_func_t {
    FX_WEIGHT_NORMAL, FX_WEIGHT_HEAVY, FX_WEIGHT_BOLD, FX_WEIGHT_BLACK,
    FX_MASK, FX_MASK_1 = FX_MASK, FX_MASK_2, FX_MASK_3, FX_MASK_4, FX_MASK_END,
    _graph_putsa_fx_func_FORCE_INT16 = 0x7FFF
};
enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
static const int KAJA_SONG_PLAY = 0;
static const int KAJA_SONG_STOP = 1;
static const int KAJA_SONG_FADE = 2;
static const uint16_t INPUT_NONE = 0;
static const uint16_t INPUT_SHOT = 0x0020;
static const uint16_t INPUT_CANCEL = 0x1000;
static const uint16_t INPUT_OK = 0x2000;

extern uint16_t key_det;
extern unsigned int PaletteTone;
extern graph_putsa_fx_func_t graph_putsa_fx_func;
extern dots8_t far *VRAM_PLANE_B;
extern unsigned char colmap_count;
extern const dot_rect_t(16, 4) BOX_MASKS[5];
extern ShiftJISKanji near CUTSCENE_KANJI[];

// This module's runtime-owned state; these are declarations, not alias objects.
extern unsigned char script[8192];
extern unsigned char near *script_p;
extern Planar<dots16_t> far *box_bg;
extern bool fast_forward;
extern screen_point_t cursor;
extern int text_interval;
extern vc_t text_col;
extern uint8_t text_fx;

void pascal far frame_delay(int frames);
int16_t far input_reset_sense_held(void);
int pascal far pi_load(int slot, const char far *filename);
void pascal far pi_palette_apply(int slot);
void pascal far pi_put_8(screen_x_t left, vram_y_t top, int slot);
void pascal far pi_put_quarter_8(screen_x_t left, vram_y_t top, int slot, int quarter);
void pascal far pi_free(int slot);
void pascal far pi_put_quarter_masked_8(screen_x_t left, vram_y_t top, int slot, int quarter, int mask_id);
void pascal far egc_copy_rect_1_to_0_16(screen_x_t left, vram_y_t top, pixel_t width, pixel_t height);
extern "C" {
    int pascal far file_ropen(const char far *filename);
    int pascal far file_read(void far *buffer, unsigned size);
    long pascal far file_size(void);
    void pascal far file_close(void);
    void pascal far egc_on(void);
    void pascal far egc_off(void);
    void pascal far graph_clear(void);
    int pascal far graph_copy_page(int to_page);
    void pascal far graph_scrollup(unsigned line);
    void pascal far graph_gaiji_putc(screen_x_t left, vram_y_t top, int glyph, vc2 color);
    void pascal far grcg_setcolor(int mode, vc2 color);
    void pascal far grcg_byteboxfill_x(int left, int top, int right, int bottom);
    void pascal far palette_show(void);
    void pascal far palette_black_in(unsigned speed);
    void pascal far palette_black_out(unsigned speed);
    void pascal far palette_white_in(unsigned speed);
    void pascal far palette_white_out(unsigned speed);
    void far bgimage_snap(void);
    void far bgimage_free(void);
    void pascal far bgimage_put_rect_16(screen_x_t left, screen_y_t top, pixel_t width, pixel_t height);
    void pascal far graph_putsa_fx(screen_x_t left, vram_y_t top, vc2 color, const shiftjis_t far *text);
    int pascal far snd_kaja_interrupt(int ax);
    void far snd_se_reset(void);
    void pascal far snd_se_play(int effect);
    void far snd_se_update(void);
    void pascal far snd_delay_until_measure(int measure, int frame);
    void pascal far snd_load(const char far *filename, snd_load_func_t operation);
}

#define graph_accesspage(page) outportb(0xA6, page)
#define graph_showpage(page) outportb(0xA4, page)
#define grcg_off() outportb(0x7C, 0)
#define palette_settone(tone) (PaletteTone = (tone), palette_show())
#define grcg_boxfill_8(left, top, right, bottom) \
    grcg_byteboxfill_x(((left) / BYTE_DOTS), top, ((right) / BYTE_DOTS), bottom)
#define snd_kaja_func(operation, parameter) \
    snd_kaja_interrupt(((operation) << 8) | static_cast<uint8_t>(parameter))
#define snd_se_play_force(effect) { snd_se_reset(); snd_se_play(effect); snd_se_update(); }

static inline vram_offset_t vram_offset_shift(screen_x_t x, vram_y_t y) {
    return (x >> 3) + (y << 6) + (y << 4);
}
// A word EGC write consumes the real OUT DX,AX register pair. Preserve
// the device protocol explicitly rather than supplying an assembler body.
inline void cutscene_egc_write(unsigned int port, unsigned int value) {
    _AX = value;
    _DX = port;
    outport(_DX, _AX);
}

#define egc_chunk(offset) *(dots16_t far *)(VRAM_PLANE_B + offset)

// Genuine EGC register writes. The reference's instruction macro is replaced
// by the standard hardware I/O intrinsic; code generation is still unproven.
#define EGC_ACTIVEPLANEREG 0x04A0
#define EGC_READPLANEREG 0x04A2
#define EGC_MODE_ROP_REG 0x04A4
#define EGC_MASKREG 0x04A8
#define EGC_ADDRRESSREG 0x04AC
#define EGC_BITLENGTHREG 0x04AE
#define egc_setup_copy_masked(mask) { \
    cutscene_egc_write(EGC_READPLANEREG, 0x00FF); \
    cutscene_egc_write(EGC_MODE_ROP_REG, 0x3100); \
    cutscene_egc_write(EGC_BITLENGTHREG, 0xF); \
    outport(EGC_MASKREG, mask); \
}

inline void cutscene_script_free(void) {}
bool16 pascal near cutscene_script_load(const char far *filename);
#ifndef TH05_CUTSCENE_IMPLEMENTATION
void near cutscene_animate(void);
#endif

typedef char th05_cutscene_bool_is_1[(sizeof(bool) == 1) ? 1 : -1];
typedef char th05_cutscene_screen_point_is_4[(sizeof(screen_point_t) == 4) ? 1 : -1];
typedef char th05_cutscene_kanji_is_2[(sizeof(ShiftJISKanji) == 2) ? 1 : -1];
typedef char th05_cutscene_mask_is_8[(sizeof(dot_rect_t(16, 4)) == 8) ? 1 : -1];
typedef char th05_cutscene_vram_pointer_is_4[(sizeof(VRAM_PLANE_B) == 4) ? 1 : -1];

#endif
