// Local OP menu interfaces, preserving real Borland large-model ABI.
// Natural-source provenance: nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: OP/start/menu and graphics/sound headers.
#ifndef TH05_OP_MAIN_MENU_HPP
#define TH05_OP_MAIN_MENU_HPP

#include "src/main/hud/resident.hpp"

typedef char int8_t;
typedef int screen_x_t;
typedef int screen_y_t;
typedef int vram_y_t;
typedef uint8_t shiftjis_t;
typedef unsigned int vc2;
typedef void (near pascal *near menu_unput_and_put_func_t)(int sel, vc2 col);
#define RES_X 640
#define RES_Y 400
#define GLYPH_H 16
#define GLYPH_FULL_W 16
#define GLYPH_HALF_W 8
#define GC_RMW 0xC0
#define V_WHITE 15
#define CFG_LIVES_MAX 6
#define CFG_LIVES_DEFAULT 3
static const int CFG_BOMBS_MAX = 3;
#define CFG_BOMBS_DEFAULT CFG_BOMBS_MAX
static const int STAGE_EXTRA = 6;
static const int ES_SCORE = 0;

typedef enum {
	RANK_EASY,
	RANK_NORMAL,
	RANK_HARD,
	RANK_LUNATIC,

	// Hi Asprey, there is no unused Extra rank in TH01.
	// (https://www.youtube.com/watch?v=RcjhM4tfPq4&t=169s)

	RANK_EXTRA,


	RANK_COUNT,


	// Triggering the first-launch setup menu via a special rank value...
	// Definitely unique.
	RANK_SHOW_SETUP_MENU = 0xFF,


	_rank_t_FORCE_INT16 = 0x7FFF
} rank_t;

typedef enum {
	PLAYCHAR_REIMU = 0,
	PLAYCHAR_MARISA = 1,
	PLAYCHAR_MIMA = 2,
	PLAYCHAR_YUUKA = 3,
	PLAYCHAR_COUNT = 4,

	_playchar_t_FORCE_UINT8 = 0xFF
} playchar_t;

typedef enum {
	SND_BGM_OFF = 0,
	SND_BGM_FM26 = 1,
	SND_BGM_FM86 = 2,
	SND_BGM_MODE_COUNT = 3,
	SND_BGM_MIDI = 3, // unsupported

	_snd_bgm_mode_t_FORCE_UINT8 = 0xFF
} snd_bgm_mode_t;

typedef enum {
	SND_SE_OFF = 0,
	SND_SE_FM = 1,
	SND_SE_BEEP = 2,
	SND_SE_MODE_COUNT = 3,

	_snd_se_mode_t_FORCE_INT16 = 0x7FFF
} snd_se_mode_t;

typedef enum {
	// sft1.cd2
	// --------
	CDG_NUMERAL = 0,
	CDG_NUMERAL_last = (CDG_NUMERAL + 9),
	// --------
	// sft2.cd2
	// --------
	CDG_MAIN,
	CDG_MAIN_GAME = CDG_MAIN,
	CDG_MAIN_EXTRA,
	CDG_MAIN_REGIST_VIEW,
	CDG_MAIN_MUSICROOM,
	CDG_MAIN_OPTION,
	CDG_QUIT,

	CDG_OPTION_LABEL_RANK,
	CDG_OPTION_LABEL_LIVES,
	CDG_OPTION_LABEL_BOMBS,
	CDG_OPTION_LABEL_BGM,
	CDG_OPTION_LABEL_SE,

	CDG_OPTION_VALUE_RANK,
	CDG_OPTION_VALUE_RANK_last = (CDG_OPTION_VALUE_RANK + RANK_LUNATIC),

	CDG_OPTION_VALUE_BGM,
	CDG_OPTION_VALUE_BGM_last = (
		CDG_OPTION_VALUE_BGM + (SND_BGM_MIDI - SND_BGM_FM26)
	),

	CDG_OPTION_VALUE_OFF,

	// ZUN bloat: Does not match the order in snd_se_mode_t.
	CDG_OPTION_VALUE_SE_BEEP,
	CDG_OPTION_VALUE_SE_FM,

	CDG_OPTION_RESET,

	CDG_OPTION_TURBO,
	CDG_OPTION_SLOW,
	CDG_EMPTY,
	// --------

	// car.cd2
	// -------
	CDG_CURSOR,
	CDG_CURSOR_LEFT = CDG_CURSOR,
	CDG_CURSOR_RIGHT,
	// -------

	CDG_PIC = 40,
	CDG_PIC_last = (CDG_PIC + PLAYCHAR_COUNT - 1),
	CDG_CLEARED,
	CDG_PIC_NOT_CLEARED,

	_op_cdg_slot_t_FORCE_INT16 = 0x7FFF
} op_cdg_slot_t;


enum graph_putsa_fx_func_t {
    FX_WEIGHT_NORMAL = 0, FX_WEIGHT_HEAVY = 1,
    FX_WEIGHT_BOLD = 2, FX_WEIGHT_BLACK = 3,
    FX_MASK, FX_MASK_1 = FX_MASK, FX_MASK_2, FX_MASK_3, FX_MASK_4, FX_MASK_END,
    _graph_putsa_fx_func_FORCE_INT16 = 0x7FFF
};
enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
static const int KAJA_SONG_PLAY = 0;
static const int KAJA_SONG_STOP = 1;
static const int KAJA_SONG_FADE = 2;
static const uint8_t INPUT_UP = 0x01;
static const uint8_t INPUT_DOWN = 0x02;
static const uint8_t INPUT_LEFT = 0x04;
static const uint8_t INPUT_RIGHT = 0x08;
static const uint8_t INPUT_SHOT = 0x20;
static const uint16_t INPUT_CANCEL = 0x1000;
static const uint16_t INPUT_OK = 0x2000;

