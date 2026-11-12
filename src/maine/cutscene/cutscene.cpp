// Natural TH05 MAINE cutscene interpreter, adapted from pinned ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47, th03/cutscene/cutscene.cpp.
// Candidate only. Real EGC port intrinsics replace the reference ASM macro.
#pragma option -zCCUTSCENE_TEXT -zPgroup_01
#define TH05_CUTSCENE_IMPLEMENTATION
#include "src/maine/cutscene/cutscene.hpp"

static const screen_y_t CUTSCENE_PIC_TOP = 64;
static const int CUTSCENE_PIC_SLOT = 0;

static const screen_x_t BOX_LEFT = 80;
static const screen_y_t BOX_TOP = 320;
static const pixel_t BOX_W = 480;
static const pixel_t BOX_H = (GLYPH_H * 4);

static const vram_byte_amount_t BOX_VRAM_W = (BOX_W / BYTE_DOTS);
static const screen_x_t BOX_RIGHT = (BOX_LEFT + BOX_W);
static const screen_y_t BOX_BOTTOM = (BOX_TOP + BOX_H);

static const screen_x_t RETURN_LEFT = (BOX_RIGHT + GLYPH_FULL_W);

static const shiftjis_ank_amount_t NAME_LEN = 6;
static const shiftjis_kanji_amount_t NAME_KANJI_LEN = (
	NAME_LEN / sizeof(shiftjis_kanji_t)
);

static const pixel_t NAME_W = ((NAME_LEN * GLYPH_HALF_W) + GLYPH_FULL_W);

static const int TEXT_INTERVAL_DEFAULT = ((GAME == 5) ? 2 : 1);

unsigned char script[8192];

unsigned char near *script_p;

Planar<dots16_t> far *box_bg;

bool fast_forward;

// Reference-correlated unused runtime state. Its ownership/type is unaccepted;
// the original only independently corroborates the surrounding touched offsets.
static int8_t unused[60];

static const int COLMAP_COUNT = 8;

struct colmap_t {
	vc_t values[COLMAP_COUNT];

	ShiftJISKanji keys[COLMAP_COUNT][NAME_KANJI_LEN];
};

colmap_t colmap;
extern unsigned char colmap_count;
static int8_t padding; // Reference-correlated unused byte; no authored credit.
typedef char th05_cutscene_colmap_is_56[(sizeof(colmap_t) == 56) ? 1 : -1];
typedef char th05_cutscene_colmap_keys_at_8[(offsetof(colmap_t, keys) == 8) ? 1 : -1];

screen_point_t cursor;

int text_interval;
vc_t text_col;
uint8_t text_fx;

#define text_fx graph_putsa_fx_func

#pragma option -a2

inline void cutscene_input_sense(void) {
	input_reset_sense_held();
}

bool16 pascal near cutscene_script_load(const char* fn)
{
	cutscene_script_free();

	if(!file_ropen(fn)) {
		return true;
	}
	size_t size = file_size();

	script_p = static_cast<unsigned char near *>(script);
	file_read(script_p, size);
	file_close();
	return false;
}

void near egc_start_copy(void)
{
    egc_on();
    cutscene_egc_write(EGC_ACTIVEPLANEREG, 0xFFF0);
    cutscene_egc_write(EGC_READPLANEREG, 0x00FF);
    cutscene_egc_write(EGC_MODE_ROP_REG, 0x3100);
    cutscene_egc_write(EGC_MASKREG, 0xFFFF);
#ifdef TH05_CUTSCENE_JOINED
    // The original word-write must use MOV, not flag-changing XOR.
    asm { mov ax, 0 }
    _DX = EGC_ADDRRESSREG;
    outport(_DX, _AX);
#else
    cutscene_egc_write(EGC_ADDRRESSREG, 0);
#endif
    cutscene_egc_write(EGC_BITLENGTHREG, 0xF);
}

// The complete EGC helper above remains inexact. The independent linker
// context preserves one uncredited byte between these CODE contributions;
// no byte or instruction is supplied inside either compiler-owned function.
#ifdef TH05_CUTSCENE_JOINED
#pragma codeseg CUTSCENE_TEXT group_01
#else
#pragma codeseg CUTSCENE_AFTER_TEXT group_01
#endif
void near cutscene_animate(void);
void pascal near box_wait_animate(int frames_to_wait = 0);
void near box_1_to_0_animate(void);

#define pic_copy_to_other(left, top) { \
	egc_copy_rect_1_to_0_16(left, top, CUTSCENE_PIC_W, CUTSCENE_PIC_H); \
}

