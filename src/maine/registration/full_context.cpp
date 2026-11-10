// Complete natural MAINE score codec / registration compiler context.
// All 14 real function bodies remain in original order; no artificial CODE prefix.
// Includes only the genuine one-byte local ROR required by the score file format.
#pragma option -zCREG_FULL_TEXT
#include "src/main/hud/resident.hpp"
// Both genuine codec function definitions now precede the score lifecycle.
#pragma codeseg REG_FULL_TEXT GROUP_01
unsigned char pascal near scoredat_decode(void);
void pascal near scoredat_encode(void);
// Score lifecycle function signatures must precede their general header.
#pragma codeseg REG_FULL_TEXT GROUP_01
void near scoredat_recreate(void);
bool pascal near hiscore_scoredat_load_for(int pc);
void near hiscore_scoredat_save(void);
#pragma codeseg _TEXT
// The two complete type headers do not declare the nine owned functions.
#include "src/op/hiscore/view.hpp"
#include "src/maine/score/end.hpp"
#include "src/maine/registration/glyphball.hpp"
// Exact real declarations; registration and sound headers separately declare
// two incompatible original game-specific sound enum names in this combined TU.
#pragma codeseg SHARED
extern "C" void far snd_se_update(void);
void pascal far frame_delay(int frames);
extern unsigned char registration_page;
#pragma codeseg REG_FULL_TEXT GROUP_01
void near scoredat_recreate(void);
bool pascal near hiscore_scoredat_load_for(int pc);
void near hiscore_scoredat_save(void);
void near score_insert(void);
void pascal near registration_score_put(int place, int pc);
void pascal near registration_stage_put(int place, int pc, int glyph);
void pascal near reg_name_put(int place, playchar_t pc, uint8_t cursor);
void pascal near registration_place_put(int place, int pc);
void pascal near places_put(int pc);
void pascal near alphabet_cursor_put(int col, int row, int attr);
void near registration_frame(void);
void pascal near glyphball_spawn(int x, int y, int place, playchar_t pc, uint8_t cursor);
void near glyphballs_update(void);
void near glyphballs_commit_and_wait(void);
void near regist_menu(void);
#include "src/maine/registration/values.hpp"
#include "src/maine/registration/insert.hpp"
#include "src/maine/registration/display.hpp"
#include "src/maine/registration/places.hpp"
#include "src/maine/registration/alphabet.hpp"
#include "src/maine/registration/motion.hpp"
#include "src/maine/registration/menu.hpp"
#pragma codeseg REG_FULL_TEXT GROUP_01
// First eight-byte score key and original near-Pascal cipher interface.
// The one-byte local rotate is genuinely required by the original codec.
unsigned char pascal near scoredat_decode(void)
{
    int index;
    int checksum;
    for(index = offsetof(scoredat_section_t, score);
        index < (sizeof(scoredat_section_t) - 1); index++) {
        unsigned char value = reinterpret_cast<unsigned char *>(&hi)[index + 1];
        _AL = hi.key2;
        asm { ror value, 3; }
        value ^= _AL;
        reinterpret_cast<unsigned char *>(&hi)[index] =
            (hi.key1 + value + reinterpret_cast<unsigned char *>(&hi)[index]);
    }
    reinterpret_cast<unsigned char *>(&hi)[index] += hi.key1;
    checksum = 0;
    for(index = offsetof(scoredat_section_t, score);
        index < sizeof(scoredat_section_t); index++) {
        checksum += reinterpret_cast<unsigned char *>(&hi)[index];
    }
    return (hi.score_sum - checksum);
}
void pascal near scoredat_encode(void)
{
    int index;
    hi.score_sum = 0;
    for(index = offsetof(scoredat_section_t, score);
        index < sizeof(scoredat_section_t); index++) {
        hi.score_sum += reinterpret_cast<unsigned char *>(&hi)[index];
    }
    hi.key1 = irand();
    hi.key2 = irand();
    unsigned char feedback = 0;
    index = sizeof(scoredat_section_t) - 1;
    while(index >= offsetof(scoredat_section_t, score)) {
        reinterpret_cast<unsigned char *>(&hi)[index] -= (hi.key1 + feedback);
        feedback = reinterpret_cast<unsigned char *>(&hi)[index];
        _AL = hi.key2;
        asm { ror feedback, 3; }
        feedback ^= _AL;
        index--;
    }
}


