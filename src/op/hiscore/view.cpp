// TH05 score-file recreation/loading and view-only High Score menu.
// Natural C++ provenance: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47,
// th04/formats/scoredat/recreate.cpp, th04/hiscore/score_ld.cpp and view.cpp.
// GAME=5 / BINARY='O' branches only; default filenames remain ordinary text.
#pragma option -zCSCORE_TEXT -zPop_01
#include <dos.h>
#include <stdio.h>
#include "src/op/hiscore/view.hpp"



static const int SCORE_INITIAL_DIGIT = ((GAME == 5) ? 6 : 5);

void near scoredat_recreate(void)
{
	int i;
	int place;

	// ZUN bloat
	#define c place

	// ACTUAL TYPE: gaiji_th04_t
	unsigned char digit = (gb_0 + 10 - (10 / SCOREDAT_PLACES));

	for(i = 0; i < SCOREDAT_PLACES; i++) {
		hi.score.cleared = SCOREDAT_NOT_CLEARED;
		for(c = 0; c < SCORE_DIGITS; c++) {
			hi.score.g_score[i].digits[c] = gb_0;
		}

		if(i == 0) {
			hi.score.g_score[i].digits[SCORE_INITIAL_DIGIT - 0] = gb_1;
		} else {
			hi.score.g_score[i].digits[SCORE_INITIAL_DIGIT - 1] = digit;

			// ZUN bloat: `digit -= (10 / SCOREDAT_PLACES);` would work for
			// both games.
			digit -= (10 / SCOREDAT_PLACES);
		}

		// ZUN landmine: This assigns decreasing stage numbers even for TH05's
		// Extra Stage, which should default to a constant 1 according to the
		// loop below.
		// Classifying this as a landmine because it's impossible for the
		// MAINE.EXE version of this code to ever run within our criteria of
		// observability - OP.EXE will have always regenerated [SCOREDAT_FN] if
		// it didn't exist or was corrupted, so this code can only ever run if
		// the file was somehow modified or deleted from outside the game while
		// it was running.

		for(c = 0; c < SCOREDAT_NAME_LEN; c++) {
			hi.score.g_name[i][c] = gs_DOT;
		}
		hi.score.g_name[i][SCOREDAT_NAME_LEN] = g_NULL;
	}

	#undef c

	file_create(SCOREDAT_FN);
	for(i = 0; i < (RANK_COUNT * PLAYCHAR_COUNT); i++) {
		for(place = 0; place < SCOREDAT_PLACES; place++) {
			if((i % RANK_COUNT) == RANK_EXTRA) {
				hi.score.g_stage[place] = gb_1;
			} else {
				hi.score.g_stage[place] = (gb_1 + SCOREDAT_PLACES - place);
			}
		}
		// Well, OK, if you like to fully obfuscate the format by giving every
		// section its own encraption key...
		scoredat_encode_func();
		file_write(&hi, sizeof(hi));
		scoredat_decode_func();
	}
	file_close();
}

// This file is probably the prime reason why you'd rather want to work on the
// `debloated` or `anniversary` branches instead.


// ZUN bloat: Take [rank] as a parameter instead.
extern unsigned char rank;

