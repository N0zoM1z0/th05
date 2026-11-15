// MAINE high-score file declarations. The score record types and the rank and
// player character enums are the same as in OP and come from its header.
// See ReC98 th04/formats/scoredat/scoredat.hpp and th04/hiscore/end.cpp.
#ifndef TH05_MAINE_SCORE_END_HPP
#define TH05_MAINE_SCORE_END_HPP

#include "src/op/hiscore/view.hpp"

#if GAME != 5 || BINARY != 'E'
#error This header is for TH05's MAINE.EXE only
#endif

// MAINE has four separate copies of the score file name (see
// resource_strings.c), one per file call, instead of OP's single literal.
#undef SCOREDAT_FN
extern const char SCOREDAT_FN[];
extern const char SCOREDAT_FN_0[];
extern const char SCOREDAT_FN_1[];
extern const char SCOREDAT_FN_2[];
extern playchar_t playchar;
#define SEEK_SET 0

void near hiscore_scoredat_save(void);
extern "C" int pascal far file_append(const char far *filename);

// The score codecs are defined in src/maine/registration/full_context.cpp.
typedef char th05_maine_score_section_is_96[
    (sizeof(scoredat_section_t) == 96) ? 1 : -1];
typedef char th05_maine_score_payload_is_92[
    (sizeof(scoredat_t) == 92) ? 1 : -1];
typedef char th05_maine_score_rank_is_1[(sizeof(rank) == 1) ? 1 : -1];
typedef char th05_maine_score_playchar_is_1[(sizeof(playchar) == 1) ? 1 : -1];

#endif
