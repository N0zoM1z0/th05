// Genuine TH05 MAINE score ABI. The score92/section96 definitions and full
// rank/player-character enum domains are identical to OP and reused read-only.
// Natural-source provenance: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47,
// th04/formats/scoredat/scoredat.hpp, th04/hiscore/end.cpp, th05/playchar.h.
#ifndef TH05_MAINE_SCORE_END_HPP
#define TH05_MAINE_SCORE_END_HPP

#include "src/op/hiscore/view.hpp"

#if GAME != 5 || BINARY != 'E'
#error This owner is the TH05 MAINE high-score file lifecycle
#endif

// MAINE uses four distinct foreign const arrays in its registration module,
// not OP's coalesced literal or four pointer aliases. This owner defines none.
#undef SCOREDAT_FN
extern const char SCOREDAT_FN[];
extern const char SCOREDAT_FN_0[];
extern const char SCOREDAT_FN_1[];
extern const char SCOREDAT_FN_2[];
extern playchar_t playchar;
#define SEEK_SET 0

void near hiscore_scoredat_save(void);
extern "C" int pascal far file_append(const char far *filename);

// The canonical score declarations above give the codecs their genuine
// no-argument near-Pascal ABI. Their active ROR primitives require assembly
// in both references and are deliberately foreign to this natural C++ owner.
typedef char th05_maine_score_section_is_96[
    (sizeof(scoredat_section_t) == 96) ? 1 : -1];
typedef char th05_maine_score_payload_is_92[
    (sizeof(scoredat_t) == 92) ? 1 : -1];
typedef char th05_maine_score_rank_is_1[(sizeof(rank) == 1) ? 1 : -1];
typedef char th05_maine_score_playchar_is_1[(sizeof(playchar) == 1) ? 1 : -1];

#endif