#define recreated true
#define loaded false
// Loads the score data for the given [playchar] at the global [rank] into
// [hi]. Returns `false` if the data was loaded and decoded correctly, or
// `true` if the defaults were recreated.
// ZUN bloat: Use the regular `playchar_t` type.
bool pascal near hiscore_scoredat_load_for(playchar2 playchar)
{
	#define SCOREDAT_FN_0 SCOREDAT_FN
	#define SCOREDAT_FN_1 SCOREDAT_FN

	// ZUN bloat: Classic TOCTOU issue; file_ropen() also fails if the file
	// doesn't exist. Doesn't have any consequences in this case though: In the
	// very unlikely event that the file stops existing between file_exist()
	// and file_ropen(), the following will happen:
	// * All file-related calls will fail and leave old score data in [hi] and
	//   [hi2].
	// * scoredat_decode() re-decodes already decoded data and fails.
	// * The code then recreates score data just as it would have if the file
	//   hadn't existed in this initial check.
	// Hence, this is not a landmine, just bloat.
	if(file_exist(SCOREDAT_FN_0)) {
		file_ropen(SCOREDAT_FN_1);

		// ZUN bloat: The TH05 version is correct for both games and all
		// binaries.
		file_seek(
			(((playchar * RANK_COUNT) + rank) * sizeof(scoredat_section_t)),
			SEEK_SET
		);
		file_read(&hi, sizeof(scoredat_section_t));
		file_close();

		// ZUN landmine: In TH04, scoredat_recreate() only writes to [hi] and
		// leaves [hi2] as it is. TH04's High Score viewer in OP.EXE uses both
		// sections and doesn't double-check whether it contains valid data,
		// because why should it, this is our job. But this means that it will
		// render garbage data in both cases:
		//
		// * If Reimu/[hi] is corrupt, scoredat_decode() exits early and
		//   doesn't decode [hi2]. The call site assumes that it got decoded,
		//   though, and consequently renders garbage. The fact that [hi]
		//   receives the default data from scoredat_recreate() doesn't even
		//   matter because the corruption from [hi2] will most likely mess up
		//   the entire screen.
		//
		// * If Marisa/[hi2] is corrupt, [hi2] did get decoded, but still
		//   carries the same garbage data that failed decoding.
		//
		// Both sections then only get loaded correctly on the next call to
		// this function.
		if(scoredat_decode_func() != 0) {
			scoredat_recreate();
			return recreated;
		}
	} else {
		// Same TH04 landmine as above.
		scoredat_recreate();
		return recreated;
	}
	return loaded;
}

/// View-only High Score menu
/// -------------------------


enum hiscore_patnum_t {
	// scnum.bft
	// ---------
	PAT_SCNUM = 0,
	PAT_SCNUM_last = (PAT_SCNUM + 9),
	PAT_SCNUM_UNUSED,
	PAT_SCNUM_UNUSED_last = (PAT_SCNUM_UNUSED + 9),
	// ---------
	// hi_m.bft
	// --------
	PAT_RANK_1,
	PAT_RANK_2,
	PAT_RANK_last = (PAT_RANK_1 + (RANK_COUNT * 2) - 1),
	// --------
};

enum hiscore_colors_t {
	COL_NAME = 2,
	COL_NAME_FIRST = 7,
	COL_STAGE = 7,
	COL_SHADOW = 14,
};

/// Coordinates
/// -----------

static const pixel_t NAME_W = (SCOREDAT_NAME_LEN * GAIJI_W);
static const pixel_t DIGIT_W = 16;

// The optional 9th score digit is written into the name padding.
static const pixel_t NAME_PADDED_W = (NAME_W + ((GAME == 5) ? 6 : 4) + DIGIT_W);

static const pixel_t SCORE_PADDED_W = ((DIGIT_W * SCORE_DIGITS) + 8);
static const pixel_t STAGE_PADDED_W = (GAIJI_W + 8);
static const pixel_t COLUMN_W = (
	NAME_PADDED_W + SCORE_PADDED_W + STAGE_PADDED_W + ((GAME == 5) ? 10 : 0)
);

static const pixel_t RANK_W = 128;

// These obviously only apply to the leftmost column.
static const screen_x_t NAME_LEFT = 8;
static const screen_x_t SCORE_LEFT = (NAME_LEFT + NAME_PADDED_W);
static const screen_x_t STAGE_LEFT = (SCORE_LEFT + SCORE_PADDED_W);

static const screen_y_t TABLE_1_TOP = 88;
static const screen_y_t TABLE_2_TOP = 224;
static const pixel_t PLACE_1_PADDING_BOTTOM = 8;

static const screen_x_t RANK_LEFT = (RES_X - GLYPH_FULL_W - RANK_W);
static const screen_y_t RANK_TOP = (RES_Y - (GLYPH_H / 2) - GLYPH_H);
/// -----------