// th04/formats/scoredat/recreate.cpp


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
		hi.score.g_stage[i] = (gb_6 - i);

		for(c = 0; c < SCOREDAT_NAME_LEN; c++) {
			hi.score.g_name[i][c] = gs_DOT;
		}
		hi.score.g_name[i][SCOREDAT_NAME_LEN] = g_NULL;
	}

	#undef c

	#undef SCOREDAT_FN
	extern const char SCOREDAT_FN[];
	file_create(SCOREDAT_FN);
	for(i = 0; i < (RANK_COUNT * PLAYCHAR_COUNT); i++) {
		// Well, OK, if you like to fully obfuscate the format by giving every
		// section its own encraption key...
		scoredat_encode_func();
		file_write(&hi, sizeof(hi));
		scoredat_decode_func();
	}
	file_close();
}

// th04/hiscore/score_ld.cpp
// This file is probably the prime reason why you'd rather want to work on the
// `debloated` or `anniversary` branches instead.

typedef int playchar2;

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
	extern const char SCOREDAT_FN_0[];
	extern const char SCOREDAT_FN_1[];

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

// th04/hiscore/score_sv.cpp
// Leaves [hi] in encoded state.
void near hiscore_scoredat_save(void)
{
	#undef SCOREDAT_FN
	#define SCOREDAT_FN SCOREDAT_FN_2
	extern const char SCOREDAT_FN[];

	scoredat_encode_func();

	file_append(SCOREDAT_FN);

	// ZUN bloat: The TH05 version is correct for both games and all binaries.
	file_seek(
		(((playchar * RANK_COUNT) + rank) * sizeof(scoredat_section_t)),
		SEEK_SET
	);
	file_write(&hi, sizeof(scoredat_section_t));

	// Re-encode the entire score file with newly randomized encraption keys.
	// ZUN bloat: Could have been its own function, and not thrashed [hi].
	for(int i = 0; i < ((RANK_COUNT * PLAYCHAR_COUNT)); i++) {
		file_seek((i * sizeof(scoredat_section_t)), SEEK_SET);
		file_read(&hi, sizeof(scoredat_section_t));
		scoredat_decode_func();
		scoredat_encode_func();
		file_seek((i * sizeof(scoredat_section_t)), SEEK_SET);
		file_write(&hi, sizeof(scoredat_section_t));
	}
	file_close();
}

#pragma option -a
#include "src/maine/registration/insert.inl"
#include "src/maine/registration/score.inl"
#include "src/maine/registration/stage.inl"
#include "src/maine/registration/name.inl"
#include "src/maine/registration/place.inl"
#include "src/maine/registration/places.inl"
void pascal near alphabet_cursor_put(int col, int row, int attr)
{
    register int col_r = col;
    register int row_r = row;
    gaiji_putca(
        ((col_r * 2) + 23), (row_r + 21),
        gALPHABET[(row_r * REGISTRATION_ALPHABET_COLS) + col_r], attr
    );
}

void near registration_frame(void)
{
    snd_se_update();
    glyphballs_update();
    frame_delay(1);
    outportb(0xA6, registration_page);
    registration_page = 1 - registration_page;
    outportb(0xA4, registration_page);
}

#pragma option -a
#include "src/maine/registration/spawn.inl"
#include "src/maine/registration/update.inl"
void near glyphballs_commit_and_wait(void)
{
    unsigned char pending = 0;
    glyphball_t near *ball;
    int i;

    snd_se_play(11);
    for((ball = glyphballs, i = 0); i < REGISTRATION_NAME_LENGTH; (i++, ball++)) {
        if(ball->phase == GBP_CLOUD_AT_ORIGIN) {
            ball->phase = GBP_FLOAT_TO_TARGET;
        }
        if(ball->phase == GBP_FLOAT_TO_TARGET) {
            ball->angle = iatan2(
                ball->target.y - ball->pos.cur.y,
                ball->target.x - ball->pos.cur.x
            );
            ball->speed.v = 6 * 16;
        }
    }
    do {
        pending = 0;
        for((i = 0, ball = glyphballs); i < REGISTRATION_NAME_LENGTH; (i++, ball++)) {
            if(ball->phase != GBP_FREE) {
                pending++;
            }
        }
        registration_frame();
    } while(pending != 0);
}

#include "src/maine/registration/menu.inl"
