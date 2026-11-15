// MAINE's cutscene script interpreter, which plays the ending scripts
// (_ED??.TXT). Adapted from ReC98 th03/cutscene/cutscene.cpp (GAME == 5).
//
// TH05 renders all text and pictures onto the invisible VRAM page 1, and then
// crossfades the text box onto the visible page 0 in box_1_to_0_animate().
// The text box background is restored through the bgimage system.
//
// This file is compiled in two configurations:
// * through cutscene_joined.cpp (TH05_CUTSCENE_JOINED), with every function
//   in the single CUTSCENE_TEXT segment of the original. This is the layout
//   that reproduces script_op()'s relocation order.
// * directly, with everything after egc_start_copy() moved to a separate
//   CUTSCENE_AFTER_TEXT segment. The other nine functions also match in this
//   configuration; egc_start_copy() itself is matched by egc_setup_exact.cpp.
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

// Adding a fullwidth colon after the name
static const pixel_t NAME_W = ((NAME_LEN * GLYPH_HALF_W) + GLYPH_FULL_W);

static const int TEXT_INTERVAL_DEFAULT = ((GAME == 5) ? 2 : 1);

// ZUN landmine: cutscene_script_load() doesn't check whether the script
// actually fits into this buffer.
unsigned char script[8192];

unsigned char near *script_p;

// Unused in TH05, which uses the bgimage system instead.
Planar<dots16_t> far *box_bg;

// Skips any delays during the cutscene if `true`.
bool fast_forward;

static int8_t unused[60]; // ZUN bloat

// String-to-color map
// -------------------
// Used to automatically change the text color whenever a specific Shift-JIS
// code point is encountered at the start of a line.

static const int COLMAP_COUNT = 8;

struct colmap_t {
	vc_t values[COLMAP_COUNT];

	// Might have been originally meant for a complete character name?
	ShiftJISKanji keys[COLMAP_COUNT][NAME_KANJI_LEN];
};

colmap_t colmap;
extern unsigned char colmap_count; // Defined in box_mask_patterns.c.
static int8_t padding; // ZUN bloat
// -------------------

// [y] is always aligned to GLYPH_H pixels.
screen_point_t cursor;

int text_interval;
vc_t text_col;
uint8_t text_fx; // Unused; TH05 directly sets [graph_putsa_fx_func].

#define text_fx graph_putsa_fx_func

#pragma option -a2

// ZUN quirk: The top-level loop senses input once per command to update the
// fast-forward flag, while the wait commands run their own blocking input
// loops that are skipped while fast-forwarding. The "held" variant of the
// input function prevents a momentary key-release scancode from entering such
// a wait loop while the fast-forward key is still held, at the cost of about
// 0.6 ms per call. (See ReC98 for the TH03/TH04 comparison.)
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

	// ZUN landmine: No check whether [size] >= sizeof(script).
	script_p = static_cast<unsigned char near *>(script);
	file_read(script_p, size);
	file_close();
	return false;
}

// Sets up the EGC for a 16-dot inter-page copy of all four planes.
void near egc_start_copy(void)
{
    egc_on();
    cutscene_egc_write(EGC_ACTIVEPLANEREG, 0xFFF0);
    cutscene_egc_write(EGC_READPLANEREG, 0x00FF);
    cutscene_egc_write(EGC_MODE_ROP_REG, 0x3100);
    cutscene_egc_write(EGC_MASKREG, 0xFFFF);
#ifdef TH05_CUTSCENE_JOINED
    // The original loads the zero with MOV AX, 0; assigning 0 to _AX would
    // compile to the one byte shorter XOR AX, AX.
    asm { mov ax, 0 }
    _DX = EGC_ADDRRESSREG;
    outport(_DX, _AX);
#else
    cutscene_egc_write(EGC_ADDRRESSREG, 0);
#endif
    cutscene_egc_write(EGC_BITLENGTHREG, 0xF);
}

// In the split configuration, the linker scaffold reserves the byte that the
// XOR version of egc_start_copy() is short by, so that everything below still
// lands at its original address.
#ifdef TH05_CUTSCENE_JOINED
#pragma codeseg CUTSCENE_TEXT group_01
#else
#pragma codeseg CUTSCENE_AFTER_TEXT group_01
#endif
// Function ordering fails
// -----------------------

void near cutscene_animate(void);

// Waits the given amount of frames (0 = forever) for the OK, Shot, or Cancel
// button to be pressed, while showing the Return key animation in a blocking
// way.
void pascal near box_wait_animate(int frames_to_wait = 0);

// Crossfades the text box area from VRAM page 1 to VRAM page 0, spending
// [text_interval] frames on each step.
void near box_1_to_0_animate(void);
// -----------------------