/// State
/// -----

scoredat_section_t hi;
scoredat_section_t hi2;
static uint8_t scoredat_unused; // ZUN bloat

unsigned char rank;
unsigned char cleared_with[PLAYCHAR_COUNT][RANK_COUNT];
bool extra_unlocked;
/// -----

// ZUN bloat: The main difference between the TH04 and TH05 implementations is
// that TH04 explicitly spells out its two characters while TH05 sanely loops
// over its four. The `debloated` branch would also migrate TH04 to loops.

#define digit_at(section, place, digit) ( \
	((section.score.g_score[place].digits[digit]) - gb_0) \
)

#define digit_put(left, top, digit) { \
	super_put(left, top, (PAT_SCNUM + digit)); \
}

// ZUN bug: Since score addition in MAIN.EXE effectively turns the most
// significant digit of a `score_lebcd_t` value from BCD to binary for scores
// past 99,999,999, the type would support a maximum score of 2,559,999,999
// points, or `09 09 09 09 09 09 09 FF` in memory. TH04's OMAKE.TXT confirms
// that ZUN knew it was possible to reach more than 100 million points in that
// game, and so he equipped this menu with the ability to interpret the last
// byte as binary and display a 9th digit in what would normally be the padding
// between name and score.
// However, `scoredat_section_t` stores its digits as gaiji, with an offset of
// [gb_0_]. This makes no sense no matter *how* you look at it, since both the
// in-game HUD and this High Score screen would prefer raw digits from 0 to 9.
// At first, this *seems* like no big deal because subtracting [gb_0_] would
// always correctly remove that offset, even if a digit's value wrapped around
// 0. But the problems then arise when such a subtraction is done as an
// expression that gets promoted to `int` as per C's integer promotion rules...
// such as when dividing by an untyped 10 in both functions below. As a result,
// the subtraction actually yields a negative integer, the result of the
// division remains negative as well, and the subsequent super_put() call ends
// up corrupting VRAM as master.lib does not bounds-check the patnum parameter.
// Therefore, this screen only supports a maximum 8th and 9th digit value of
// (0xFF - 0xA0) = 95, or a total score of 959,999,999 - not the 999 million
// you would expect.
//
// (At least scores above 1 billion on both unmodified games seem to be way out
// of reach as of December 2024, so you can't really complain about the lack of
// support for a 10th digit.)

void pascal near score_put(screen_x_t left, screen_y_t top, int place)
{
	HISCORE_STATIC_ASSERT(SCORE_DIGITS == 8);
	if(digit_at(hi, place, 7) >= 10) {
		digit_put((left + (-1 * DIGIT_W)), top, (digit_at(hi, place, 7) / 10));
	}
	digit_put(left, top, (digit_at(hi, place, 7) % 10));
	left += DIGIT_W;

	int digit = (SCORE_DIGITS - 2);
	while(digit >= 0) {
		digit_put(left, top, digit_at(hi, place, digit));
		digit--;
		left += DIGIT_W;
	}
}

void pascal near stage_put(
	screen_x_t left, screen_y_t top, int gaiji // ACTUAL TYPE: gaiji_th04_t
)
{
	// ZUN bloat: Reassigning [gaiji] would have been simpler.
	if(gaiji != g_NONE) {
		graph_gaiji_putc((left + 2), (top + 2), gaiji, COL_SHADOW);
		graph_gaiji_putc((left + 0), (top + 0), gaiji, COL_STAGE);
	} else {
		graph_gaiji_putc(
			(left + 2), (top + 2), g_HISCORE_STAGE_EMPTY, COL_SHADOW
		);
		graph_gaiji_putc(
			(left + 0), (top + 0), g_HISCORE_STAGE_EMPTY, COL_STAGE
		);
	}
}