extern bool extra_unlocked;
extern bool extra_playable_with[PLAYCHAR_COUNT];
extern uint16_t key_det;
extern unsigned int mem_assign_paras;
extern unsigned int PaletteTone;
extern graph_putsa_fx_func_t graph_putsa_fx_func;
extern int8_t menu_sel;
extern int8_t in_option;
extern bool quit;
extern menu_unput_and_put_func_t menu_unput_and_put;
extern const shiftjis_t far *MENU_DESC[26];

void near start_game(void);
void near start_extra(void);
void near start_demo(void);
void near setup_menu(void);
void near zunsoft_animate(void);
void near main_cdg_load(void);
void near main_cdg_free(void);
void near op_animate(void);
void near regist_view_menu(void);
void near cleardata_and_regist_view_sprites_load(void);
int near playchar_menu(void);
void near musicroom_menu(void);
void near cfg_load(void);
void near cfg_save(void);
void near cfg_save_exit(void);
void far game_exit(void);
void far game_exit_to_dos(void);
int far game_init_op(const unsigned char far *pf_fn);
int far input_reset_sense_held(void);
void pascal far frame_delay(int frames);
void pascal far egc_copy_rect_1_to_0_16(screen_x_t left, vram_y_t top,
    pixel_t width, pixel_t height);
int pascal far pi_load(int slot, const char far *filename);
void pascal far pi_palette_apply(int slot);
void pascal far pi_put_8(screen_x_t left, vram_y_t top, int slot);
void pascal far pi_free(int slot);

extern "C" {
    void pascal far dos_puts2(const char far *text);
    int pascal far respal_create(void);
    void pascal far respal_free(void);
    int pascal far graph_copy_page(int to_page);
    void pascal far grcg_setcolor(int mode, vc2 color);
    void pascal far palette_show(void);
    void pascal far palette_black_out(unsigned int speed);
    void pascal far text_clear(void);
    int pascal far snd_kaja_interrupt(int ax);
    void far snd_se_reset(void);
    void pascal far snd_se_play(int new_se);
    void far snd_se_update(void);
    int pascal far snd_determine_modes(int bgm, int se);
    void pascal far snd_load(const char far *filename, snd_load_func_t func);
    void pascal far graph_putsa_fx(screen_x_t left, vram_y_t top,
        vc2 color, const shiftjis_t far *text);
    void pascal far cdg_put_8(screen_x_t left, vram_y_t top, int slot);
    void pascal far cdg_put_nocolors_8(screen_x_t left, vram_y_t top, int slot);
}

#define graph_accesspage(page_value) outportb(0xA6, page_value)
#define grcg_off() outportb(0x7C, 0)
#define palette_100() (PaletteTone = 100, palette_show())
#define snd_kaja_func(function_value, parameter_value) \
    snd_kaja_interrupt(((function_value) << 8) | static_cast<uint8_t>(parameter_value))
#define snd_se_play_force(new_se_value) { \
    snd_se_reset(); snd_se_play(new_se_value); snd_se_update(); \
}
#define input_reset_sense_interface input_reset_sense_held
#define pi_fullres_load_palette_apply_put_free(slot_value, filename_value) { \
    pi_load(slot_value, filename_value); pi_palette_apply(slot_value); \
    pi_put_8(0, 0, slot_value); pi_free(slot_value); \
}

void pascal near menu_sel_update_and_render(int8_t max, int8_t direction);
#define menu_update_vertical(input_value, choice_count_value) { \
    if(input_value & INPUT_UP) { \
        menu_sel_update_and_render((choice_count_value - 1), -1); \
    } \
    if(input_value & INPUT_DOWN) { \
        menu_sel_update_and_render((choice_count_value - 1), +1); \
    } \
}

#define ring_inc_range(val, ring_min, ring_max) { \
	(val)++; \
	if((val) > (ring_max)) { \
		(val) = (ring_min); \
	} \
}

#define ring_inc_ge_range(val, ring_min, ring_max) { \
	(val)++; \
	if((val) >= ((ring_max) + 1)) { \
		(val) = (ring_min); \
	} \
}


#define ring_dec_range(val, ring_min, ring_max) { \
	if(val == (ring_min)) { \
		(val) = ((ring_max) + 1); \
	} \
	(val)--; \
}

typedef char th05_op_menu_callback_is_2[(sizeof(menu_unput_and_put_func_t) == 2) ? 1 : -1];
typedef char th05_op_menu_string_pointer_is_4[(sizeof(const shiftjis_t far *) == 4) ? 1 : -1];
typedef char th05_op_menu_rank_is_2[(sizeof(rank_t) == 2) ? 1 : -1];
typedef char th05_op_menu_cdg_slot_is_2[(sizeof(op_cdg_slot_t) == 2) ? 1 : -1];
typedef char th05_op_menu_effect_is_2[(sizeof(graph_putsa_fx_func_t) == 2) ? 1 : -1];
typedef char th05_op_menu_se_mode_is_2[(sizeof(snd_se_mode_t) == 2) ? 1 : -1];
typedef char th05_op_menu_bgm_mode_is_1[(sizeof(snd_bgm_mode_t) == 1) ? 1 : -1];
typedef char th05_op_menu_playchar_is_1[(sizeof(playchar_t) == 1) ? 1 : -1];
typedef char th05_op_menu_sound_load_is_2[(sizeof(snd_load_func_t) == 2) ? 1 : -1];
typedef char th05_op_menu_resident_pointer_is_4[(sizeof(resident_t far *) == 4) ? 1 : -1];

#endif