void pascal near pic_put_both_masked(
	screen_x_t left, vram_y_t top, int quarter, int mask_id
)
{
	graph_accesspage(1);
	pi_put_quarter_masked_8(left, top, CUTSCENE_PIC_SLOT, quarter, mask_id);
	pic_copy_to_other(left, top);
}

#include "src/maine/cutscene/script.hpp"

void near cursor_advance_and_animate(void)
{
	cursor.x += GLYPH_FULL_W;
	if(cursor.x >= BOX_RIGHT) {
		cursor.y += GLYPH_H;
		cursor.x = (BOX_LEFT + NAME_W);

		if(cursor.y >= BOX_BOTTOM) {
			box_1_to_0_animate();

			if(!fast_forward) {
				box_wait_animate(0);
			}

			cursor.x = BOX_LEFT;
			cursor.y = BOX_TOP;

		}
	}
}

typedef enum {
	BOX_MASK_0,
	BOX_MASK_1,
	BOX_MASK_2,
	BOX_MASK_3,
	BOX_MASK_COPY,
	BOX_MASK_COUNT,

	_box_mask_t_FORCE_UINT16 = 0xFFFF
} box_mask_t;

void pascal near box_1_to_0_masked(box_mask_t mask)
{
	extern const dot_rect_t(16, 4) BOX_MASKS[BOX_MASK_COUNT];
	egc_temp_t tmp;

	for(screen_y_t y = BOX_TOP; y < BOX_BOTTOM; y++) {
		egc_setup_copy_masked(BOX_MASKS[mask][y & 3]);

		vram_offset_t vram_offset = vram_offset_shift(BOX_LEFT, y);
		pixel_t x = 0;
		while(x < BOX_W) {
			graph_accesspage(1);	tmp = egc_chunk(vram_offset);
			graph_accesspage(0);	egc_chunk(vram_offset) = tmp;
			x += EGC_REGISTER_DOTS;
			vram_offset += EGC_REGISTER_SIZE;
		}
	}
}

void near box_1_to_0_animate(void)
{

	graph_accesspage(0);

	egc_start_copy();
	if(!fast_forward) {
		for(int i = BOX_MASK_0; i < BOX_MASK_COPY; i++) {
			box_1_to_0_masked(static_cast<box_mask_t>(i));
			frame_delay(text_interval);
		}
	}
	box_1_to_0_masked(BOX_MASK_COPY);
	egc_off();

	frame_delay(1);
}

void pascal near box_wait_animate(int frames_to_wait)
{
	unsigned int frame = 0;
	bool16 ignore_frames = false;

	while(1) {
		cutscene_input_sense();
		if(key_det == INPUT_NONE) {
			break;
		}
		frame_delay(1);
	}

	if(frames_to_wait == 0) {
		frames_to_wait = 999;
		ignore_frames = true;
	}

	graph_accesspage(0);
	while(1) {
		cutscene_input_sense();

		bgimage_put_rect_16(RETURN_LEFT, cursor.y, GLYPH_FULL_W, GLYPH_H);

		if(
			(frames_to_wait <= 0) ||
			(key_det & INPUT_OK) ||
			(key_det & INPUT_SHOT) ||
			(key_det & INPUT_CANCEL)
		) {
			return;
		}
		graph_gaiji_putc(
			RETURN_LEFT,
			cursor.y,
			(ga_RETURN_KEY + ((frame / 8) % RETURN_KEY_CELS)),
			V_WHITE
		);
		frame++;
		if(!ignore_frames) {
			frames_to_wait--;
		}
		frame_delay(1);
	}
}

#ifndef CUTSCENE_SCRIPT_DEFAULT_COLOR
#define CUTSCENE_SCRIPT_DEFAULT_COLOR V_WHITE
#endif
// TH05's script is a byte-oriented control language. These 16 command
// letters are the real sparse-switch keys; keeping the original ASCII values
// is part of the original 64-byte Borland switch-table contract.
// Subcommands (such as `wi`/`wo`, `fm`, `vp`, `p=` and `p-`) are parsed by the
// corresponding handlers, not additional top-level opcode values.
enum CutsceneCommandByte {
    CUTSCENE_CMD_NEWLINE = 'n',
    CUTSCENE_CMD_NEW_TEXT_BOX = 's',
    CUTSCENE_CMD_TEXT_COLOR_OR_COLOR_MAP = 'c',
    CUTSCENE_CMD_FONT_WEIGHT = 'b',
    CUTSCENE_CMD_WHITE_FADE_OR_WAIT = 'w',
    CUTSCENE_CMD_TEXT_INTERVAL_OR_DISPLAY_PAGE = 'v',
    CUTSCENE_CMD_PALETTE_TONE = 't',
    CUTSCENE_CMD_BLACK_FADE_OR_SONG_FADE = 'f',
    CUTSCENE_CMD_SCREEN_SHAKE_OR_GAIJI = 'g',
    CUTSCENE_CMD_RETURN_KEY_WAIT = 'k',
    CUTSCENE_CMD_CLEAR_BOTH_PAGES = '@',
    CUTSCENE_CMD_PICTURE_RESOURCE = 'p',
    CUTSCENE_CMD_PICTURE_QUARTER = '=',
    CUTSCENE_CMD_BGM_CONTROL = 'm',
    CUTSCENE_CMD_SOUND_EFFECT = 'e',
    CUTSCENE_CMD_END_SCRIPT = '$',
};