#define name_put_shadowed(left, top, str, col_fg) { \
	graph_gaiji_puts((left + 2), (top + 2), GAIJI_W, str, COL_SHADOW); \
	graph_gaiji_puts((left + 0), (top + 0), GAIJI_W, str, col_fg); \
}

void pascal near place_put(playchar2 playchar, int place)
{
	screen_x_t left;
	screen_y_t top;
	vc2 name_col;

	// ZUN bloat: Could have been calculated arithmetically...
	if(place == 0) {
		switch(playchar) {
		case PLAYCHAR_REIMU:
			left = (NAME_LEFT + (0 * COLUMN_W));
			top = TABLE_1_TOP;
			break;
		case PLAYCHAR_MARISA:
			left = (NAME_LEFT + (1 * COLUMN_W));
			top = TABLE_1_TOP;
			break;
		case PLAYCHAR_MIMA:
			left = (NAME_LEFT + (0 * COLUMN_W));
			top = TABLE_2_TOP;
			break;
		case PLAYCHAR_YUUKA:
			left = (NAME_LEFT + (1 * COLUMN_W));
			top = TABLE_2_TOP;
			break;
		}
		name_col = COL_NAME_FIRST;
	} else {
		// ZUN bloat: ...and without branching by place.
		switch(playchar) {
		case PLAYCHAR_REIMU:
			left = (NAME_LEFT + (0 * COLUMN_W));
			top = (TABLE_1_TOP + PLACE_1_PADDING_BOTTOM + (place * GLYPH_H));
			break;
		case PLAYCHAR_MARISA:
			left = (NAME_LEFT + (1 * COLUMN_W));
			top = (TABLE_1_TOP + PLACE_1_PADDING_BOTTOM + (place * GLYPH_H));
			break;
		case PLAYCHAR_MIMA:
			left = (NAME_LEFT + (0 * COLUMN_W));
			top = (TABLE_2_TOP + PLACE_1_PADDING_BOTTOM + (place * GLYPH_H));
			break;
		case PLAYCHAR_YUUKA:
			left = (NAME_LEFT + (1 * COLUMN_W));
			top = (TABLE_2_TOP + PLACE_1_PADDING_BOTTOM + (place * GLYPH_H));
			break;
		}
		name_col = COL_NAME;
	}
	name_put_shadowed(
		left,
		top,
		reinterpret_cast<const char far *>(hi.score.g_name[place]),
		name_col
	);
	score_put((left + (SCORE_LEFT - NAME_LEFT)), top, place);
	stage_put((left + (STAGE_LEFT - NAME_LEFT)), top, hi.score.g_stage[place]);
}

void near rank_render(void)
{
	// ZUN bloat: The palette is not page-dependent...
	graph_accesspage(1);	pi_palette_apply(0);	pi_put_8(0, 0, 0);
	graph_accesspage(0);	pi_palette_apply(0);	pi_put_8(0, 0, 0);

	for(playchar2 pc = PLAYCHAR_REIMU; pc < PLAYCHAR_COUNT; pc++) {
		hiscore_scoredat_load_for(pc);
		for(int place = 0; place < SCOREDAT_PLACES; place++) {
			place_put(pc, place);
		}
	}

	HISCORE_STATIC_ASSERT(RANK_W == (2 * BFNT_ASSUMED_MAX_W));
	super_put(
		(RANK_LEFT + (0 * (RANK_W / 2))), RANK_TOP, (PAT_RANK_1 + (rank * 2))
	);
	super_put(
		(RANK_LEFT + (1 * (RANK_W / 2))), RANK_TOP, (PAT_RANK_2 + (rank * 2))
	);
}

