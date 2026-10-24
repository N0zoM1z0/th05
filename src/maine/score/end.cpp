// Natural TH05 MAINE high-score file lifecycle from ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47, th04/hiscore/end.cpp
// and its recreate/load/save implementations, GAME5/BINARYE.
#pragma option -zCSCORE_TEXT -zPGROUP_01
#include "src/maine/score/end.hpp"


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