#include "src/maine/cutscene/subcommands.hpp"

script_ret_t pascal near script_op(unsigned char c)
{

	#define palette_black_in(x)  palette_black_in(x);  return CONTINUE;
	#define palette_black_out(x) palette_black_out(x); return CONTINUE;
	#define palette_white_in(x)  palette_white_in(x);  return CONTINUE;
	#define palette_white_out(x) palette_white_out(x); return CONTINUE;

	int i;
	int p1;
	int p2;

	char fn[PF_FN_LEN + 3];

	c = tolower(c);
	switch(c) {
	case CUTSCENE_CMD_NEWLINE:
		cursor.y += GLYPH_H;
		cursor.x = BOX_LEFT;
		if(cursor.y < BOX_BOTTOM) {
			break;
		}

	case CUTSCENE_CMD_NEW_TEXT_BOX:
		c = *script_p;
		box_1_to_0_animate();
		if(c != CUTSCENE_BOX_SKIP_WAIT) {
			script_param_read_number_first(p1, 0);
			if(!fast_forward) {
				box_wait_animate(p1);
			}
		} else {
			script_p++;
		}
		cursor.x = BOX_LEFT;
		cursor.y = BOX_TOP;

		graph_accesspage(CUTSCENE_PAGE_BACKGROUND);
		bgimage_put_rect_16(BOX_LEFT, BOX_TOP, BOX_W, BOX_H);

		graph_accesspage(CUTSCENE_PAGE_FOREGROUND);
		break;

	case CUTSCENE_CMD_TEXT_COLOR_OR_COLOR_MAP:

		c = tolower(*script_p);

		if(c == CUTSCENE_COLOR_MAP_ASSIGN) {
			goto colmap_add;
		}
		script_param_read_number_first(p1, CUTSCENE_SCRIPT_DEFAULT_COLOR);
		text_col = p1;
		break;

	case CUTSCENE_CMD_FONT_WEIGHT:
		script_param_read_number_first(p1, WEIGHT_BOLD);
		graph_putsa_fx_func = static_cast<graph_putsa_fx_func_t>(p1);
		break;

	case CUTSCENE_CMD_WHITE_FADE_OR_WAIT:
		c = tolower(*script_p);
		if((c == CUTSCENE_FADE_OUT) || (c == CUTSCENE_FADE_IN)) {
			script_op_fade(c, palette_white_in, palette_white_out, p1);
		} else {
			box_1_to_0_animate();
			script_param_number_default = CUTSCENE_WAIT_DEFAULT_FRAMES;
			if(c != CUTSCENE_WAIT_FOR_MEASURE) {
				if(c == CUTSCENE_WAIT_EXTRA_KEY) {
					script_p++;
				}
				script_param_read_number_first(p1);
				if(!fast_forward) {
					frame_delay(p1);
					return CONTINUE;
				}
			} else {
				script_p++;
				c = *script_p;
				if(c == CUTSCENE_WAIT_EXTRA_KEY) {
					script_p++;
				}
				script_param_read_number_first(p1);
				script_param_read_number_second(p2);
				if(!fast_forward) {

					snd_delay_until_measure(p1, p2);
				}
			}
		}
		break;

	case CUTSCENE_CMD_TEXT_INTERVAL_OR_DISPLAY_PAGE:
		if(*script_p != CUTSCENE_SHOW_PAGE) {
			script_param_read_number_first(p1, TEXT_INTERVAL_DEFAULT);
			text_interval = p1;
		} else {
			script_p++;
			script_param_read_number_first(p1, 0);
			graph_showpage(p1);
		}
		break;

	case CUTSCENE_CMD_PALETTE_TONE:
		script_param_read_number_first(p1, CUTSCENE_TONE_NORMAL);
		if(!fast_forward) {
			frame_delay(CUTSCENE_TONE_APPLY_FRAMES);
		}
		palette_settone(p1);
		break;

	case CUTSCENE_CMD_BLACK_FADE_OR_SONG_FADE:
		c = *script_p;
		if(c != CUTSCENE_FADE_MUSIC) {
			if((c == 'i') || (c == 'o')) {
				script_op_fade(c, palette_black_in, palette_black_out, p1);
			}
		} else {
			script_p++;
			script_param_read_number_first(p1, CUTSCENE_DEFAULT_MEASURE_FADE);

			snd_kaja_interrupt((KAJA_SONG_FADE << 8) + p1);

		}
		break;

	case CUTSCENE_CMD_SCREEN_SHAKE_OR_GAIJI:
		if((GAME == 5) || (*script_p != CUTSCENE_GAIJI_DIRECT)) {
			script_op_shake(fast_forward, p2, p1);
		} else {
			script_p++;
			script_param_read_number_first(p1, 0);

			graph_accesspage(CUTSCENE_PAGE_BACKGROUND);

			graph_gaiji_putc(cursor.x, cursor.y, p1, text_col);

			cursor_advance_and_animate();
		}
		return CONTINUE;

	case CUTSCENE_CMD_RETURN_KEY_WAIT:

		box_1_to_0_animate();

		script_param_read_number_first(p1, 0);
		if(!fast_forward) {

			box_wait_animate((GAME >= 4) ? p1 : 0);
		}
		return CONTINUE;

	case CUTSCENE_CMD_CLEAR_BOTH_PAGES:
		graph_accesspage(CUTSCENE_PAGE_BACKGROUND);	graph_clear();
		graph_accesspage(CUTSCENE_PAGE_FOREGROUND);	graph_clear();
		bgimage_snap();
		break;

	case CUTSCENE_CMD_PICTURE_RESOURCE:
		c = *script_p;
		script_p++;

		if((c == CUTSCENE_PIC_USE_PALETTE) || (c == CUTSCENE_PIC_KEEP_PALETTE)) {
			graph_accesspage(CUTSCENE_PAGE_BACKGROUND);
			if(c == CUTSCENE_PIC_USE_PALETTE) {
				pi_palette_apply(CUTSCENE_PIC_SLOT);
			}
			pi_put_8(0, 0, CUTSCENE_PIC_SLOT);
			graph_copy_page(0);
			graph_accesspage(CUTSCENE_PAGE_FOREGROUND);
			bgimage_snap();
		} else if(c == CUTSCENE_PIC_FREE) {
			pi_free(CUTSCENE_PIC_SLOT);
			return CONTINUE;
		} else if(c == CUTSCENE_PIC_PALETTE_ONLY) {
			pi_palette_apply(CUTSCENE_PIC_SLOT);
			return CONTINUE;
		} else if(c != CUTSCENE_PIC_LOAD_NAME) {
			script_p--;
		} else {
			script_param_read_fn(fn, p1, c);
			pi_free(CUTSCENE_PIC_SLOT);
			pi_load(CUTSCENE_PIC_SLOT, fn);
		}
		break;

	case CUTSCENE_CMD_PICTURE_QUARTER:
		script_param_number_default = PI_QUARTER_COUNT;
		c = *script_p;

		if(c != CUTSCENE_QUARTER_TRANSITION) {
			script_param_read_number_first(p1);
			frame_delay(CUTSCENE_QUARTER_TRANSITION_DELAY);
			graph_showpage(CUTSCENE_PAGE_FOREGROUND);
			graph_accesspage(CUTSCENE_PAGE_BACKGROUND);
			if(p1 < PI_QUARTER_COUNT) {
				pi_put_quarter_8(
					CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP, CUTSCENE_PIC_SLOT, p1
				);
			} else {
				grcg_setcolor(GC_RMW, 0);
				grcg_boxfill_8(
					CUTSCENE_PIC_LEFT,
					CUTSCENE_PIC_TOP,
					(CUTSCENE_PIC_LEFT + CUTSCENE_PIC_W - 1),
					(CUTSCENE_PIC_TOP  + CUTSCENE_PIC_H - 1)
				);
				grcg_off();
			}
		} else {
			script_p++;
			script_param_read_number_first(p1);
			script_param_number_default = 1;
			script_param_read_number_second(p2);
			for(i = 0; i < PI_MASK_COUNT; i++) {
				pic_put_both_masked(CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP, p1, i);
				if(!fast_forward) {
					frame_delay(p2);
				}
			}
			graph_accesspage(CUTSCENE_PAGE_BACKGROUND);
			pi_put_quarter_8(
				CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP, CUTSCENE_PIC_SLOT, p1
			);
			frame_delay(CUTSCENE_QUARTER_TRANSITION_DELAY);
		}
		typedef char pic_width_matches_quarter[(CUTSCENE_PIC_W == PI_QUARTER_W) ? 1 : -1];
		typedef char pic_height_matches_quarter[(CUTSCENE_PIC_H == PI_QUARTER_H) ? 1 : -1];
		pic_copy_to_other(CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP);
		break;

	case CUTSCENE_CMD_BGM_CONTROL:

		script_op_bgm(true, c, fn, p1);
		break;

	case CUTSCENE_CMD_SOUND_EFFECT:
		script_param_read_number_first(p1);
		snd_se_play_force(p1);
		break;

colmap_add:
	script_p++;
	colmap.keys[colmap_count][0].byte[0] = *script_p;
	script_p++;
	colmap.keys[colmap_count][0].byte[1] = *script_p;

	script_p += 2;

	script_param_read_number_first(p1, V_WHITE);

	colmap.values[colmap_count] = p1;
	colmap_count++;
	break;

	case CUTSCENE_CMD_END_SCRIPT:
		return STOP;
	}
	return CONTINUE;
}