void near regist_view_menu(void)
{
	snd_kaja_func(KAJA_SONG_STOP, 0);
	snd_load(BGM_HISCORE_FN, SND_LOAD_SONG);
	snd_kaja_func(KAJA_SONG_PLAY, 0);

	// ZUN bloat: This both
	// * doesn't work, because fade-ins require the volume to be set to a lower
	//   value than what [KAJA_SONG_PLAY] resets it to, and
	// * sounds terrible, because -128 is the fastest but still not quite
	//   instant fade speed. This leaves the initial note on each channel muted
	//   while the rest of the track fades in very abruptly, clashing with the
	//   bass and chord notes of the name registration themes in both games.
	snd_kaja_func(KAJA_SONG_FADE, -128);

	palette_black_out(1);
	rank = resident->rank;

	pi_load(0, HISCORE_BG_FN);
	rank_render();
	palette_black_in(1);

	while(1) {
		// ZUN bug: The TH04 version of this function doesn't address the PC-98
		// keyboard quirk documented in the `Research/HOLDKEY` example, which
		// causes input to occasionally be processed a frame or two later than
		// expected. Not that big of a deal given that every key press launches
		// a 16-frame palette fade animation, but a bug nonetheless.
		input_reset_sense_interface();
		frame_delay(1);

		// ZUN bloat: Testing twice for [INPUT_OK].
		if(
			(key_det & INPUT_OK) || (key_det & INPUT_SHOT) ||
			(key_det & INPUT_CANCEL) || (key_det & INPUT_OK)
		) {
			break;
		}
		if((key_det & INPUT_LEFT) && (rank != RANK_EASY)) {
			rank--;
			palette_settone(0);
			rank_render();
			palette_black_in(1);
		}
		if((key_det & INPUT_RIGHT) && (rank < RANK_EXTRA)) {
			rank++;
			palette_settone(0);
			rank_render();
			palette_black_in(1);
		}
	}

	snd_kaja_func(KAJA_SONG_FADE, 1);
	palette_black_out(1);
	pi_free(0);
	graph_accesspage(1);
	pi_fullres_load_palette_apply_put_free(0, MENU_MAIN_BG_FN);
	graph_copy_page(0);
	palette_black_in(1);

	do {
		// ZUN bug: With that one PC-98 keyboard quirk still not addressed in
		// TH04, the loop will break relatively quickly even while the player
		// is still holding a key. This cuts short any attempt to listen to the
		// fade-out by holding a key. In TH05, this works as intended.
		// (At least it proves that this loop wasn't actually necessary to
		// ensure that this menu isn't re-entered, confirming this entire loop
		// to be an easter egg that allows the player to actually listen to the
		// BGM fade-out.)
		input_reset_sense_interface();
		frame_delay(1);
	} while(key_det != INPUT_NONE);

	snd_kaja_func(KAJA_SONG_STOP, 0);
	snd_load(BGM_MENU_MAIN_FN, SND_LOAD_SONG);
	snd_kaja_func(KAJA_SONG_PLAY, 0);
}

void near cleardata_and_regist_view_sprites_load(void)
{
	extra_unlocked = false;
	for(int playchar = PLAYCHAR_REIMU; playchar < PLAYCHAR_COUNT; playchar++) {
		rank = RANK_EASY;
		while(rank < RANK_COUNT) {
			if(hiscore_scoredat_load_for(playchar)) {
				break;
			}
			cleared_with[playchar][rank] = hi.score.cleared;
			if(cleared_with[playchar][rank] != SCOREDAT_CLEARED) {
				cleared_with[playchar][rank] = false;
			}
			if(rank < RANK_EXTRA) {
				extra_unlocked |= cleared_with[playchar][rank];
			}
			rank++;
		}
	}

	// See the call site for why these load calls absolutely don't belong here.
	rank = resident->rank;
	super_entry_bfnt("scnum.bft");
	super_entry_bfnt("hi_m.bft");

	// ZUN bloat: Integrate into the upper loop
	for(playchar = PLAYCHAR_REIMU; playchar < PLAYCHAR_COUNT; playchar++) {
		extra_playable_with[playchar] = (
			cleared_with[playchar][RANK_EASY] |
			cleared_with[playchar][RANK_NORMAL] |
			cleared_with[playchar][RANK_HARD] |
			cleared_with[playchar][RANK_LUNATIC]
		);
	}
}