// Picture crossfading works by doing a masked blit of the new picture on top
// of the old one on the invisible VRAM page, then blitting the result to the
// visible page using an EGC inter-page copy. Blitting the packed-pixel .PI
// data directly to the visible page could easily take more than one frame on
// lower-end systems.
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

			// ZUN quirk: Since [cursor.y] is >= BOX_BOTTOM here, the Return
			// key animation will be displayed at the right edge of the "5th"
			// line, below BOX_BOTTOM. (Same issue as with the \n command.)
			if(!fast_forward) {
				box_wait_animate(0);
			}

			// Unconditionally moving the cursor into the name area? This is
			// not what a script author would expect, especially with automatic
			// line breaks doing the opposite.
			cursor.x = BOX_LEFT;
			cursor.y = BOX_TOP;

			// ZUN landmine: The \s command is the only place where text is
			// unblitted from any page. Any text in an automatically started
			// new box will be blitted on top of the old one.
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

// Copies the text box area from VRAM page 1 to VRAM page 0, applying the
// given [mask]. Assumes that the EGC is active, and initialized for a copy.
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
	// ZUN bloat: box_1_to_0_masked() switches the accessed page anyway.
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

	frame_delay(1); // ZUN quirk
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

		// ZUN bloat: A white glyph aligned to the 8x16 cell grid, without
		// applying boldface... why not just show it on TRAM?
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

// Default text color for the \c command. cutscene_joined.cpp spells out the
// value, which gives its replay a place for a mutation control.
#ifndef CUTSCENE_SCRIPT_DEFAULT_COLOR
#define CUTSCENE_SCRIPT_DEFAULT_COLOR V_WHITE
#endif

// Script commands are introduced by a backslash and named by one
// case-insensitive letter or symbol. Their second characters (such as the
// `i`/`o` in `\wi`/`\wo`, or the `=` in `\p=`) are parsed by each command and
// named in subcommands.hpp.
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

// Called with [script_p] at the character past [c].
script_ret_t pascal near script_op(unsigned char c)
{
	// ZUN bloat: Needed for code generation reasons. The structure of the
	// conditional branches below ensures that the `return`s have no actual
	// effect.
	#define palette_black_in(x)  palette_black_in(x);  return CONTINUE;
	#define palette_black_out(x) palette_black_out(x); return CONTINUE;
	#define palette_white_in(x)  palette_white_in(x);  return CONTINUE;
	#define palette_white_out(x) palette_white_out(x); return CONTINUE;

	int i;
	int p1;
	int p2;

	// ZUN bloat: PF_FN_LEN on its own is enough, it already includes the \0
	// terminator.
	char fn[PF_FN_LEN + 3];

	c = tolower(c);
	switch(c) {
	case CUTSCENE_CMD_NEWLINE:
		cursor.y += GLYPH_H;
		cursor.x = BOX_LEFT;
		if(cursor.y < BOX_BOTTOM) {
			break;
		}
		// ZUN quirk: Since [cursor.y] is >= BOX_BOTTOM here, the Return key
		// animation will be displayed at the right edge of the "5th" line,
		// below BOX_BOTTOM. (Same issue as in cursor_advance_and_animate().)

		// fallthrough to \s if this box is full

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

		// ZUN bloat: All blitting operations in this module access the
		// intended page before they blit.
		graph_accesspage(CUTSCENE_PAGE_FOREGROUND);
		break;

	case CUTSCENE_CMD_TEXT_COLOR_OR_COLOR_MAP:
		// ZUN bloat: tolower() doesn't matter for either '=' or digits.
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
					// ZUN landmine: Does not prevent the potential deadlock
					// issue with this function.
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

			// ZUN landmine: Should restrict [p1] to 8 bits - otherwise, the
			// parameter would overflow into the function and not make this a
			// fade. (The regular snd_kaja_func() behaves this way.)
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

			// [text_fx] is also ignored here...
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

		// ZUN landmine: Blitting and palette changes will cause screen tearing
		// if done outside of VBLANK. It shouldn't be the script's
		// responsibility to prevent that.
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

	// ZUN landmine: Jumps over the additional comma separating the two
	// parameters, and assumes it's always present.
	// script_param_read_number_second() exists to handle exactly this
	// situation in a cleaner way.
	script_p += 2;

	script_param_read_number_first(p1, V_WHITE);

	// ZUN landmine: No bounds check
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

		// Same iteration code as in TH04's dialog system.
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
			i = 1; // ZUN bloat
			continue;
		}

		// Regular kanji
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
		i = 1; // ZUN bloat
	}
	bgimage_free();
	pi_free(CUTSCENE_PIC_SLOT);
}