void near cutscene_animate(void)
{
	extern ShiftJISKanji near CUTSCENE_KANJI[];

	int gaiji;
	unsigned char c;
	uint8_t speedup_cycle;

	ShiftJISKanji& kanji = *CUTSCENE_KANJI;

	cursor.x = BOX_LEFT;
	cursor.y = BOX_TOP;
	text_interval = TEXT_INTERVAL_DEFAULT;
	text_col = V_WHITE;
	text_fx = FX_WEIGHT_BOLD;

	fast_forward = false;

	while(1) {
		cutscene_input_sense();
		if(key_det & INPUT_CANCEL) {
			fast_forward = true;
		} else {
			fast_forward = false;
		}

		int i = 0;

		c = *(script_p++);
		if(str_sep_control_or_space(c)) {
			continue;
		}

		if(c == CUTSCENE_ESCAPE_COMMAND) {
			c = *(script_p++);
			if(script_op(c) == STOP) {
				break;
			}
			continue;
		}

		if(c == CUTSCENE_INLINE_GAIJI) {
			c = tolower(*script_p);
			script_p++;
			switch(c) {
			case CUTSCENE_INLINE_SWEAT:
				gaiji = gs_SWEAT;
				break;

			case CUTSCENE_INLINE_HEART:
				gaiji = gs_HEART_2;
				break;

			case CUTSCENE_INLINE_QUESTION:
				gaiji = gs_QUESTION;
				break;

			case CUTSCENE_INLINE_EXCLAMATION:
				c = *(script_p++);
				switch(c) {
				case CUTSCENE_INLINE_EXCLAMATION:
					gaiji = gs_DOUBLE_EXCLAMATION;
					break;

				case CUTSCENE_INLINE_QUESTION:
					gaiji = gs_EXCLAMATION_QUESTION;
					break;

				default:
					script_p--;
					gaiji = gs_EXCLAMATION;
					break;
				}
				break;

			default:
				script_p--;
				script_param_read_number_first(gaiji, gs_NOTES);
				break;
			}
			graph_showpage(CUTSCENE_PAGE_FOREGROUND);
			graph_accesspage(CUTSCENE_PAGE_BACKGROUND);

			graph_gaiji_putc(cursor.x, cursor.y, gaiji, text_col);

			cursor_advance_and_animate();
			i = 1;
			continue;
		}

		kanji.byte[0] = c;
		c = *script_p;
		kanji.byte[1] = c;
		script_p++;

		if(cursor.x == BOX_LEFT) {
			for(i = 0; i < colmap_count; i++) {
				if(colmap.keys[i][0].t == kanji.t) {
					text_col = colmap.values[i];
					break;
				}
			}
		}

		graph_showpage(CUTSCENE_PAGE_FOREGROUND);
		graph_accesspage(CUTSCENE_PAGE_BACKGROUND);
		graph_putsa_fx(cursor.x, cursor.y, text_col, kanji.byte);

		graph_accesspage(CUTSCENE_PAGE_FOREGROUND);
		cursor_advance_and_animate();
		i = 1;

	}
	bgimage_free();
	pi_free(CUTSCENE_PIC_SLOT);
}
